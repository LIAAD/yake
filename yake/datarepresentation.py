import re
import string
import math

from segtok.segmenter import split_multi
from segtok.tokenizer import web_tokenizer, split_contractions

import networkx as nx
import numpy as np
import jellyfish

STOPWORD_WEIGHT = 'bi'

class DataCore(object):
    
    def __init__(self, text, stopword_set, windows_size, n, tags_to_discard=None, exclude=None):
        if tags_to_discard is None:
            tags_to_discard = set(['u', 'd'])
        if exclude is None:
            exclude = set(string.punctuation)
        self.number_of_sentences = 0
        self.number_of_words = 0
        self.terms = {}
        self.candidates = {}
        self.sentences_obj = []
        self.sentences_str = []
        self.G = nx.DiGraph()
        self.exclude = exclude
        self.tags_to_discard = tags_to_discard
        self.freq_ns = {}
        for i in range(n):
            self.freq_ns[i+1] = 0.
        self.stopword_set = stopword_set
        self._build(text, windows_size, n)

    def build_candidate(self, candidate_string):
        sentences_str = [w for w in split_contractions(web_tokenizer(candidate_string.lower())) if not (w.startswith("'") and len(w) > 1) and len(w) > 0]
        candidate_terms = []
        for (i, word) in enumerate(sentences_str):
            tag = self.getTag(word, i)
            term_obj = self.getTerm(word, save_non_seen=False)
            if term_obj.tf == 0:
                term_obj = None
            candidate_terms.append( (tag, word, term_obj) )
        if len([cand for cand in candidate_terms if cand[2] is not None]) == 0:
            invalid_virtual_cand = composed_word(None)
            return invalid_virtual_cand
        virtual_cand = composed_word(candidate_terms)
        return virtual_cand

    # Build the datacore features
    def _build(self, text, windows_size, n):
        text = self.pre_filter(text)
        self.sentences_str = [ [w for w in split_contractions(web_tokenizer(s)) if not (w.startswith("'") and len(w) > 1) and len(w) > 0] for s in list(split_multi(text)) if len(s.strip()) > 0]
        self.number_of_sentences = len(self.sentences_str)
        pos_text = 0
        block_of_word_obj = []
        sentence_obj_aux = []
        for (sentence_id, sentence) in enumerate(self.sentences_str):
            sentence_obj_aux = []
            block_of_word_obj = []
            for (pos_sent, word) in enumerate(sentence):
                if len([c for c in word if c in self.exclude]) == len(word): # If the word is based on exclude chars
                    if len(block_of_word_obj) > 0:
                        sentence_obj_aux.append( block_of_word_obj )
                        block_of_word_obj = []
                else:
                    tag = self.getTag(word, pos_sent)
                    term_obj = self.getTerm(word)
                    term_obj.add_occur(tag, sentence_id, pos_sent, pos_text)
                    pos_text += 1

                    #Create co-occurrence matrix
                    if tag not in self.tags_to_discard:
                        word_windows = list(range( max(0, len(block_of_word_obj)-windows_size), len(block_of_word_obj) ))
                        for w in word_windows:
                            if block_of_word_obj[w][0] not in self.tags_to_discard: 
                                self.addCooccur(block_of_word_obj[w][2], term_obj)
                    #Generate candidate keyphrase list
                    candidate = [ (tag, word, term_obj) ]
                    cand = composed_word(candidate)
                    self.addOrUpdateComposedWord(cand)
                    word_windows = list(range( max(0, len(block_of_word_obj)-(n-1)), len(block_of_word_obj) ))[::-1]
                    for w in word_windows:
                        candidate.append(block_of_word_obj[w])
                        self.freq_ns[len(candidate)] += 1.
                        cand = composed_word(candidate[::-1])
                        self.addOrUpdateComposedWord(cand)

                    # Add term to the block of words' buffer
                    block_of_word_obj.append( (tag, word, term_obj) )

            if len(block_of_word_obj) > 0:
                sentence_obj_aux.append( block_of_word_obj )

            if len(sentence_obj_aux) > 0:
                self.sentences_obj.append(sentence_obj_aux)

        if len(block_of_word_obj) > 0:
            sentence_obj_aux.append( block_of_word_obj )

        if len(sentence_obj_aux) > 0:
            self.sentences_obj.append(sentence_obj_aux)

        self.number_of_words = pos_text

    def build_single_terms_features(self, features=None):
        valid_terms = [ term for term in self.terms.values() if not term.stopword ]
        valid_tfs = (np.array([ x.tf for x in valid_terms ]))

        if len(valid_tfs) == 0:
            return

        avgTF = valid_tfs.mean()
        stdTF = valid_tfs.std()
        maxTF = max([ x.tf for x in self.terms.values()])
        list(map(lambda x: x.updateH(maxTF=maxTF, avgTF=avgTF, stdTF=stdTF, number_of_sentences=self.number_of_sentences, features=features), self.terms.values()))

    def build_mult_terms_features(self, features=None):
        list(map(lambda x: x.updateH(features=features), [cand for cand in self.candidates.values() if cand.isValid()]))

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

    def getTag(self, word, i):
        try:
            w2 = word.replace(",","")
            float(w2)
            return "d"
        except ValueError:
            cdigit = len([c for c in word if c.isdigit()])
            calpha = len([c for c in word if c.isalpha()])
            if ( cdigit > 0 and calpha > 0 ) or (cdigit == 0 and calpha == 0) or len(
                [c for c in word if c in self.exclude]) > 1:
                return "u"
            if len(word) == len([c for c in word if c.isupper()]):
                return "a"
            if (len([c for c in word if c.isupper()]) == 1 and len(word) > 1 and 
                word[0].isupper() and i > 0):
                return "n"
        return "p"

    def getTerm(self, str_word, save_non_seen=True):
        unique_term = str_word.lower()
        simples_sto = unique_term in self.stopword_set
        if unique_term.endswith('s') and len(unique_term) > 3:
            unique_term = unique_term[:-1]

        if unique_term in self.terms:
            return self.terms[unique_term]
                
        # Include this part
        simples_unique_term = unique_term
        for pontuation in self.exclude:
            simples_unique_term = simples_unique_term.replace(pontuation, '')
        # until here
        isstopword = simples_sto or unique_term in self.stopword_set or len(simples_unique_term) < 3
        
        term_id = len(self.terms)
        term_obj = single_word(unique_term, term_id, self.G)
        term_obj.stopword = isstopword

        if save_non_seen:
            self.G.add_node(term_id)
            self.terms[unique_term] = term_obj

        return term_obj

    def addCooccur(self, left_term, right_term):
        if right_term.id not in self.G[left_term.id]:
            self.G.add_edge(left_term.id, right_term.id, TF=0.)
        self.G[left_term.id][right_term.id]["TF"]+=1.
        
    def addOrUpdateComposedWord(self, cand):
        if cand.unique_kw not in self.candidates:
            self.candidates[cand.unique_kw] = cand
        else:
            self.candidates[cand.unique_kw].uptadeCand(cand)
        self.candidates[cand.unique_kw].tf += 1.


