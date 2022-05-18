import funzioni as fun
from grasp import greedy_randomized_adaptive_search_procedure as g
from funzioni import first_op as FOp

#inizializzazione albergo
'''
    #creazione dati randomici per l'utente (posizione, gradimento)

    fun.f["utente"]["x"]=round(fun.r.uniform(fun.f["range_albergo"]["x_min"],fun.f["range_albergo"]["x_max"]),12)
    fun.f["utente"]["y"]=round(fun.r.uniform(fun.f["range_albergo"]["y_min"],fun.f["range_albergo"]["y_max"]),12)

    for grad in fun.f["utente"]["gradimento"]:
        fun.f["utente"]["gradimento"][grad]=fun.r.randint(1,5)
        
    fun.dist_home()
    fun.np.savetxt('distanze.txt', fun.dist, fmt='%-5i')

    print("inserisci l'orario di partenza del percorso: ")
    fun.f["utente"]["t_inf"]=int(input())
    print("inserisci l'orario di fine del percorso: ")
    fun.f["utente"]["t_sup"]=int(input())

    with open("./InputCompleto.json", "w") as js:
        fun.json.dump(fun.f, js,indent=4) 
'''
#fase iniziale terminata

fun.os.mkdir("Solutions")
  
    
#eseguo i vari algoritmi
res=[]
res.append( g(iterations = 500, greediness_value = 0.5) )


#print("Ratio:\n",res[0], "\n\n1_Open:\n", res[1], "\n\nNeighbors:\n",res[2], end="\n\n\n---FINE---")