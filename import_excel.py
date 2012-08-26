import os
from main.models import Credit
import xlrd

def import_file(file_name):
    HEADER_ROW = 0

    book = xlrd.open_workbook('%s' % file_name, encoding_override='cp1252')
    sh = book.sheet_by_index(0)
    header_row = sh.row(HEADER_ROW)

    #print header_row
    
    if(sh.nrows > 1):
        Credit.objects.all().delete()
        for rx in range(1, sh.nrows):

            amount_number = sh.cell_value(rowx=rx, colx=1)

            if amount_number != '':

                r = Credit(credit_id=sh.cell_value(rowx=rx, colx=0),
                amount=amount_number,
                _range=sh.cell_value(rowx=rx, colx=2),
                cancel_reason=sh.cell_value(rowx=rx, colx=3),
                supposed_by=sh.cell_value(rowx=rx, colx=4),
                taxpayer_type=sh.cell_value(rowx=rx, colx=5),
                entity=sh.cell_value(rowx=rx, colx=6),
                sector=sh.cell_value(rowx=rx, colx=7))
                r.save()
                print 'Insertando... ' + str(r.id)