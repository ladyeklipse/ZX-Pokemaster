from classes.database import *
import os
XLSX_FILENAME = 'pokes.xlsx'

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
        worksheet.write_row(i, 0, [
            str(row['wos_id']).zfill(7),
                row['name'],
                row[2],
                row[3]
        ], mformat)
    workbook.close()

def xlsx2db():
    import xlrd
    db = Database()
    workbook = xlrd.open_workbook(XLSX_FILENAME)
    worksheet = workbook.sheet_by_index(0)
    for i in range(worksheet.nrows):
        wos_id = int(worksheet.cell_value(rowx=i, colx=0))
        pok_file_contents = worksheet.cell_value(rowx=i, colx=2)
        game = Game()
        try:
            game.importPokFile(text=pok_file_contents)
            for cheat in game.cheats:
                if cheat.description.isdigit():
                    raise(ValueError('Cheat desc is digit!'))
        except Exception as e:
            print(str(wos_id).zfill(7))
            #raise e
        sql = 'UPDATE game SET pok_file_contents = ? WHERE wos_id=?'
        params = [pok_file_contents, wos_id]
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
