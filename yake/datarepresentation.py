import re
import string
import math
import jellyfish

from segtok.segmenter import split_multi
from segtok.tokenizer import web_tokenizer, split_contractions

import networkx as nx
import numpy as np

STOPWORD_WEIGHT = 'bi'

class WordProcessingContext:
    """Helper class to encapsulate word processing parameters"""
    def __init__(self, word, pos_sent, sentence_id, pos_text, block_of_word_obj):
        self.word = word
        self.pos_sent = pos_sent
        self.sentence_id = sentence_id
        self.pos_text = pos_text
        self.block_of_word_obj = block_of_word_obj

    def get_word_info(self):
        """Returns a dictionary with word information"""
        return {
            'word': self.word,
            'position_in_sentence': self.pos_sent,
            'sentence_id': self.sentence_id,
            'position_in_text': self.pos_text
        }

    def append_to_block(self, tag, term_obj):
        """Adds a processed word to the block of word objects"""
        self.block_of_word_obj.append((tag, self.word, term_obj))


class SentenceProcessingContext:
    """Helper class to encapsulate sentence processing parameters"""
    def __init__(self, sentence, sentence_id, pos_text):
        self.sentence = sentence
        self.sentence_id = sentence_id
        self.pos_text = pos_text
        self.sentence_obj_aux = []
        self.block_of_word_obj = []

    def clear_block(self):
        """Clears the current block and adds it to sentence objects if not empty"""
        if len(self.block_of_word_obj) > 0:
            self.sentence_obj_aux.append(self.block_of_word_obj)
            self.block_of_word_obj = []

    def get_sentence_info(self):
        """Returns a dictionary with sentence information"""
        return {
            'sentence': self.sentence,
            'sentence_id': self.sentence_id,
            'word_count': len(self.sentence),
            'processed_blocks': len(self.sentence_obj_aux)
        }

