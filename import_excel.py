import os
from main.models import Credit
import xlrd

def import_file(file_name):
    HEADER_ROW = 1

    book = xlrd.open_workbook('%s' % file_name, encoding_override='cp1252')
    sh = book.sheet_by_index(0)
    header_row = sh.row(HEADER_ROW)
    if(sh.nrows > 1):
        Credit.objects.all().delete()
        for rx in range(1, sh.nrows):
            genero = sh.cell_value(rowx=rx, colx=0)

            if genero == 'm' or genero == 'M':
                genero = 'hombre'

            elif genero == 'f' or genero == 'F':
                genero = 'mujer'

            else:
                genero = ''

            r = Credit(sex=genero,
            name=sh.cell_value(rowx=rx, colx=1),
            lastname=sh.cell_value(rowx=rx, colx=2),
            party=sh.cell_value(rowx=rx, colx=3),
            election_type=sh.cell_value(rowx=rx, colx=4),
            entity=sh.cell_value(rowx=rx, colx=5),
            district=str(sh.cell_value(rowx=rx, colx=6)).replace('.0', ''),
            circunscription=sh.cell_value(rowx=rx, colx=7),
            phone=str(sh.cell_value(rowx=rx, colx=8)).replace('.0', ''),
            extension=str(sh.cell_value(rowx=rx, colx=9)).replace('.0', ''),
            email=sh.cell_value(rowx=rx, colx=10),
            twitter=sh.cell_value(rowx=rx, colx=11),
            commissions=sh.cell_value(rowx=rx, colx=12),
            bio=sh.cell_value(rowx=rx, colx=13),
            patrimony=sh.cell_value(rowx=rx, colx=14),
            answer=sh.cell_value(rowx=rx, colx=15),
            answer_why=sh.cell_value(rowx=rx, colx=16),
            suplent=sh.cell_value(rowx=rx, colx=17),
            status=sh.cell_value(rowx=rx, colx=18))
            r.save()
            print 'Insertando... ' + str(r.id)
