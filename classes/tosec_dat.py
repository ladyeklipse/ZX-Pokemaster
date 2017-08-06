from lxml import etree

class TOSECDat():

    machine_name = 'Sinclair ZX Spectrum'
    type = ''
    Format = ''

    def __init__(self, path):
        path = path.split(' - ')
        self.machine_name = path[0]
        self.format = path[-1]
