from asyncore import write
import json
from this import d
import openpyxl as xl

def readF():
    a = open("neigh_data_1.json")
    b = open("2opt_data_1.json")
    c = open("dbridge_data_1.json")
    d = open("vns_data_1.json")
    neig = json.load(a)
    opt2 = json.load(b)
    dbrdg = json.load(c)
    dvns = json.load(d)
    a.close()
    b.close()
    c.close()
    d.close()

    return neig, opt2, dbrdg, dvns


def write_excel(alg, name):
    sheet=xl.Workbook()
    ricerca=sheet['Sheet']
    #get_sheet_by_name('Sheet')
    ricerca['A1']='alfa = 0'
    ricerca['A1'].value
    ricerca['B1']='alfa = 0.25'
    ricerca['B1'].value
    ricerca['C1']='alfa = 0.5'
    ricerca['C1'].value
    ricerca['D1']='alfa = 0.75'
    ricerca['D1'].value
    ricerca['E1']='alfa = 1'
    ricerca['E1'].value

    for i in range(1,101):
        ricerca['A'+str(i+1)]=alg['0'][i][1]
        ricerca['A'+str(i+1)].value
        ricerca['B'+str(i+1)]=alg['0.25'][i][1]
        ricerca['B'+str(i+1)].value
        ricerca['C'+str(i+1)]=alg['0.5'][i][1]
        ricerca['C'+str(i+1)].value
        ricerca['D'+str(i+1)]=alg['0.75'][i][1]
        ricerca['D'+str(i+1)].value
        ricerca['E'+str(i+1)]=alg['1'][i][1]
        ricerca['E'+str(i+1)].value

    sheet.save(name+'.xlsx')


#neig.to_excel("best_data.xlsx")
neig = readF()[0]
opt2 = readF()[1]
dbrdg = readF()[2]
dvns = readF()[3]
write_excel(neig, 'neigh_graph')
write_excel(opt2, '2opt_graph')
write_excel(dbrdg, 'dbridge_graph')
write_excel(dvns, 'vns_graph')