class DataCore():
    def __init__(self, text, stopword_set, windows_size, n, tags_to_discard=None, exclude=None):
        if tags_to_discard is None:
            tags_to_discard = set(['u', 'd'])
        if exclude is None:
            exclude = set(string.punctuation)
        # Group text analysis stats
        self.stats = {
            'number_of_sentences': 0,
            'number_of_words': 0,
            'freq_ns': {i+1: 0. for i in range(n)}
        }
        # Group text components
        self.components = {
            'terms': {},
            'candidates': {},
            'sentences_obj': [],
            'sentences_str': []
        }
        # Group configuration parameters
        self.config = {
            'g': nx.DiGraph(),
            'exclude': exclude,
            'tags_to_discard': tags_to_discard,
            'stopword_set': stopword_set
        }
        # Build the core data structures
        self._build(text, windows_size, n)

    # Properties to maintain backwards compatibility
    @property
    def number_of_sentences(self):
        return self.stats['number_of_sentences']
    @property
    def number_of_words(self):
        return self.stats['number_of_words']
    @property
    def terms(self):
        return self.components['terms']
    @property
    def candidates(self):
        return self.components['candidates']
    @property
    def sentences_obj(self):
        return self.components['sentences_obj']
    @property
    def sentences_str(self):
        return self.components['sentences_str']
    @property
    def g(self):
        return self.config['g']
    @property
    def exclude(self):
        return self.config['exclude']
    @property
    def tags_to_discard(self):
        return self.config['tags_to_discard']
    @property
    def freq_ns(self):
        return self.stats['freq_ns']
    @property
    def stopword_set(self):
        return self.config['stopword_set']
    def build_candidate(self, candidate_string):
        sentences_str = [w for w in split_contractions(
            web_tokenizer(candidate_string.lower())) if not
                        (w.startswith("'") and len(w) > 1) and len(w) > 0]
        candidate_terms = []
        for (i, word) in enumerate(sentences_str):
            tag = self.get_tag(word, i)
            term_obj = self.get_term(word, save_non_seen=False)
            if term_obj.tf == 0:
                term_obj = None
            candidate_terms.append( (tag, word, term_obj) )
        if len([cand for cand in candidate_terms if cand[2] is not None]) == 0:
            invalid_virtual_cand = ComposedWord(None)
            return invalid_virtual_cand
        virtual_cand = ComposedWord(candidate_terms)
        return virtual_cand

    # Build the datacore features
    def _build(self, text, windows_size, n):
        text = self.pre_filter(text)
        self.components['sentences_str'] = self.tokenize_sentences(text)
        self.stats['number_of_sentences'] = len(self.components['sentences_str'])
        pos_text = 0
        for sentence_id, sentence in enumerate(self.components['sentences_str']):
            # Create sentence context object
            context = SentenceProcessingContext(sentence, sentence_id, pos_text)
            pos_text = self.process_sentence(context, windows_size, n)
        self.stats['number_of_words'] = pos_text

    def tokenize_sentences(self, text):
        return [[
            w for w in split_contractions(web_tokenizer(s)) if not (
                w.startswith("'") and len(w) > 1) and len(w) > 0] for s in
                list(split_multi(text)) if len(s.strip()) > 0]

    def process_sentence(self, context, windows_size, n):
        """Process a sentence using the context object and configuration parameters"""
        for pos_sent, word in enumerate(context.sentence):
            if len([c for c in word if c in self.config['exclude']]) == len(word):
                context.clear_block()
            else:
                # Create word context object
                word_context = WordProcessingContext(
                    word, pos_sent, context.sentence_id, context.pos_text, context.block_of_word_obj
                )
                context.pos_text = self.process_word(word_context, windows_size, n)

        # Make sure we handle any remaining blocks
        context.clear_block()

        if len(context.sentence_obj_aux) > 0:
            self.components['sentences_obj'].append(context.sentence_obj_aux)

        return context.pos_text

    def process_word(self, context, windows_size, n):
        """Process a word using the context object and configuration parameters"""
        tag = self.get_tag(context.word, context.pos_sent)
        term_obj = self.get_term(context.word)
        term_obj.add_occur(tag, context.sentence_id, context.pos_sent, context.pos_text)
        context.pos_text += 1

        if tag not in self.config['tags_to_discard']:
            self.update_cooccurrence(context.block_of_word_obj, term_obj, windows_size)
   
        self.generate_candidates((tag, context.word), term_obj, context.block_of_word_obj, n)

        # Use the new method to append to block
        context.append_to_block(tag, term_obj)

        return context.pos_text

    def update_cooccurrence(self, block_of_word_obj, term_obj, windows_size):
        word_windows = list(
            range(max(0, len(block_of_word_obj) - windows_size), len(block_of_word_obj)))
        for w in word_windows:
            if block_of_word_obj[w][0] not in self.config['tags_to_discard']:
                self.add_cooccur(block_of_word_obj[w][2], term_obj)

    def generate_candidates(self, term, term_obj, block_of_word_obj, n):
        candidate = [term + (term_obj,)]
        cand = ComposedWord(candidate)
        self.add_or_update_composedword(cand)
        word_windows = list(
            range(max(0, len(block_of_word_obj) - (n - 1)), len(block_of_word_obj)))[::-1]
        for w in word_windows:
            candidate.append(block_of_word_obj[w])
            self.stats['freq_ns'][len(candidate)] += 1.
            cand = ComposedWord(candidate[::-1])
            self.add_or_update_composedword(cand)

    def build_single_terms_features(self, features=None):
        valid_terms = [term for term in self.components['terms'].values() if not term.stopword]
        valid_tfs = np.array([x.tf for x in valid_terms])

        if len(valid_tfs) == 0:
            return

        avg_tf = valid_tfs.mean()
        std_tf = valid_tfs.std()
        max_tf = max(x.tf for x in self.components['terms'].values())
        stats = {
            'max_tf': max_tf,
            'avg_tf': avg_tf,
            'std_tf': std_tf,
            'number_of_sentences': self.stats['number_of_sentences']
        }
        list(map(lambda x: x.update_h(stats, features=features), self.components['terms'].values()))

    def build_mult_terms_features(self, features=None):
        list(map(lambda x: x.update_h(features=features),
                [cand for cand in self.components['candidates'].values() if cand.is_valid()]))

    def pre_filter(self, text):
        prog = re.compile("^(\\s*([A-Z]))")
        parts = text.split('\n')
        buffer = ''
        for part in parts:
            sep = ' '
            if prog.match(part):
                sep = '\n\n'
            buffer += sep + part.replace('\t',' ')
        return buffer

    def get_tag(self, word, i):
        try:
            w2 = word.replace(",","")
            float(w2)
            return "d"
        except ValueError:
            cdigit = len([c for c in word if c.isdigit()])
            calpha = len([c for c in word if c.isalpha()])
            if ( cdigit > 0 and calpha > 0 ) or (cdigit == 0 and calpha == 0) or len(
                [c for c in word if c in self.config['exclude']]) > 1:
                return "u"
            if len(word) == len([c for c in word if c.isupper()]):
                return "a"
            if (len([c for c in word if c.isupper()]) == 1 and len(word) > 1 and
                word[0].isupper() and i > 0):
                return "n"
        return "p"

    def get_term(self, str_word, save_non_seen=True):
        unique_term = str_word.lower()
        simples_sto = unique_term in self.config['stopword_set']
        if unique_term.endswith('s') and len(unique_term) > 3:
            unique_term = unique_term[:-1]

        if unique_term in self.components['terms']:
            return self.components['terms'][unique_term]


        simples_unique_term = unique_term
        for pontuation in self.config['exclude']:
            simples_unique_term = simples_unique_term.replace(pontuation, '')
        isstopword = simples_sto or unique_term in self.config[
            'stopword_set'] or len(simples_unique_term) < 3

        term_id = len(self.components['terms'])
        term_obj = SingleWord(unique_term, term_id, self.config['g'])
        term_obj.stopword = isstopword

        if save_non_seen:
            self.config['g'].add_node(term_id)
            self.components['terms'][unique_term] = term_obj

        return term_obj

    def add_cooccur(self, left_term, right_term):
        if right_term.id not in self.config['g'][left_term.id]:
            self.config['g'].add_edge(left_term.id, right_term.id, tf=0.)
        self.config['g'][left_term.id][right_term.id]["tf"] += 1.

    def add_or_update_composedword(self, cand):
        if cand.unique_kw not in self.components['candidates']:
            self.components['candidates'][cand.unique_kw] = cand
        else:
            self.components['candidates'][cand.unique_kw].uptade_cand(cand)
        self.components['candidates'][cand.unique_kw].tf += 1.


