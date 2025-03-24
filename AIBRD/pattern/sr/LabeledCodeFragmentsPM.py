from pattern.entity.Token import Token
from pattern.entity.Sentence import Sentence
from pattern.processor.TextProcessor import TextProcessor
from pattern.StepsToReproducePatternMatcher import StepsToReproducePatternMatcher
from pattern.Utils.SentenceUtils import SentenceUtils
import re


class LabeledCodeFragmentsPM(StepsToReproducePatternMatcher):
    OTHER_LABEL_TOKENS = {"example", "e.g.", "persistence.xml"}

    CODE_SYMBOLS = {"-LCB-", "-RCB-", "-LRB-", "-RRB-", "-LSB-", "-RSB-", ";", "*", "/", "%", "+", "-", "<", ">", "=",
                    "!", "&", "^", "|", "?", ":", "\"", "'", "--", "++"}

    JAVA_KEYWORDS = {"abstract", "continue", "for", "new", "switch", "assert", "default", "goto", "package",
                     "synchronized", "boolean", "do", "if", "private", "this", "break", "double", "implements",
                     "protected", "throw", "byte", "else", "import", "public", "throws", "case", "enum", "instanceof",
                     "return", "transient", "catch", "extends", "int", "short", "try", "char", "final", "interface",
                     "static", "void", "class", "finally", "long", "strictfp", "volatile", "const", "float", "native",
                     "super", "while"}

    DOCKER_KEYWORDS = {"add", "copy", "env", "expose", "label", "maintainer", "user", "workdir", "volume", "stopsignal"}

    DOCKER_COMMAND_KEYWORDS = {"attach", "build", "commit", "connect", "cp", "create", "demote", "diff", "disconnect",
                               "dockerd", "events", "exec", "export", "history", "images", "import", "info", "init",
                               "inspect", "join", "join-token", "kill", "leave", "load", "login", "logout", "logs",
                               "ls", "network", "node", "pause", "port", "promote", "ps", "pull", "push", "rename",
                               "restart", "rm", "rmi", "run", "save", "scale", "search", "service", "start", "stats",
                               "stop", "swarm", "tag", "top", "unpause", "update", "version", "volume", "wait"}

    SQL_KEYWORDS = {"alter", "begin", "between", "boolean", "case", "char", "column", "commit", "constraint", "create",
                    "cursor", "date", "declare", "decimal", "delete", "distinct", "fetch", "foreign", "from",
                    "function", "having", "inner", "insert", "into", "join", "like", "outer", "procedure", "primary",
                    "rollback", "select", "table", "timestamp", "update", "varchar"}

    def matchSentence(self, sentence):
        # 获取句子的标记和文本
        tokens = sentence.getTokens()
        text = TextProcessor.get_string_from_lemmas(sentence)

        # 检查是否包含特定模式
        # 首先检查关键字匹配
        keyword_sets = [self.JAVA_KEYWORDS, self.DOCKER_KEYWORDS, self.SQL_KEYWORDS, self.DOCKER_COMMAND_KEYWORDS]
        for keyword_set in keyword_sets:
            keyword_matches = [token for token in tokens if token.getLemma() in keyword_set]
            keyword_ratio = len(keyword_matches) / len(tokens)
            if keyword_ratio > 0.2:
                return 1

        # 然后检查 XML 标记
        num_tags = self.check_for_XML(tokens)
        tags_ratio = num_tags / len(tokens)
        if tags_ratio > 0.2:
            return 1

        # 如果不满足任何条件，返回0表示不匹配
        return 0

    def check_for_XML(self, tokens):
        num_tags = 0
        num_tag_tokens = sum(1 for tok in tokens if re.match(r"<[\w-]+ .*>|</?[\w-]+>", tok.lemma))
        num_tags = num_tags + num_tag_tokens
        return num_tags


