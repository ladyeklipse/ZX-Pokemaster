MIN_POKE_ADDRESS = 13384 #first 16K is ROM #I've lowered this value for Gyruss, which requires modifying ROM
MAX_POKE_ADDRESS = 65535 #POKE 65536,0 returns error even on 128k Speccy

class Poke(object):

    memory_bank = 8
    address = 0
    value = 0
    original_value = 0

    def __init__(self, address, value, memory_bank=8, original_value=0):
        if type(address)==str:
            address=int(address)
        if type(value)==str:
            if not value.strip().isdigit():
                value = 256
            else:
                value = int(value)
        if type(memory_bank)==str:
            memory_bank = int(memory_bank)
        if type(original_value)==str:
            original_value = int(original_value)
        if address<MIN_POKE_ADDRESS or address>MAX_POKE_ADDRESS:
            raise ValueError('Wrong address:'+str(address))
        elif value<0 or value>256:
            raise ValueError('Wrong value:'+str(value))
        elif memory_bank<0 or memory_bank>8:
            raise ValueError('Wrong memory bank:'+str(memory_bank))
        elif original_value<0 or original_value>255:
            raise ValueError('Wrong original value:'+str(original_value))
        else:
            self.memory_bank = memory_bank
            self.address = address
            self.value = value
            self.original_value = original_value

    def __eq__(self, other):
        if other.address == self.address and \
            other.value  == self.value:
            return True

    def toString(self):
        return str(self.address)+','+str(self.value)