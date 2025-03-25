import re
import string
import math
import jellyfish
from collections import namedtuple

from segtok.segmenter import split_multi
from segtok.tokenizer import web_tokenizer, split_contractions

import networkx as nx
import numpy as np

STOPWORD_WEIGHT = 'bi'

# Group word position parameters into a single structure
Positions = namedtuple("Positions", ["pos_sent", "sentence_id", "pos_text"])


class WordProcessingContext:
    """Encapsulates parameters for word processing."""
    def __init__(self, word, positions: Positions, block_of_word_obj):
        self.word = word
        self.positions = positions
        self.block_of_word_obj = block_of_word_obj

    def get_word_info(self):
        """Returns a dictionary with word information."""
        return {
            'word': self.word,
            'position_in_sentence': self.positions.pos_sent,
            'sentence_id': self.positions.sentence_id,
            'position_in_text': self.positions.pos_text
        }

    def append_to_block(self, tag, term_obj):
        """Adds a processed word to the block of word objects."""
        self.block_of_word_obj.append((tag, self.word, term_obj))


class SentenceProcessingContext:
    """Encapsulates parameters for sentence processing."""
    def __init__(self, sentence, sentence_id, pos_text):
        self.sentence = sentence
        self.sentence_id = sentence_id
        self.pos_text = pos_text
        self.sentence_obj_aux = []
        self.block_of_word_obj = []

    def clear_block(self):
        """Clears the current block and stores it if non-empty."""
        if self.block_of_word_obj:
            self.sentence_obj_aux.append(self.block_of_word_obj)
            self.block_of_word_obj = []

    def get_sentence_info(self):
        """Returns a dictionary with sentence information."""
        return {
            'sentence': self.sentence,
            'sentence_id': self.sentence_id,
            'word_count': len(self.sentence),
            'processed_blocks': len(self.sentence_obj_aux)
        }


class DataCoreConfig:
    """Configuration for DataCore."""
    def __init__(self, stopword_set, windows_size, n, tags_to_discard=None, exclude=None):
        self.stopword_set = stopword_set
        self.windows_size = windows_size
        self.n = n
        self.tags_to_discard = tags_to_discard if tags_to_discard is not None else {'u', 'd'}
        self.exclude = exclude if exclude is not None else set(string.punctuation)


