class Sentence:
    def __init__(self, id, tokens=None, dependencies = None, text=None):
        if id is None:
            raise ValueError("id cannot be None")
        self.id = id
        self.tokens = tokens if tokens is not None else []
        self.dependencies = dependencies
        self.text = text

    def get_id(self):
        return self.id

    def get_tokens(self):
        return self.tokens

    def get_dependencies(self):
        return self.dependencies

    def set_dependencies(self, dependencies):
        self.dependencies = dependencies

    def get_text(self):
        return self.text
    
    def add_token(self, token):
        self.tokens.append(token)

    def is_empty(self):
        return len(self.tokens) == 0

    def __hash__(self):
        prime = 31
        result = 1
        result = prime * result + (0 if self.id is None else hash(self.id))
        return result

    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None:
            return False
        if not isinstance(obj, Sentence):
            return False
        other = Sentence(obj)
        if self.id is None:
            if other.id is not None:
                return False
        else:
            if self.id != other.id:
                return False
        return True

    def __str__(self):
        return f"s [id={self.id}, tk={self.tokens}]"