class ComposedWord():
    def __init__(self, terms): # [ (tag, word, term_obj) ]
        if terms is None:
            self.start_or_end_stopwords = True
            self.tags = set()
            return
        self.tags = set([''.join([ w[0] for w in terms ])])
        self.kw = ' '.join( [ w[1] for w in terms ] )
        self.unique_kw = self.kw.lower()
        self.size = len(terms)
        self.terms = [ w[2] for w in terms if w[2] is not None ]
        self.tf = 0.
        self.integrity = 1.
        self.h = 1.
        self.start_or_end_stopwords = self.terms[0].stopword or self.terms[-1].stopword

    def uptade_cand(self, cand):
        for tag in cand.tags:
            self.tags.add( tag )

    def is_valid(self):
        is_valid = False
        for tag in self.tags:
            is_valid = is_valid or ( "u" not in tag and "d" not in tag )
        return is_valid and not self.start_or_end_stopwords

    def get_composed_feature(self, feature_name, discart_stopword=True):
        list_of_features = [ getattr(term, feature_name) for term in self.terms
                            if ( discart_stopword and not term.stopword ) or not discart_stopword ]
        sum_f = sum(list_of_features)
        prod_f = np.prod(list_of_features)
        return (sum_f, prod_f, prod_f / (sum_f + 1))

    def build_features(self, params):
        """
        Build features for the composed word.

        Args:
            params (dict): Dictionary containing the following keys:
                - doc_id (optional): Document ID.
                - keys (optional): List of keys.
                - rel (optional): Boolean indicating relevance.
                - rel_approx (optional): Boolean indicating approximate relevance.
        """
        features = params.get('features', ['wfreq', 'wrel', 'tf', 'wcase', 'wpos', 'wspread'])
        _stopword = params.get('_stopword', [True, False])
        if features is None:
            features = ['wfreq', 'wrel', 'tf', 'wcase', 'wpos', 'wspread']
        if _stopword is None:
            _stopword = [True, False]
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
                max_gold_ = ('', 0.)
                for gold_key in params['keys']:
                    dist = 1.-jellyfish.levenshtein_distance(
                        gold_key, self.unique_kw) / max(len(gold_key), len(self.unique_kw)) # _tL
                    max_gold_ = ( gold_key, dist )
                features_cand.append(max_gold_[1])
                features_cand.append(max_gold_[1])

        columns.append('kw')
        features_cand.append(self.unique_kw)
        columns.append('h')
        features_cand.append(self.h)
        columns.append('tf')
        features_cand.append(self.tf)
        columns.append('size')
        features_cand.append(self.size)
        columns.append('is_virtual')
        columns.append('is_virtual')
        features_cand.append(int(params.get('is_virtual', False)))
        for feature_name in features:

            for discart_stopword in _stopword:
                (f_sum, f_prod, f_sum_prod) = self.get_composed_feature(
                    feature_name, discart_stopword=discart_stopword)
                columns.append(f"{'n' if discart_stopword else ''}s_sum_K{feature_name}")
                features_cand.append(f_sum)

                columns.append(f"{'n' if discart_stopword else ''}s_prod_K{feature_name}")
                features_cand.append(f_prod)

                columns.append(f"{'n' if discart_stopword else ''}s_sum_prod_K{feature_name}")
                features_cand.append(f_sum_prod)

        return (features_cand, columns, seen)

    def update_h(self, features=None, is_virtual=False):
        sum_h  = 0.
        prod_h = 1.

        for (t, term_base) in enumerate(self.terms):
            if not term_base.stopword:
                sum_h += term_base.h
                prod_h *= term_base.h

            else:
                if STOPWORD_WEIGHT == 'bi':
                    prob_t1 = 0.
                    if t > 0 and term_base.g.has_edge(
                        self.terms[t-1].id, self.terms[t].id):
                        prob_t1 = term_base.g[
                            self.terms[t-1].id][self.terms[t].id]["tf"] / self.terms[t-1].tf
                    prob_t2 = 0.
                    if t < len(self.terms) - 1 and term_base.g.has_edge(
                        self.terms[t].id, self.terms[t+1].id):
                        prob_t2 = term_base.g[
                            self.terms[t].id][self.terms[t+1].id]["tf"] / self.terms[t+1].tf

                    prob = prob_t1 * prob_t2
                    prod_h *= (1 + (1 - prob ) )
                    sum_h -= (1 - prob)
                elif STOPWORD_WEIGHT == 'h':
                    sum_h += term_base.h
                    prod_h *= term_base.h
                elif STOPWORD_WEIGHT == 'none':
                    pass

        tf_used = 1.
        if features is None or "KPF" in features:
            tf_used = self.tf

        if is_virtual:
            tf_used = np.mean( [term_obj.tf for term_obj in self.terms] )

        self.h = prod_h / ( ( sum_h + 1 ) * tf_used )

    def update_h_old(self, features=None, is_virtual=False):
        sum_h  = 0.
        prod_h = 1.

        for (t, term_base) in enumerate(self.terms):
            if is_virtual and term_base.tf==0:
                continue

            if term_base.stopword:
                prob_t1 = 0.
                if term_base.g.has_edge(self.terms[t-1].id, self.terms[ t ].id):
                    prob_t1 = term_base.g[
                        self.terms[t-1].id][self.terms[ t ].id]["tf"] / self.terms[t-1].tf

                prob_t2 = 0.
                if term_base.g.has_edge(self.terms[ t ].id, self.terms[t+1].id):
                    prob_t2 = term_base.g[
                        self.terms[ t ].id][self.terms[t+1].id]["tf"] / self.terms[t+1].tf

                prob = prob_t1 * prob_t2
                prod_h *= (1 + (1 - prob ) )
                sum_h -= (1 - prob)
            else:
                sum_h += term_base.h
                prod_h *= term_base.h
        tf_used = 1.
        if features is None or "KPF" in features:
            tf_used = self.tf
        if is_virtual:
            tf_used = np.mean( [term_obj.tf for term_obj in self.terms] )
        self.h = prod_h / ( ( sum_h + 1 ) * tf_used )