class DataCore:
    """Core data structure for text analysis."""
    def __init__(self, text, stopword_set=None, windows_size=None, n=None, tags_to_discard=None, exclude=None, **kwargs):
        """
        Backward compatible constructor.
        
        Expected usage in tests:
            DataCore(text, stopword_set=<...>, windows_size=<...>, n=<...>, ...)
        
        Alternatively, a config object can be passed via keyword 'config'.
        """
        if stopword_set is not None and windows_size is not None and n is not None:
            self.config_params = DataCoreConfig(stopword_set, windows_size, n, tags_to_discard, exclude)
        elif 'config' in kwargs:
            self.config_params = kwargs['config']
        else:
            raise TypeError("Missing required arguments: stopword_set, windows_size, and n must be provided")
        
        # Text analysis stats
        self._stats = {
            'number_of_sentences': 0,
            'number_of_words': 0,
            'freq_ns': {i + 1: 0. for i in range(self.config_params.n)}
        }

        # Text components
        self._components = {
            'terms': {},
            'candidates': {},
            'sentences_obj': [],
            'sentences_str': []
        }

        # Graph configuration
        self._graph = nx.DiGraph()

        # Build core structures from the text
        self._build(text)

    @property
    def number_of_sentences(self):
        return self._stats['number_of_sentences']

    @property
    def number_of_words(self):
        return self._stats['number_of_words']

    @property
    def terms(self):
        return self._components['terms']

    @property
    def candidates(self):
        return self._components['candidates']

    @property
    def sentences_obj(self):
        return self._components['sentences_obj']

    @property
    def sentences_str(self):
        return self._components['sentences_str']

    @property
    def g(self):
        return self._graph

    @property
    def exclude(self):
        return self.config_params.exclude

    @property
    def tags_to_discard(self):
        return self.config_params.tags_to_discard

    @property
    def freq_ns(self):
        return self._stats['freq_ns']

    @property
    def stopword_set(self):
        return self.config_params.stopword_set

    def build_candidate(self, candidate_string):
        tokens = [w for w in split_contractions(web_tokenizer(candidate_string.lower()))
                  if not (w.startswith("'") and len(w) > 1) and w]
        candidate_terms = []
        for i, word in enumerate(tokens):
            tag = self.get_tag(word, i)
            term_obj = self.get_term(word, save_non_seen=False)
            if term_obj.tf_stats['tf'] == 0:
                term_obj = None
            candidate_terms.append((tag, word, term_obj))
        if not any(cand[2] is not None for cand in candidate_terms):
            return ComposedWord(None)
        return ComposedWord(candidate_terms)

    def _build(self, text):
        text = self.pre_filter(text)
        self._components['sentences_str'] = self.tokenize_sentences(text)
        self._stats['number_of_sentences'] = len(self._components['sentences_str'])
        pos_text = 0
        for sentence_id, sentence in enumerate(self._components['sentences_str']):
            context = SentenceProcessingContext(sentence, sentence_id, pos_text)
            pos_text = self._process_sentence(context)
        self._stats['number_of_words'] = pos_text

    def tokenize_sentences(self, text):
        return [
            [w for w in split_contractions(web_tokenizer(s)) if not (w.startswith("'") and len(w) > 1) and w]
            for s in split_multi(text) if s.strip()
        ]

    def _process_sentence(self, context: SentenceProcessingContext):
        for pos_sent, word in enumerate(context.sentence):
            if all(c in self.exclude for c in word):
                context.clear_block()
            else:
                positions = Positions(pos_sent, context.sentence_id, context.pos_text)
                word_context = WordProcessingContext(word, positions, context.block_of_word_obj)
                context.pos_text = self._process_word(word_context)
        context.clear_block()
        if context.sentence_obj_aux:
            self._components['sentences_obj'].append(context.sentence_obj_aux)
        return context.pos_text

    def _process_word(self, context: WordProcessingContext):
        tag = self.get_tag(context.word, context.positions.pos_sent)
        term_obj = self.get_term(context.word)
        term_obj.add_occur(tag, context.positions.sentence_id, context.positions.pos_sent, context.positions.pos_text)
        # Increment text position
        context.positions = context.positions._replace(pos_text=context.positions.pos_text + 1)
        if tag not in self.tags_to_discard:
            self._update_cooccurrence(context.block_of_word_obj, term_obj)
        self._generate_candidates((tag, context.word), term_obj, context.block_of_word_obj)
        context.append_to_block(tag, term_obj)
        return context.positions.pos_text

    def _update_cooccurrence(self, block_of_word_obj, term_obj):
        window = self.config_params.windows_size
        indices = range(max(0, len(block_of_word_obj) - window), len(block_of_word_obj))
        for i in indices:
            if block_of_word_obj[i][0] not in self.tags_to_discard:
                self.add_cooccur(block_of_word_obj[i][2], term_obj)

    def _generate_candidates(self, term, term_obj, block_of_word_obj):
        candidate = [term + (term_obj,)]
        cand = ComposedWord(candidate)
        self.add_or_update_composedword(cand)
        window_n = self.config_params.n
        indices = range(max(0, len(block_of_word_obj) - (window_n - 1)), len(block_of_word_obj))[::-1]
        for i in indices:
            candidate.append(block_of_word_obj[i])
            self._stats['freq_ns'][len(candidate)] += 1.
            cand = ComposedWord(candidate[::-1])
            self.add_or_update_composedword(cand)

    def build_single_terms_features(self, features=None):
        valid_terms = [term for term in self._components['terms'].values() if not term.stopword]
        valid_tfs = np.array([term.tf_stats['tf'] for term in valid_terms])
        if valid_tfs.size == 0:
            return
        avg_tf = valid_tfs.mean()
        std_tf = valid_tfs.std()
        max_tf = max(term.tf_stats['tf'] for term in self._components['terms'].values())
        stats = {
            'max_tf': max_tf,
            'avg_tf': avg_tf,
            'std_tf': std_tf,
            'number_of_sentences': self._stats['number_of_sentences']
        }
        for term in self._components['terms'].values():
            term.update_h(stats, features=features)

    def build_mult_terms_features(self, features=None):
        for cand in self._components['candidates'].values():
            if cand.is_valid():
                cand.update_h(features=features)

    def pre_filter(self, text):
        prog = re.compile(r"^(\s*([A-Z]))")
        parts = text.split('\n')
        buffer = ''
        for part in parts:
            sep = ' '
            if prog.match(part):
                sep = '\n\n'
            buffer += sep + part.replace('\t', ' ')
        return buffer

    def get_tag(self, word, i):
        try:
            w2 = word.replace(",", "")
            float(w2)
            return "d"
        except ValueError:
            cdigit = sum(c.isdigit() for c in word)
            calpha = sum(c.isalpha() for c in word)
            if (cdigit > 0 and calpha > 0) or (cdigit == 0 and calpha == 0) or \
               sum(c in self.exclude for c in word) > 1:
                return "u"
            if len(word) == sum(1 for c in word if c.isupper()):
                return "a"
            if sum(1 for c in word if c.isupper()) == 1 and len(word) > 1 and word[0].isupper() and i > 0:
                return "n"
        return "p"

    def get_term(self, str_word, save_non_seen=True):
        unique_term = str_word.lower()
        is_stopword = unique_term in self.stopword_set
        if unique_term.endswith('s') and len(unique_term) > 3:
            unique_term = unique_term[:-1]
        if unique_term in self._components['terms']:
            return self._components['terms'][unique_term]
        simple_term = unique_term
        for punc in self.exclude:
            simple_term = simple_term.replace(punc, '')
        is_stopword = is_stopword or unique_term in self.stopword_set or len(simple_term) < 3
        term_id = len(self._components['terms'])
        term_obj = SingleWord(unique_term, term_id, self._graph)
        term_obj.stopword = is_stopword
        if save_non_seen:
            self._graph.add_node(term_id)
            self._components['terms'][unique_term] = term_obj
        return term_obj

    def add_cooccur(self, left_term, right_term):
        if right_term.id not in self._graph[left_term.id]:
            self._graph.add_edge(left_term.id, right_term.id, tf=0.)
        self._graph[left_term.id][right_term.id]["tf"] += 1.

    def add_or_update_composedword(self, cand):
        if cand.unique_kw not in self._components['candidates']:
            self._components['candidates'][cand.unique_kw] = cand
        else:
            self._components['candidates'][cand.unique_kw].uptade_cand(cand)
        self._components['candidates'][cand.unique_kw].tf += 1.


