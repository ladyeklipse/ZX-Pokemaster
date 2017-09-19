from classes.poke import *

class Cheat(object):

    def __init__(self, description):
        if description:
            self.description = description[0].upper()+description[1:].strip()
        self.pokes = []

    def __repr__(self):
        return '<Cheat '+'"'+self.description+'": '+self.pokesToString()+'>'

    def pokesToString(self):
        return ':'.join([poke.toString() for poke in self.pokes])


    def __eq__(self, other):
        # if len(self.pokes)!=len(other.pokes):
        #     return False
        for poke in self.pokes:
            if poke not in other.pokes:
                return False
        return True

    def addPoke(self, address=0, value=0, memory_bank=8, original_value=0):
        poke = Poke(address, value, memory_bank, original_value)
        if not poke:
            raise ValueError('Wrong poke')
        if poke not in self.pokes:
            self.pokes.append(poke)

    def asFileRecord(self, for_xlsx=False):
        record = []
        if for_xlsx:
            record.append('N '+self.description)
        else:
            record.append('N' + self.description)
        for i, poke in enumerate(self.pokes):
            if i == len(self.pokes) - 1:
                marker = 'Z'
            else:
                marker = 'M'
            line = ' '.join([marker,
                             str(poke.memory_bank),
                             str(poke.address),
                             str(poke.value),
                             str(poke.original_value)])
            record.append(line)
        return '\n'.join(record)
