import numpy as np, requests, json , openpyxl as xl, webbrowser as wb, random as r, os, folium
from copy import deepcopy
from time import time 


dist = np.loadtxt('distanze.txt', dtype=int).reshape((34,34))

with open("InputCompleto.json") as js:
    f=json.load(js)

Grad_pond=[0]
for p in f["attrazioni"]: 
    Grad_pond.append(np.average(list(p["gradimento"].values()), weights=list(f["utente"]["gradimento"].values())))

'''
def dist_home(): #utilizzo iniziale solo per calcolare le distanze albergo-attrazione

    try:
        with open("API_orienteering-fe.txt","r") as api:
            api_key = api.read()

        home = f["utente"]
        start = str(home["x"]) + ", " + str(home["y"])
        url = "" #"https://maps.googleapis.com/maps/api/distancematrix/json?"

        for j in range(len(f["attrazioni"])):
            dest = f["attrazioni"][j]["nome"] + ", Ferrara, Italia"
            r = requests.get(url + "&origins=" + start + "&destinations=" + dest + "&mode=walking" + "&transit_routing_preference=less_walking" + "&language=ita" + "&key=" + api_key)
            dist[0,j+1] = dist[j+1,0] = round(r.json()["rows"][0]["elements"][0]["duration"]["value"]/60)
        
        return 1

    except:
        return 0
'''

def open_attr(node, time): #verifico che una determinata attrazione sia aperta

    ora_attuale = f["utente"]["inizio"] + time

    for i in range(len(f["attrazioni"][node-1]["orari"])):
        apertura = f["attrazioni"][node-1]["orari"][i]["apre"]
        chiusura = f["attrazioni"][node-1]["orari"][i]["chiude"]

        if (apertura <= ora_attuale < chiusura):
            return 0
        elif(i==0 and ora_attuale < apertura):
            return int((apertura - ora_attuale)*60) 

    if(ora_attuale >= chiusura):
        return int((24 + apertura - ora_attuale)*60)
    elif(ora_attuale <= apertura):
        return int((apertura - ora_attuale)*60)
    #se l'attrazione è chiusa ritorno il tempo che manca affinchè sia aperta
    #restituisco il risultato in minuti


def end_tour(time,a,b): #calcolo se rimane tempo per visitare l'attrazione e tornare all'albergo
    
    t_tot = f["utente"]["fine"] - f["utente"]["inizio"]
    t_pass = time + ( (dist[a,b] + dist[b,0] + open_attr(b, time)) /60 )
    #tempo.passato = tempo.visitati + (tempo.pross.attr + tempo.ritorno + penalità)

    if( t_tot >= t_pass):
        return 0
    else:
        return 1


        
'''
def wexcel(tour, fun_name, iteration): #scrivo il risultato su un file excel

    try:
        sheet=xl.Workbook()
        ricerca=sheet.get_sheet_by_name('Sheet')
        
        ricerca['A1']='Num nodi visitati'
        ricerca['A1'].value
        ricerca['A2']=len(tour[0])-2 #N° attrazioni visitate oltre l'albergo
        ricerca['A2'].value

        ricerca['B1']="Gradimento:"
        ricerca['B1'].value
        ricerca['B2']=tour[1]
        ricerca['B2'].value

        ricerca['C1']='Tempo trascorso:'
        ricerca['C1'].value
        ricerca['C2']=tour[2]
        ricerca['C2'].value
        
        ricerca['E1']='Nodi visitati:'
        ricerca['E1'].value

        for i in range(len(tour[0])):    
            ricerca['E'+str(i+2)]=tour[0][i]
            ricerca['E'+str(i+2)].value
        
        sheet.save('.//'+fun_name+'//#'+str(iteration)+'.xlsx')
        return 1

    except:
        return 0    

def write_res(tour, fun_name, iteration): #scrivo i risultati su un file excel e creo una mappa per ogni soluzione possibile trovata

    if not os.path.exists(fun_name) :
        os.mkdir(fun_name)
    
    map = folium.Map(location=[44.83895673644131, 11.614725304456822], zoom_start=14)

    folium.Marker(
        location = [f["utente"]["x"],f["utente"]["y"]],
        popup = "Albergo", 
        tooltip = 0, 
        icon = folium.Icon(color="lightgreen",icon="home", prefix="fa")
        ).add_to(map)
    
    for i in range(len(f["attrazioni"])):
        folium.Marker(
            location = [f["attrazioni"][i]["x"],f["attrazioni"][i]["y"]],
            popup = f["attrazioni"][i]["nome"],
            icon = folium.Icon(color="darkred", icon="map", prefix="fa")
            ).add_to(map)

    wexcel(tour, fun_name, iteration)
    route(tour)

    folium.GeoJson("percorso.geojson", name=fun_name).add_to(map)
    folium.LayerControl().add_to(map)
    
    for k in tour[0][1:-1]:
        folium.Marker(
            location = [f["attrazioni"][(k-1)]["x"],f["attrazioni"][(k-1)]["y"]],
            popup = f["attrazioni"][(k-1)]["nome"], 
            tooltip = tour[0].index(k),
            icon = folium.Icon(color="darkpurple", icon="map", prefix="fa")
            ).add_to(map)

    map.save('.//'+fun_name+"//Map#"+str(iteration)+".html")
    #wb.open(fun_name+"\\#"+str(iteration)+".html")
    del(map)

def route(tour): #scrivo le coordinate dei luoghi su un file geojson per poi creare la mappa
    
    clear_route()

    try:
        with open("percorso.geojson") as js:
            g = json.load(js)

        for i in tour[0][1:-1]:
            attr = [f["attrazioni"][(i-1)]["y"],f["attrazioni"][(i-1)]["x"]]
            g["features"][0]["geometry"]["coordinates"].append(attr)

        with open("percorso.geojson", "w") as js:
            json.dump(g, js, indent=4)

        return 1

    except:
        return 0

def clear_route(): #ripulisco il file geojson contenente il percorso della soluzione predcedente
    
    r_default = {
        "type": "FeatureCollection",
        "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                ]
            }
        }
        ]
    }
    
    r_default["features"][0]["geometry"]["coordinates"].append([f["utente"]["y"],f["utente"]["x"]])

    with open("percorso.geojson", "w") as js:
        json.dump(r_default, js, indent=4)
    
    return 1
'''


def time_and_sat_calc(tour):
    sat = 0
    time = 0

    for k in range(1,len(tour[0])):
        
        open = open_attr(tour[0][k], time/60)
        time = time + (dist[tour[0][k-1],tour[0][k]] + open)
        
        #se ancora non è stata visitata l'attrazione aggiungo il gradimento
        if (tour[0][k] not in tour[0][0:k]): 
            sat += Grad_pond[tour[0][k]]

        if(end_tour(time/60, tour[0][k-1], tour[0][k])):
            break


    tour[2] = round(time / 60, 4)
    tour[1] = round(sat,4)
    return tour