class ComposedWord:
    def __init__(self, terms):
        """
        Represents a composed word from a list of terms.
        Args:
            terms (list): List of tuples (tag, word, term_obj)
        """
        if terms is None:
            self.start_or_end_stopwords = True
            self.tags = set()
            return
        self.tags = {''.join([w[0] for w in terms])}
        self.kw = ' '.join([w[1] for w in terms])
        self.unique_kw = self.kw.lower()
        self.size = len(terms)
        self.terms = [w[2] for w in terms if w[2] is not None]
        self.tf = 0.
        self.integrity = 1.
        self.h = 1.
        self.start_or_end_stopwords = self.terms[0].stopword or self.terms[-1].stopword

    def uptade_cand(self, cand):
        for tag in cand.tags:
            self.tags.add(tag)

    def is_valid(self):
        valid = any("u" not in tag and "d" not in tag for tag in self.tags)
        return valid and not self.start_or_end_stopwords

    def get_composed_feature(self, feature_name, discart_stopword=True):
        features = [getattr(term, feature_name) for term in self.terms
                    if (discart_stopword and not term.stopword) or not discart_stopword]
        sum_f = sum(features)
        prod_f = np.prod(features)
        return (sum_f, prod_f, prod_f / (sum_f + 1))

    def build_features(self, params):
        """
        Build features for the composed word.

        Args:
            params (dict): Dictionary with keys such as 'doc_id', 'keys', 'rel', 'rel_approx', and 'is_virtual'.
        Returns:
            tuple: (features_cand, columns, seen)
        """
        features = params.get('features', ['wfreq', 'wrel', 'tf', 'wcase', 'wpos', 'wspread'])
        _stopword = params.get('_stopword', [True, False])
        columns = []
        features_cand = []
        seen = set()
        if params.get('doc_id') is not None:
            columns.append('doc_id')
            features_cand.append(params['doc_id'])
        if params.get('keys') is not None:
            if params.get('rel', True):
                columns.append('rel')
                if self.unique_kw in params['keys'] or params.get('is_virtual', False):
                    features_cand.append(1)
                    seen.add(self.unique_kw)
                else:
                    features_cand.append(0)
            if params.get('rel_approx', True):
                columns.append('rel_approx')
                max_gold = ('', 0.)
                for gold_key in params['keys']:
                    dist = 1. - jellyfish.levenshtein_distance(gold_key, self.unique_kw) / max(len(gold_key), len(self.unique_kw))
                    max_gold = (gold_key, dist)
                features_cand.append(max_gold[1])
                features_cand.append(max_gold[1])
        columns.append('kw')
        features_cand.append(self.unique_kw)
        columns.append('h')
        features_cand.append(self.h)
        columns.append('tf')
        features_cand.append(self.tf)
        columns.append('size')
        features_cand.append(self.size)
        columns.extend(['is_virtual', 'is_virtual'])
        features_cand.append(int(params.get('is_virtual', False)))
        for feature_name in features:
            for discart_stopword in _stopword:
                s, p, sp = self.get_composed_feature(feature_name, discart_stopword=discart_stopword)
                prefix = 'n' if discart_stopword else ''
                columns.append(f"{prefix}s_sum_K{feature_name}")
                features_cand.append(s)
                columns.append(f"{prefix}s_prod_K{feature_name}")
                features_cand.append(p)
                columns.append(f"{prefix}s_sum_prod_K{feature_name}")
                features_cand.append(sp)
        return (features_cand, columns, seen)

    def update_h(self, features=None, is_virtual=False):
        sum_h = 0.
        prod_h = 1.
        for t, term in enumerate(self.terms):
            if not term.stopword:
                sum_h += term.h
                prod_h *= term.h
            else:
                if STOPWORD_WEIGHT == 'bi':
                    prob_t1 = 0.
                    if t > 0 and term.g.has_edge(self.terms[t - 1].id, term.id):
                        prob_t1 = term.g[self.terms[t - 1].id][term.id]["tf"] / self.terms[t - 1].tf_stats['tf']
                    prob_t2 = 0.
                    if t < len(self.terms) - 1 and term.g.has_edge(term.id, self.terms[t + 1].id):
                        prob_t2 = term.g[term.id][self.terms[t + 1].id]["tf"] / self.terms[t + 1].tf_stats['tf']
                    prob = prob_t1 * prob_t2
                    prod_h *= (1 + (1 - prob))
                    sum_h -= (1 - prob)
                elif STOPWORD_WEIGHT == 'h':
                    sum_h += term.h
                    prod_h *= term.h
                elif STOPWORD_WEIGHT == 'none':
                    pass
        tf_used = self.tf
        if features is None or "KPF" in features:
            tf_used = self.tf
        if is_virtual:
            tf_used = np.mean([term.tf_stats['tf'] for term in self.terms])
        self.h = prod_h / ((sum_h + 1) * tf_used)

    def update_h_old(self, features=None, is_virtual=False):
        sum_h = 0.
        prod_h = 1.
        for t, term in enumerate(self.terms):
            if is_virtual and term.tf_stats['tf'] == 0:
                continue
            if term.stopword:
                prob_t1 = 0.
                if term.g.has_edge(self.terms[t - 1].id, term.id):
                    prob_t1 = term.g[self.terms[t - 1].id][term.id]["tf"] / self.terms[t - 1].tf_stats['tf']
                prob_t2 = 0.
                if term.g.has_edge(term.id, self.terms[t + 1].id):
                    prob_t2 = term.g[term.id][self.terms[t + 1].id]["tf"] / self.terms[t + 1].tf_stats['tf']
                prob = prob_t1 * prob_t2
                prod_h *= (1 + (1 - prob))
                sum_h -= (1 - prob)
            else:
                sum_h += term.h
                prod_h *= term.h
        tf_used = self.tf
        if features is None or "KPF" in features:
            tf_used = self.tf
        if is_virtual:
            tf_used = np.mean([term.tf_stats['tf'] for term in self.terms])
        self.h = prod_h / ((sum_h + 1) * tf_used)


