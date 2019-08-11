class SentenceObject():  
    def __init__(self, text, tokens, tagged, entities):
        self.text = text
        self.tokens = tokens
        self.tagged = tagged
        self.entities = entities
        self.periodic = False
        self.argument = False
        self.knownType = "Unknown"