class composed_word(object):
    def __init__(self, terms): # [ (tag, word, term_obj) ]
        if terms is None:
            self.start_or_end_stopwords = True
            self.tags = set()
            return
        self.tags = set([''.join([ w[0] for w in terms ])])
        self.kw = ' '.join( [ w[1] for w in terms ] )
        self.unique_kw = self.kw.lower()
        self.size = len(terms)
        self.terms = [ w[2] for w in terms if w[2] != None ]
        self.tf = 0.
        self.integrity = 1.
        self.h = 1.
        self.start_or_end_stopwords = self.terms[0].stopword or self.terms[-1].stopword

    def uptadeCand(self, cand):
        for tag in cand.tags:
            self.tags.add( tag )

    def isValid(self):
        isValid = False
        for tag in self.tags:
            isValid = isValid or ( "u" not in tag and "d" not in tag )
        return isValid and not self.start_or_end_stopwords

    def get_composed_feature(self, feature_name, discart_stopword=True):
        list_of_features = [ getattr(term, feature_name) for term in self.terms if ( discart_stopword and not term.stopword ) or not discart_stopword ]
        sum_f = sum(list_of_features)
        prod_f = np.prod(list_of_features)
        return (sum_f, prod_f, prod_f / (sum_f + 1))

    def build_features(
        self,
        doc_id = None,
        keys = None,
        rel = True,
        rel_approx = True,
        isVirtual = False,
        features = None,
        _stopword = None,
        ):
        if features is None:
            features = ['WFreq', 'WRel', 'tf', 'WCase', 'WPos', 'WSpread']
        if _stopword is None:
            _stopword = [True, False]
        columns = []
        seen = set()
        features_cand = []

        if doc_id is not None:
            columns.append('doc_id')
            features_cand.append(doc_id)

        if keys is not None:
            if rel:
                columns.append('rel')
                if self.unique_kw in keys or isVirtual:
                    features_cand.append(1)
                    seen.add(self.unique_kw)
                else:
                    features_cand.append(0)

            if rel_approx:
                columns.append('rel_approx')
                max_gold_ = ('', 0.)
                for gold_key in keys:
                    dist = 1.-jellyfish.levenshtein_distance(gold_key, self.unique_kw) / max(len(gold_key), len(self.unique_kw)) # _tL
                    if max_gold_[1] < dist:
                        max_gold_ = ( gold_key, dist )
                features_cand.append(max_gold_[1])

        columns.append('kw')
        features_cand.append(self.unique_kw)
        columns.append('h')
        features_cand.append(self.h)
        columns.append('tf')
        features_cand.append(self.tf)
        columns.append('size')
        features_cand.append(self.size)
        columns.append('isVirtual')
        features_cand.append(int(isVirtual))

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

    def updateH(self, features=None, isVirtual=False):
        sum_h  = 0.
        prod_h = 1.

        for (t, term_base) in enumerate(self.terms):
            if not term_base.stopword:
                sum_h += term_base.h
                prod_h *= term_base.h

            else:
                if STOPWORD_WEIGHT == 'bi':
                    prob_t1 = 0.
                    if t > 0 and term_base.G.has_edge(
                        self.terms[t-1].id, self.terms[t].id):
                        prob_t1 = term_base.G[
                            self.terms[t-1].id][self.terms[t].id]["TF"] / self.terms[t-1].tf                 
                    prob_t2 = 0.
                    if t < len(self.terms) - 1 and term_base.G.has_edge(
                        self.terms[t].id, self.terms[t+1].id):
                        prob_t2 = term_base.G[
                            self.terms[t].id][self.terms[t+1].id]["TF"] / self.terms[t+1].tf

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

        if isVirtual:
            tf_used = np.mean( [term_obj.tf for term_obj in self.terms] )

        self.h = prod_h / ( ( sum_h + 1 ) * tf_used )

    def updateH_old(self, features=None, isVirtual=False):
        sum_h  = 0.
        prod_h = 1.

        for (t, term_base) in enumerate(self.terms):
            if isVirtual and term_base.tf==0:
                continue

            if term_base.stopword:
                prob_t1 = 0.
                if term_base.G.has_edge(self.terms[t-1].id, self.terms[ t ].id):
                    prob_t1 = term_base.G[
                        self.terms[t-1].id][self.terms[ t ].id]["TF"] / self.terms[t-1].tf

                prob_t2 = 0.
                if term_base.G.has_edge(self.terms[ t ].id, self.terms[t+1].id):
                    prob_t2 = term_base.G[
                        self.terms[ t ].id][self.terms[t+1].id]["TF"] / self.terms[t+1].tf

                prob = prob_t1 * prob_t2
                prod_h *= (1 + (1 - prob ) )
                sum_h -= (1 - prob)
            else:
                sum_h += term_base.h
                prod_h *= term_base.h
        tf_used = 1.
        if features is None or "KPF" in features:
            tf_used = self.tf
        if isVirtual:
            tf_used = np.mean( [term_obj.tf for term_obj in self.terms] )
        self.h = prod_h / ( ( sum_h + 1 ) * tf_used )


