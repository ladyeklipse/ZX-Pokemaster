class GameAlias():

    def __init__(self, name=None, language='en'):
        self.name = name
        self.language = language

    def __eq__(self, other):
        if self.language==other.language and \
            self.name==other.name:
            return True
        return False