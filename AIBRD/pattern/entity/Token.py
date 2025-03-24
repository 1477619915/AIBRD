class Token:
    def __init__(self, word, general_pos, pos, lemma, stem):
        self.word = word
        self.general_pos = general_pos   # 一般词性
        self.pos = pos                   # 详细词性
        self.lemma = lemma               # 单词的词元
        self.stem = stem                 # 单词的词干

    def get_word(self):
        return self.word

    def set_word(self, word):
        self.word = word

    def get_general_pos(self):
        return self.general_pos

    def set_general_pos(self, general_pos):
        self.general_pos = general_pos

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_stem(self):
        return self.stem

    def set_stem(self, stem):
        self.stem = stem

    def get_lemma(self):
        return self.lemma

    def set_lemma(self, lemma):
        self.lemma = lemma

    def __str__(self):
        return f"(w={self.word}, gp={self.general_pos}, p={self.pos}, l={self.lemma})"

