import re

DEFAULT_HIGHLIGHT_PRE = "<kw>"
DEFAULT_HIGHLIGHT_POST = "</kw>"


class TextHighlighter:
    def __init__(
        self,
        max_ngram_size,
        highlight_pre=DEFAULT_HIGHLIGHT_PRE,
        highlight_post=DEFAULT_HIGHLIGHT_POST,
    ):
        """
        TextHighlighter constructor. Define highlight text snippets.

        :max_ngram_size - Specifies the maximum ngram size in the keywords.
        :highlight_pre – Specifies the text before a highlighted term. Defaults to <kw>.
        :highlight_post – Specifies the text after a highlighted term. Defaults to </kw>.
        """
        self.highlight_pre = highlight_pre
        self.highlight_post = highlight_post
        self.max_ngram_size = max_ngram_size

    def highlight(self, text, keywords):
        """
        Highlights keywords in the given text.

        :param text: The original text to be processed.
        :param keywords: A list of keywords to highlight. Each keyword can be a string or a tuple where the first element is the keyword.
        :return: The text with highlighted keywords.
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
                n_text = self.format_n_gram_text(text, kw_list, self.max_ngram_size)
        return n_text

    def format_one_gram_text(self, text, relevant_words_array):
        """Formats text for one-gram highlighting."""
        text_tokens = text.replace("\n", " ").split(" ")
        relevant_words_array = [kw.lower() for kw in relevant_words_array]
        try:
            for tk in range(len(text_tokens)):
                kw = re.sub(
                    r'[!",:.;?()]$|^[!",:.;?()]|\W[!",:.;?()]', '', text_tokens[tk]
                )
                if kw.lower() in relevant_words_array:
                    text_tokens[tk] = text_tokens[tk].replace(
                        kw, f"{self.highlight_pre}{kw}{self.highlight_post}"
                    )
        except re.error as e:
            import logging
            logging.error(f"Regex error: {e}")
        return " ".join(text_tokens)

    def format_n_gram_text(self, text, relevant_words_array, n_gram):
        """Formats text for n-gram highlighting."""
        text_tokens = text.replace("\n", " ").split(" ")
        relevant_words_array = [kw.lower() for kw in relevant_words_array]

        y = 0
        final_splited_text = []

        while y < len(text_tokens):
            splited_n_gram_kw_list = []
            n_gram_kw_list = []
            n_gram_word_list, splited_n_gram_kw_list = self.find_more_relevant(
                y, text_tokens, n_gram, relevant_words_array, n_gram_kw_list, splited_n_gram_kw_list
            )

            if n_gram_word_list:
                if len(n_gram_word_list[0].split(" ")) == 1:
                    y, new_expression = self.replace_token(
                        text_tokens, y, n_gram_word_list
                    )
                    final_splited_text.append(new_expression)
                else:
                    kw_list = []
                    splited_n_gram_kw_list = []
                    splited_one = n_gram_word_list[0].split()

                    for len_kw in range(len(splited_one)):
                        kw_list, splited_n_gram_kw_list = self.find_more_relevant(
                            y + len_kw, text_tokens, n_gram,
                            relevant_words_array, kw_list, splited_n_gram_kw_list
                        )

                    min_score_word = min(
                        kw_list, key=lambda x: relevant_words_array.index(x.lower())
                    )

                    if kw_list.index(min_score_word) == 0:
                        term_list = [min_score_word]
                        y, new_expression = self.replace_token(
                            text_tokens, y, term_list
                        )
                        final_splited_text.append(new_expression)
                    elif kw_list.index(min_score_word) >= 1:
                        index_of_more_relevant = splited_n_gram_kw_list[0].index(
                            min_score_word.split()[0]
                        )
                        temporal_kw = " ".join(
                            splited_n_gram_kw_list[0][:index_of_more_relevant]
                        )

                        if temporal_kw in relevant_words_array:
                            try:
                                last_item = final_splited_text[-1]
                                combined_kw = f"{last_item} {temporal_kw}"
                                if (
                                    relevant_words_array.index(temporal_kw)
                                    > relevant_words_array.index(combined_kw)
                                    and not re.findall(self.highlight_pre, last_item)
                                ):
                                    term_list = [combined_kw]
                                    del final_splited_text[-1]
                                    y -= 1
                                    y, new_expression = self.replace_token(
                                        text_tokens, y, term_list
                                    )
                                    final_splited_text.append(new_expression)
                                else:
                                    term_list = [temporal_kw]
                                    y, new_expression = self.replace_token(
                                        text_tokens, y, term_list
                                    )
                                    final_splited_text.append(new_expression)
                            except Exception as e:
                                print(f"Error: {e}")
                                term_list = [temporal_kw]
                                y, new_expression = self.replace_token(
                                    text_tokens, y, term_list
                                )
                                final_splited_text.append(new_expression)
                        else:
                            for tmp_kw in splited_n_gram_kw_list[0][:index_of_more_relevant]:
                                if tmp_kw in relevant_words_array:
                                    term_list = [tmp_kw]
                                    y, new_expression = self.replace_token(
                                        text_tokens, y, term_list
                                    )
                                    final_splited_text.append(new_expression)
                                else:
                                    final_splited_text.append(text_tokens[y])
                                    y += 1
            else:
                final_splited_text.append(text_tokens[y])
                y += 1

        return " ".join(final_splited_text)

    def find_more_relevant(
        self, y, text_tokens, n_gram, relevant_words_array, kw_list, splited_n_gram_word_list
    ):
        """Finds the most relevant n-gram words."""
        temporary_list = []
        temporary_list_two = []
        for i in range(n_gram):
            temporary_list.append(text_tokens[y: y + i + 1])
            k = re.sub(
                r'[!",:.;?()]$|^[!",:.;?()]|\W[!",:.;?()]', '', " ".join(
                    temporary_list[i]
                )
            )
            if k.lower() in relevant_words_array:
                temporary_list_two.append(k)

        if temporary_list_two:
            kw_list.append(
                sorted(temporary_list_two, key=lambda x: relevant_words_array.index(x.lower()))[0]
            )
            splited_n_gram_word_list.append(kw_list[0].split())

        return kw_list, splited_n_gram_word_list

    def replace_token(self, text_tokens, y, n_gram_word_list):
        """Replaces tokens in text with highlighted versions."""
        txt = " ".join(text_tokens[y: y + len(n_gram_word_list[0].split(" "))])
        kw_cleaned = re.sub(
            r'[!",:.;?()]$|^[!",:.;?()]|\W[!",:.;?()]', "", txt
        )
        new_expression = txt.replace(
            kw_cleaned, f"{self.highlight_pre}{n_gram_word_list[0]}{self.highlight_post}"
        )

        return y + len(n_gram_word_list[0].split(" ")), new_expression