class SingleWord:
    """Represents a single word with associated statistics and features."""
    def __init__(self, unique, idx, graph):
        self.unique_term = unique
        self.id = idx
        # Group term-frequency stats into a dictionary
        self.tf_stats = {'tf': 0.0, 'tf_a': 0.0, 'tf_n': 0.0}
        self.occurs = {}
        self.stopword = False
        self.g = graph
        # Group computed features into a dictionary
        self.features = {
            'wfreq': 0.0,
            'wcase': 0.0,
            'wrel': 1.0,
            'wpos': 1.0,
            'wspread': 0.0,
            'h': 0.0,
            'pagerank': 1.0
        }

    @property
    def h(self):
        """Expose the computed 'h' feature for compatibility."""
        return self.features.get('h', 0)

    def update_h(self, stats, features=None):
        max_tf = stats['max_tf']
        avg_tf = stats['avg_tf']
        std_tf = stats['std_tf']
        number_of_sentences = stats['number_of_sentences']

        self.features['wcase'] = max(self.tf_stats['tf_a'], self.tf_stats['tf_n']) / (1. + math.log(self.tf_stats['tf'] or 1))
        self.features['wpos'] = math.log(math.log(3. + np.median(list(self.occurs.keys())))) if self.occurs else 0
        self.features['wfreq'] = self.tf_stats['tf'] / (avg_tf + std_tf)
        self.features['wspread'] = len(self.occurs) / number_of_sentences
        self.features['wrel'] = ((0.5 + (self.pwl * (self.tf_stats['tf'] / max_tf))) +
                                 (0.5 + (self.pwr * (self.tf_stats['tf'] / max_tf))))
        self.features['h'] = (self.features['wpos'] * self.features['wrel']) / (
            self.features['wcase'] + (self.features['wfreq'] / self.features['wrel']) +
            (self.features['wspread'] / self.features['wrel']))

    @property
    def wdr(self):
        return len(self.g.out_edges(self.id))

    @property
    def wir(self):
        return sum(d['tf'] for (_, _, d) in self.g.out_edges(self.id, data=True))

    @property
    def pwr(self):
        wir = self.wir
        return 0 if wir == 0 else self.wdr / wir

    @property
    def wdl(self):
        return len(self.g.in_edges(self.id))

    @property
    def wil(self):
        return sum(d['tf'] for (_, _, d) in self.g.in_edges(self.id, data=True))

    @property
    def pwl(self):
        wil = self.wil
        return 0 if wil == 0 else self.wdl / wil

    def add_occur(self, tag, sent_id, pos_sent, pos_text):
        if sent_id not in self.occurs:
            self.occurs[sent_id] = []
        self.occurs[sent_id].append((pos_sent, pos_text))
        self.tf_stats['tf'] += 1.
        if tag == "a":
            self.tf_stats['tf_a'] += 1.
        if tag == "n":
            self.tf_stats['tf_n'] += 1.