import re

from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.processor.TextProcessor import TextProcessor
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils


class CodeRefPM(StepsToReproducePatternMatcher):
    NOUNS_TERM = {"attachment", "build/install", "call", "class", "code", "command", "config", "configuration",
                  "configure",
                  "container", "dockerfile", "env", "example", "example/test", "excerpt", "file", "function", "hql",
                  "html",
                  "html/fbml", "html/ssi", "htpasswd", "image", "installer", "line", "method", "model", "parameter",
                  "program", "project", "query", "sample", "screenshot", "screen-shot", "script", "snippet",
                  "statement",
                  "test", "test case", "test.htm", "tool", "trace", "video", "xml"}

    NOUN_TERMS_REGEX = "(" + "|".join(NOUNS_TERM) + ")"

    LOCATION_TERMS = {"here", "below", "above", "next"}

    VERB_AS_ADJS = {"provide", "enclose", "join", "attach", "upload", "include"}
    ADJS = {"provided", "enclosed", "joined", "attached", "uploaded", "included"}

    def match_sentence(self, sentence):
        # Remove label: "created attachment 34535"
        tokens_no_label = self.get_tokens_no_label(sentence.get_tokens())

        text = TextProcessor.get_string_from_lemmas(Sentence(sentence.get_id(), tokens_no_label))


        # Cases: this/here is the snippet
        regex = r"(?s).*(this|here) be [a-zA-Z]+ (\p{Punct}+ )?" + self.NOUN_TERMS_REGEX + r".*"
        if re.match(regex, text):
            return 1

        # -----------------------------------

        noun_idx = -1
        is_location_term = False
        is_adjective = False
        ends_with = False
        next_colon = False
        is_following_noun = False

        # Check for some common sentence ends: ":", "e.g.", "like:", etc
        if text.endswith(":") or text.endswith("e.g.") or re.match(r"(?s).*(,) (for example|as|like|like this|here) :$", text):
            ends_with = True

        for i, token in enumerate(tokens_no_label):
            # There is a noun that refers to code, files, etc.
            if any(token.get_lemma().equalsIgnoreCase(t) for t in self.NOUNS_TERM):
                if token.get_general_pos() == "NN":
                    noun_idx = i
                    if i + 1 < len(tokens_no_label):
                        # Case: "code:"
                        if tokens_no_label[i + 1].get_lemma() == ":":
                            next_colon = True
                        else:
                            # Case "code is"
                            if i + 2 < len(tokens_no_label):
                                if tokens_no_label[i + 1].get_general_pos() == "VB" and tokens_no_label[i + 1].get_lemma() == "be" and tokens_no_label[i + 2].get_lemma() == ":":
                                    next_colon = True
                    # Check for location terms
            elif any(token.get_lemma().equalsIgnoreCase(t) for t in self.LOCATION_TERMS) and (
                    token.get_general_pos() == "RB" or token.get_general_pos() == "IN" or token.get_general_pos() == "JJ"):
                is_location_term = True
            # Check for adjectives expressing attachment
            elif (any(token.get_lemma().equalsIgnoreCase(t) for t in self.VERB_AS_ADJS) and token.get_pos() == "VBN") or (
                    token.get_lemma() == "follow" and token.get_pos() == "VBG") or (
                    any(token.get_lemma().equalsIgnoreCase(t) for t in self.ADJS) and token.get_general_pos() == "JJ"):
                is_adjective = True
            # Check for "following"
            elif token.get_lemma() == "following":
                is_following_noun = True

            # If there is at least a code term and (location term, adjective, ends with colon, next colon, following noun)
            if noun_idx != -1 and (is_location_term or is_adjective or ends_with or next_colon or is_following_noun):
                return 1


        # Check for just the noun, no verb
        # Case: "Excel file with macro
        if noun_idx != -1 and not any(t.get_general_pos() == "VB" for t in tokens_no_label):
            return 1

        # Case allowed: "validated file"
        if noun_idx != -1 and noun_idx - 1 >= 0:
            if tokens_no_label[noun_idx - 1].get_pos() == "VBN":
                other_tokens_ok = True
                for i, t in enumerate(tokens_no_label):
                    if noun_idx != i and noun_idx - 1 != i:
                        if t.get_general_pos() == "VB":
                            other_tokens_ok = False
                            break
                if other_tokens_ok:
                    return 1

        # -------------------------------

        # Cases: ... the code shows: ...
        if noun_idx != -1 and re.match(r".* " + tokens_no_label[noun_idx].get_lemma() + " .* : .*", text):
            return 1


        return 0

    def get_tokens_no_label(self, tokens):
        tokens_no_label = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.get_lemma() == "create" and token.get_pos() == "VBN":
                if i + 2 < len(tokens):
                    if tokens[i + 1].get_lemma() == "attachment" and re.match(r"\d+", tokens[i + 2].get_lemma()):
                        i += 3
                        continue

            tokens_no_label.append(token)
            i += 1

        return tokens_no_label

