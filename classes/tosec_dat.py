from lxml import etree
# from xml.dom import minidom
import time
import os
from io import StringIO

def prettify(xml_text):
    """Pretty prints xml."""
    parser = etree.XMLParser(remove_blank_text=True)
    file_obj = StringIO(xml_text.decode('utf-8'))
    tree = etree.parse(file_obj, parser)
    pretty_xml = etree.tostring(tree,
                                encoding='utf-8',
                                pretty_print=True).decode('utf-8')
    pretty_xml = pretty_xml.replace('  ', '\t')
    return pretty_xml

class TOSECDat():

    machine_name = 'Sinclair ZX Spectrum'
    type = ''
    format = ''
    contributors = ['Lady Eklipse']
    caption = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE datafile PUBLIC "-//Logiqx//DTD ROM Management Datafile//EN" "http://www.logiqx.com/Dats/datafile.dtd">

'''


    def __init__(self, path):
        path = path.split(' - ')
        self.files = []
        self.machine_name = path[0]
        self.type = ' - '.join(path[1:-1])
        self.format = path[-1][1:-1].lower()
        self.importOldContributors()
        self.header = self.getHeader()
        self.md5s = []

    def importOldContributors(self):
        base_name = self.getBaseFileName()
        for root, dirs, files in os.walk('tosec'):
            files = [file for file in files if file.startswith(base_name)]
            break
        if files:
            old_file = os.path.join('tosec', files[0])
            print('importing contributors from', old_file)
            with open(old_file, 'rb') as f:
                contents = f.read()
                root = etree.XML(contents)
                header = root[0]
                for element in header:
                    if element.tag=='author':
                        self.contributors += [x for x in element.text.split(' - ') if x not in self.contributors]
                        break
        else:
            print(self.getBaseFileName())

    def getHeader(self):
        header = etree.Element('header')
        name = etree.Element('name')
        name.text = self.getBaseFileName()
        header.append(name)
        description = etree.Element('description')
        description.text = self.getExportFileName()
        header.append(description)
        category = etree.Element('category')
        category.text = 'TOSEC'
        header.append(category)
        version = etree.Element('version')
        version.text = time.strftime('%Y-%m-%d')
        header.append(version)
        date = etree.Element('date')
        date.text = time.strftime('%d.%m.%Y %H:%M:%S')
        header.append(date)
        author = etree.Element('author')
        author.text = ' - '.join(self.contributors)
        header.append(author)
        email = etree.Element('email')
        email.text = 'contact@tosecdev.org'
        header.append(email)
        homepage = etree.Element('homepage')
        homepage.text = 'TOSEC'
        header.append(homepage)
        url = etree.Element('url')
        url.text ='http://www.tosecdev.org/'
        header.append(url)
        comment = etree.Element('comment')
        comment.text = 'Generated by ZX Pokemaster'
        header.append(comment)
        return header

    def getBaseFileName(self):
        components = [self.machine_name,
                      self.type,
                      '['+self.format.upper()+']']
        filename = ' - '.join(components)
        return filename

    def addFiles(self, files):
        for file in files:
            self.addFile(file)

    def addFile(self, file):
        if file.getMD5() in self.md5s:
            print('Ignoring', file)
            return
        copies_count = file.countAlternateDumpsIn(self.files)
        if copies_count:
            file.addAlternateModFlag(copies_count,
                                      tosec_compliant=True,
                                      short_filenames=False)
        else:
            file.alt_dest = file.getTOSECName()
        self.files.append(file)
        self.md5s.append(file.getMD5())

    def export(self):
        root = etree.Element('datafile')
        root.append(self.header)
        self.files = sorted(self.files, key=lambda file: file.alt_dest)
        for file in self.files:
            file_tag = self.getFileTag(file)
            root.append(file_tag)
        export_path = self.getExportPath()
        with open(export_path, 'w+', encoding='utf-8') as f:
            f.write(self.caption)

            # contents = minidom.parseString(etree.tostring(root))
            # contents = contents.toprettyxml(indent='\t').split('\n')
            # contents = '\n'.join(contents[1:])

            contents = etree.tostring(root, encoding='utf-8')
            contents = prettify(contents)
            f.write(contents)

    def getExportPath(self):
        dir_path = os.path.join('tosec', 'Generated (v{})'.format(time.strftime('%Y-%m-%d')))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        filename = self.getExportFileName()
        return os.path.join(dir_path, filename)

    def getExportFileName(self):
        filename = self.getBaseFileName()
        filename += ' (TOSEC-v{}_CM).dat'.format(time.strftime('%Y-%m-%d'))
        return filename

    def getFileTag(self, file):
        game_tag = etree.Element('game')
        game_name = os.path.splitext(file.getDestPath())[0]
        game_tag.attrib['name'] = game_name
        game_desc = etree.Element('description')
        game_desc.text = game_name
        game_tag.append(game_desc)
        rom = etree.Element('rom')
        rom.attrib['name'] = file.getDestPath()
        rom.attrib['size'] = str(file.size)
        rom.attrib['crc'] = file.getCRC32()
        rom.attrib['md5'] = file.getMD5()
        rom.attrib['sha1'] = file.getSHA1()
        game_tag.append(rom)
        return game_tag