class single_word(object):

    def __init__(self, unique, idx, graph):
        self.unique_term = unique
        self.id = idx
        self.tf = 0.
        self.WFreq = 0.0
        self.WCase = 0.0
        self.tf_a = 0.
        self.tf_n = 0.
        self.WRel = 1.0
        self.PL = 0.
        self.PR = 0.
        self.occurs = {}
        self.WPos = 1.0
        self.WSpread = 0.0
        self.h = 0.0
        self.stopword = False
        self.G = graph

        self.pagerank = 1.

    def updateH(self, maxTF, avgTF, stdTF, number_of_sentences, features=None):
        """if features == None or "WRel" in features:
            self.PL = self.WDL / maxTF
            self.PR = self.WDR / maxTF
            self.WRel = ( (0.5 + (self.PWL * (self.tf / maxTF) + self.PL)) + (0.5 + (self.PWR * (self.tf / maxTF) + self.PR)) )"""

        if features is None or "WRel" in features:
            self.PL = self.WDL / maxTF
            self.PR = self.WDR / maxTF
            self.WRel = (
                (0.5 + (self.PWL * (self.tf / maxTF))) +
                (0.5 + (self.PWR * (self.tf / maxTF)))
            )

        if features is None or "WFreq" in features:
            self.WFreq = self.tf / (avgTF + stdTF)
        
        if features is None or "WSpread" in features:
            self.WSpread = len(self.occurs) / number_of_sentences
        
        if features is None or "WCase" in features:
            self.WCase = max(self.tf_a, self.tf_n) / (1. + math.log(self.tf))
        
        if features is None or "WPos" in features:
            self.WPos = math.log( math.log( 3. + np.median(list(self.occurs.keys())) ) )

        self.h = (self.WPos * self.WRel) / (self.WCase + (self.WFreq / self.WRel) + (self.WSpread / self.WRel))
        
    @property
    def WDR(self):
        return len( self.G.out_edges(self.id) )

    @property
    def WIR(self):
        return sum( [ d['TF'] for (u,v,d) in self.G.out_edges(self.id, data=True) ] )

    @property
    def PWR(self):
        wir = self.WIR
        if wir == 0:
            return 0
        return self.WDR / wir
   
    @property
    def WDL(self):
        """
        Calculate the number of incoming edges for the node.

        Returns:
            int: The number of incoming edges for the node.
        """
        return len( self.G.in_edges(self.id) )

    @property
    def WIL(self):
        """
        Calculate the sum of term frequencies for incoming edges.
        """
        return sum(d['TF'] for (_, _, d) in self.G.in_edges(self.id, data=True))

    @property
    def PWL(self):
        WIL = self.WIL
        if WIL == 0:
            return 0
        return self.WDL / WIL

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
