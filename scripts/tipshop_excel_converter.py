from classes.database import *
import os
XLSX_FILENAME = 'pokes.xlsx'
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
def db2xlsx():
    import xlsxwriter
    db = Database()
    sql = "SELECT wos_id, name, pok_file_contents, tipshop_multiface_pokes_section " \
          "FROM game WHERE pok_file_contents != ''"
    raw_data = db.execute(sql)
    workbook = xlsxwriter.Workbook(XLSX_FILENAME)
    mformat = workbook.add_format()
    mformat.set_text_wrap()
    mformat.set_align('top')
    worksheet = workbook.add_worksheet()
    worksheet.set_default_row(200)
    worksheet.set_column('C:C', 40)
    worksheet.set_column('D:D', 40)
    for i, row in enumerate(raw_data):
        game = Game()
        game.importPokFile(text=row[2])
        pok_contents = game.getPokFileContents(for_xlsx = True)
        multiface_poke_secion = row[3]
        worksheet.write_row(i, 0, [
            str(row['wos_id']).zfill(7),
                row['name'],
                pok_contents,
                multiface_poke_secion
        ], mformat)
    workbook.close()

def xlsx2db():
    import xlrd
    db = Database()
    workbook = xlrd.open_workbook(XLSX_FILENAME)
    worksheet = workbook.sheet_by_index(0)
    for i in range(worksheet.nrows):
        wos_id = int(worksheet.cell_value(rowx=i, colx=0))
        if wos_id>9000000:
            continue
        pok_file_contents = worksheet.cell_value(rowx=i, colx=2)
        game = Game()
        try:
            game.importPokFile(text=pok_file_contents)
            for cheat in game.cheats:
                if cheat.description.isdigit():
                    raise(ValueError('Cheat desc is digit!'))
            pok_file_contents = game.getPokFileContents()
        except Exception as e:
            print(str(wos_id).zfill(7))
            #raise e
        sql = 'UPDATE game SET pok_file_contents = ? WHERE wos_id=?'
        params = [pok_file_contents, wos_id]
        print(sql, params)
        db.execute(sql, params)
    db.commit()


if __name__=='__main__':
    if not os.path.exists(XLSX_FILENAME):
        print('db to xlsx')
        db2xlsx()
        os.startfile(XLSX_FILENAME)
    else:
        print('xlsx to db')
        xlsx2db()