class SingleWord():

    def __init__(self, unique, idx, graph):
        self.unique_term = unique
        self.id = idx
        self.tf = 0.
        self.wfreq = 0.0
        self.wcase = 0.0
        self.tf_a = 0.
        self.tf_n = 0.
        self.wrel = 1.0
        self.pl = 0.
        self.pr = 0.
        self.occurs = {}
        self.wpos = 1.0
        self.wspread = 0.0
        self.h = 0.0
        self.stopword = False
        self.g = graph

        self.pagerank = 1.

    def update_h(self, stats, features=None):
        """if features is None or "wrel" in features:
            self.pl = self.wdl / max_tf
            self.pr = self.wdr / max_tf
            self.wrel = ( (0.5 + (self.pwl * (self.tf / max_tf) + self.pl)) +(0.5 + (
                self.pwr * (self.tf / max_tf) + self.pr)) )"""

        max_tf = stats['max_tf']
        avg_tf = stats['avg_tf']
        std_tf = stats['std_tf']
        number_of_sentences = stats['number_of_sentences']

        if features is None or "wrel" in features:
            self.pl = self.wdl / max_tf
            self.pr = self.wdr / max_tf
            self.wrel = (
                (0.5 + (self.pwl * (self.tf / max_tf))) +
                (0.5 + (self.pwr * (self.tf / max_tf)))
            )

        if features is None or "wfreq" in features:
            self.wfreq = self.tf / (avg_tf + std_tf)

        if features is None or "wspread" in features:
            self.wspread = len(self.occurs) / number_of_sentences

        if features is None or "wcase" in features:
            self.wcase = max(self.tf_a, self.tf_n) / (1. + math.log(self.tf))

        if features is None or "wpos" in features:
            self.wpos = math.log( math.log( 3. + np.median(list(self.occurs.keys())) ) )

        self.h = (self.wpos * self.wrel) / (
            self.wcase + (self.wfreq / self.wrel) + (self.wspread / self.wrel))

    @property
    def wdr(self):
        return len( self.g.out_edges(self.id) )

    @property
    def wir(self):
        return sum(d['tf'] for (_, _, d) in self.g.out_edges(self.id, data=True))

    @property
    def pwr(self):
        wir = self.wir
        if wir == 0:
            return 0
        return self.wdr / wir

    @property
    def wdl(self):
        """
        Calculate the number of incoming edges for the node.

        Returns:
            int: The number of incoming edges for the node.
        """
        return len( self.g.in_edges(self.id) )

    @property
    def wil(self):
        """
        Calculate the sum of term frequencies for incoming edges.
        """
        return sum(d['tf'] for (_, _, d) in self.g.in_edges(self.id, data=True))

    @property
    def pwl(self):
        wil = self.wil
        if wil == 0:
            return 0
        return self.wdl / wil

    def add_occur(self, tag, sent_id, pos_sent, pos_text):
        """
        Adds an occurrence of a tag in a sentence to the internal data structure.
        Args:
            tag (str): The tag associated with the occurrence (e.g., 'a' or 'n').
            sent_id (int): The ID of the sentence where the occurrence is found.
            pos_sent (int): The position of the occurrence within the sentence.
            pos_text (int): The position of the occurrence within the entire text.
        Updates:
            self.occurs (dict): Adds the occurrence position to the list for the given sentence ID.
            self.tf (float): Increments the term frequency counter.
            self.tf_a (float): Increments the term frequency counter for tag 'a' if applicable.
            self.tf_n (float): Increments the term frequency counter for tag 'n' if applicable.
        """
        if sent_id not in self.occurs:
            self.occurs[sent_id] = []

        self.occurs[sent_id].append( (pos_sent, pos_text) )
        self.tf += 1.

        if tag == "a":
            self.tf_a += 1.
        if tag == "n":
            self.tf_n += 1.