"""
Module for highlighting text based on keywords.
Provides functionality to highlight specific keywords in text.
"""
import re
import logging
from dataclasses import dataclass
from typing import List

DEFAULT_HIGHLIGHT_PRE = "<kw>"
DEFAULT_HIGHLIGHT_POST = "</kw>"


@dataclass
class NgramData:
    """Data structure to hold n-gram processing results."""
    word_list: List[str]
    split_kw_list: List[List[str]]


class TextHighlighter:
    """
    Class for highlighting keywords in text.
    
    This class provides functionality to highlight keywords in text
    using pre-defined markers. It supports one-gram and n-gram highlighting.
    """

    def __init__(
        self,
        max_ngram_size,
        highlight_pre=DEFAULT_HIGHLIGHT_PRE,
        highlight_post=DEFAULT_HIGHLIGHT_POST,
    ):
        """
        TextHighlighter constructor. Define highlight text snippets.

        Args:
            max_ngram_size: Specifies the maximum ngram size in the keywords.
            highlight_pre: Specifies the text before a highlighted term. Defaults to <kw>.
            highlight_post: Specifies the text after a highlighted term. Defaults to </kw>.
        """
        self.highlight_pre = highlight_pre
        self.highlight_post = highlight_post
        self.max_ngram_size = max_ngram_size

    def highlight(self, text, keywords):
        """
        Highlights keywords in the given text.

        Args:
            text: The original text to be processed.
            keywords: A list of keywords to highlight.
                     Each keyword can be a string or a tuple where the first element is the keyword.
        
        Returns:
            The text with highlighted keywords.
        """
        n_text = ""
        if len(keywords) > 0:
            kw_list = keywords
            if isinstance(keywords[0], tuple):
                kw_list = [x[0] for x in keywords]
            text = text.strip()
            if self.max_ngram_size == 1:
                n_text = self.format_one_gram_text(text, kw_list)
            else:
                n_text = self.format_n_gram_text(text, kw_list)
        return n_text

    def format_one_gram_text(self, text, relevant_words_array):
        """
        Formats text for one-gram highlighting.
        
        Args:
            text: The text to process
            relevant_words_array: Keywords to highlight
            
        Returns:
            Formatted text with highlighted keywords
        """
        text_tokens = text.replace("\n", " ").split(" ")
        relevant_words_array = [kw.lower() for kw in relevant_words_array]
        try:
            for tk, token in enumerate(text_tokens):
                kw = re.sub(r'[!",:.;?()]$|^[!",:.;?()]|\W[!",:.;?()]', '', token)
                if kw.lower() in relevant_words_array:
                    text_tokens[tk] = token.replace(
                        kw, f"{self.highlight_pre}{kw}{self.highlight_post}"
                    )
        except re.error as e:
            logging.error("Regex error: %s", e)
        return " ".join(text_tokens)

    def format_n_gram_text(self, text, relevant_words_array):
        """
        Formats text for n-gram highlighting.
        
        Args:
            text: The text to process
            relevant_words_array: Keywords to highlight
            
        Returns:
            Formatted text with highlighted keywords
        """
        text_tokens = text.replace("\n", " ").split(" ")
        relevant_words_array = [kw.lower() for kw in relevant_words_array]

        y = 0
        final_splited_text = []

        while y < len(text_tokens):
            n_gram_data = self.find_relevant_ngrams(
                y, text_tokens, relevant_words_array
            )

            n_gram_word_list, splited_n_gram_kw_list = n_gram_data

            if n_gram_word_list:
                y, new_expression = self.process_ngrams(
                    text_tokens, y, n_gram_word_list,
                    splited_n_gram_kw_list, relevant_words_array, final_splited_text
                )
                final_splited_text.append(new_expression)
            else:
                final_splited_text.append(text_tokens[y])
                y += 1

        return " ".join(final_splited_text)

    def find_relevant_ngrams(self, position, text_tokens, relevant_words_array):
        """
        Finds relevant n-grams in the text.
        
        Args:
            position: Current position in text tokens
            text_tokens: List of tokens from the text
            relevant_words_array: Keywords to highlight
            
        Returns:
            Tuple containing n-gram word list and split n-gram keyword list
        """

        ngram_data = self._find_more_relevant_helper(
            position, text_tokens, relevant_words_array
        )

        return ngram_data

    def _find_more_relevant_helper(
        self, position, text_tokens, relevant_words_array
    ):
        """
        Helper method for finding relevant n-gram words.
        
        Args:
            position: Current position in text tokens
            text_tokens: List of tokens from the text
            relevant_words_array: Keywords to highlight
            
        Returns:
            NgramData containing keyword list and split n-gram word list
        """
        temporary_list = []
        temporary_list_two = []
        kw_list = []
        splited_n_gram_word_list = []

        for i in range(self.max_ngram_size):
            if position + i < len(text_tokens):
                temporary_list.append(text_tokens[position: position + i + 1])
                k = re.sub(
                    r'[!",:.;?()]$|^[!",:.;?()]|\W[!",:.;?()]', '',
                    " ".join(temporary_list[i])
                )
                if k.lower() in relevant_words_array:
                    temporary_list_two.append(k)

        if temporary_list_two:
            sorted_temp = sorted(
                temporary_list_two,
                key=lambda x: relevant_words_array.index(x.lower())
            )
            kw_list.append(sorted_temp[0])
            splited_n_gram_word_list.append(kw_list[0].split())

        return kw_list, splited_n_gram_word_list

    def process_ngrams(
        self, text_tokens, position, n_gram_word_list,
        splited_n_gram_kw_list, relevant_words_array, final_splited_text
    ):
        """
        Processes n-grams and updates the final text.
        
        Args:
            text_tokens: List of tokens from the text
            position: Current position in text tokens
            n_gram_word_list: List of n-gram words
            splited_n_gram_kw_list: List of split n-gram keywords
            relevant_words_array: Keywords to highlight
            final_splited_text: List of processed text tokens
            
        Returns:
            Tuple containing new position and new expression
        """
        if len(n_gram_word_list[0].split(" ")) == 1:
            position, new_expression = self.replace_token(
                text_tokens, position, n_gram_word_list
            )
        else:
            ctx = self._create_ngram_context(
                n_gram_word_list, splited_n_gram_kw_list,
                relevant_words_array, final_splited_text
            )
            position, new_expression = self._process_multi_word_ngrams_helper(
                text_tokens, position, ctx
            )

        return position, new_expression

    def _create_ngram_context(
        self, n_gram_word_list, splited_n_gram_kw_list,
        relevant_words_array, final_splited_text
    ):
        """
        Creates a context object for n-gram processing.
        
        Args:
            position: Current position in text tokens
            n_gram_word_list: List of n-gram words
            splited_n_gram_kw_list: List of split n-gram keywords
            relevant_words_array: Keywords to highlight
            final_splited_text: List of processed text tokens
            
        Returns:
            Dictionary with context information
        """
        return {
            "n_gram_word_list": n_gram_word_list,
            "splited_n_gram_kw_list": splited_n_gram_kw_list,
            "relevant_words_array": relevant_words_array,
            "final_splited_text": final_splited_text,
        }

    def _process_multi_word_ngrams_helper(
        self, text_tokens, position, ctx
    ):
        """
        Helper method for processing multi-word n-grams.
        
        Args:
            text_tokens: List of tokens from the text
            position: Current position in text tokens
            ctx: Context dictionary with processing information
            
        Returns:
            Tuple containing new position and new expression
        """
        kw_list = []
        n_gram_word_list = ctx["n_gram_word_list"]
        splited_n_gram_kw_list = ctx["splited_n_gram_kw_list"]
        relevant_words_array = ctx["relevant_words_array"]
        final_splited_text = ctx["final_splited_text"]

        splited_one = n_gram_word_list[0].split()

        for len_kw in range(len(splited_one)):
            if position + len_kw < len(text_tokens):
                self._update_kw_list(
                    position + len_kw, text_tokens,
                    relevant_words_array, kw_list, splited_n_gram_kw_list
                )

        if not kw_list:
            return position + 1, text_tokens[position]

        min_score_word = min(
            kw_list, key=lambda x: relevant_words_array.index(x.lower())
        )

        if kw_list.index(min_score_word) == 0:
            term_list = [min_score_word]
            position, new_expression = self.replace_token(
                text_tokens, position, term_list
            )
        else:
            terms_ctx = {
                "splited_n_gram_kw_list": splited_n_gram_kw_list,
                "min_score_word": min_score_word,
                "relevant_words_array": relevant_words_array,
                "final_splited_text": final_splited_text
            }
            position, new_expression = self._process_relevant_terms_helper(
                text_tokens, position, terms_ctx
            )

        return position, new_expression

    def _update_kw_list(self, position,
                        text_tokens, relevant_words_array, kw_list, splited_n_gram_kw_list):
        """
        Updates the keyword list and split n-gram keyword list.
        
        Args:
            position: Current position in text tokens
            text_tokens: List of tokens from the text
            relevant_words_array: Keywords to highlight
            kw_list: List of keywords
            splited_n_gram_kw_list: List of split n-gram keywords
        """
        ngram_result = self._find_more_relevant_helper(
            position, text_tokens, relevant_words_array
        )
        new_kw_list, new_split_list = ngram_result
        kw_list.extend(new_kw_list)
        if new_split_list:
            splited_n_gram_kw_list.extend(new_split_list)

    def _process_relevant_terms_helper(
        self, text_tokens, position, ctx
    ):
        """
        Helper method for processing relevant terms.
        
        Args:
            text_tokens: List of tokens from the text
            position: Current position in text tokens
            ctx: Context dictionary with processing information
            
        Returns:
            Tuple containing new position and new expression
        """
        splited_n_gram_kw_list = ctx["splited_n_gram_kw_list"]
        min_score_word = ctx["min_score_word"]
        relevant_words_array = ctx["relevant_words_array"]
        final_splited_text = ctx["final_splited_text"]

        if not splited_n_gram_kw_list:
            return position + 1, text_tokens[position]

        index_of_more_relevant = splited_n_gram_kw_list[0].index(
            min_score_word.split()[0]
        )
        temporal_kw = " ".join(
            splited_n_gram_kw_list[0][:index_of_more_relevant]
        )

        if temporal_kw.lower() in relevant_words_array:
            try:
                handle_ctx = {
                    "temporal_kw": temporal_kw,
                    "relevant_words_array": relevant_words_array,
                    "final_splited_text": final_splited_text
                }
                return self._handle_temporal_keyword(
                    text_tokens, position, handle_ctx
                )
            except ValueError as e:
                print(f"Error: {e}")
                term_list = [temporal_kw]
                position, new_expression = self.replace_token(
                    text_tokens, position, term_list
                )
        else:
            nonrelevant_ctx = {
                "splited_n_gram_kw_list": splited_n_gram_kw_list,
                "index_of_more_relevant": index_of_more_relevant,
                "relevant_words_array": relevant_words_array
            }
            position, new_expression = self._handle_nonrelevant_temporal_keyword(
                text_tokens, position, nonrelevant_ctx
            )

        return position, new_expression

    def _handle_temporal_keyword(
        self, text_tokens, position, ctx
    ):
        """
        Helper method for handling temporal keywords.
        
        Args:
            text_tokens: List of tokens from the text
            position: Current position in text tokens
            ctx: Context dictionary with processing information
            
        Returns:
            Tuple containing new position and new expression
        """
        temporal_kw = ctx["temporal_kw"]
        relevant_words_array = ctx["relevant_words_array"]
        final_splited_text = ctx["final_splited_text"]

        if not final_splited_text:
            term_list = [temporal_kw]
            return self.replace_token(text_tokens, position, term_list)

        last_item = final_splited_text[-1]
        combined_kw = f"{last_item} {temporal_kw}"

        if (combined_kw.lower() in relevant_words_array and
            relevant_words_array.index(temporal_kw.lower()) >
            relevant_words_array.index(combined_kw.lower()) and
            not re.findall(self.highlight_pre, last_item)):
            term_list = [combined_kw]
            del final_splited_text[-1]
            position -= 1
            position, new_expression = self.replace_token(
                text_tokens, position, term_list
            )
        else:
            term_list = [temporal_kw]
            position, new_expression = self.replace_token(
                text_tokens, position, term_list
            )

        return position, new_expression

    def _handle_nonrelevant_temporal_keyword(
        self, text_tokens, position, ctx
    ):
        """
        Helper method for handling non-relevant temporal keywords.
        
        Args:
            text_tokens: List of tokens from the text
            position: Current position in text tokens
            ctx: Context dictionary with processing information
            
        Returns:
            Tuple containing new position and new expression
        """
        splited_n_gram_kw_list = ctx["splited_n_gram_kw_list"]
        index_of_more_relevant = ctx["index_of_more_relevant"]
        relevant_words_array = ctx["relevant_words_array"]

        if not splited_n_gram_kw_list:
            return position + 1, text_tokens[position]

        for tmp_kw in splited_n_gram_kw_list[0][:index_of_more_relevant]:
            if tmp_kw.lower() in relevant_words_array:
                term_list = [tmp_kw]
                return self.replace_token(text_tokens, position, term_list)

        return position + 1, text_tokens[position]

    def replace_token(self, text_tokens, position, n_gram_word_list):
        """
        Replaces tokens in text with highlighted versions.
        
        Args:
            text_tokens: List of tokens from the text
            position: Current position in text tokens
            n_gram_word_list: List of n-gram words
            
        Returns:
            Tuple containing new position and new expression
        """
        if not n_gram_word_list:
            return position + 1, text_tokens[position]

        num_tokens = len(n_gram_word_list[0].split(" "))

        if position + num_tokens > len(text_tokens):
            num_tokens = len(text_tokens) - position

        txt = " ".join(text_tokens[position: position + num_tokens])
        kw_cleaned = re.sub(
            r'[!",:.;?()]$|^[!",:.;?()]|\W[!",:.;?()]', "", txt
        )
        new_expression = txt.replace(
            kw_cleaned,
            f"{self.highlight_pre}{n_gram_word_list[0]}{self.highlight_post}"
        )

        return position + num_tokens, new_expression
