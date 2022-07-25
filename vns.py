from os import remove
import funzioni as fun

def node_swap(tour):
    route = fun.deepcopy(tour)
    
    while True:
        i, j  = fun.r.sample(range(1, len(tour[0])-1), 2)
    
        if i != j:
            route[0][i], route[0][j] = route[0][j], route[0][i]
            route = fun.time_and_sat_calc(route) 
            break 
    
    return route

def stochastic_2_opt(tour):
    
    route = fun.deepcopy(tour)

    while True:
        i, j  = fun.r.sample(range(1, len(tour[0])-1), 2) #seleziono due nodi in maniera stocastica dal tour passato in input
        if not(i == 0 or j == 0 or abs(i-j)<=1): 
            break
        
    if i > j:
        i, j = j, i #se 'i' è più grande, scambio i valori per permettere uno switch 2-opt in seguito
    
    route[0][i:j+1] = list(reversed(route[0][i:j+1]))                       
    route = fun.time_and_sat_calc(route)                     
    
    return route
     
def chain_relocation(tour):
    #Chain relocation: intorno ottenuto dalla rimozione di una sequenza di 
    #archi dal ciclo e dal suo reinserimento in un altro punto. Si eliminano i
    #2 archi prima e dopo la sequenza, e un terzo laddove si va a reinserire.
    while True:
        i,j = fun.r.sample(range(1,len(tour[0])-2), 2)   
        
        if i > j:
            i,j = j,i
        if not (abs(i-j)==1 or abs(i-j)==len(tour[0])-3):
            break
    
    choose = list(range(1,len(tour[0])-1))
    choose = choose[0:(i-1)] + choose[j:]
    reloc_p = fun.r.choice(choose)
    del(choose)

    route = fun.deepcopy(tour)

    if reloc_p > j:
        route[0] = route[0][0:i] + route[0][j:reloc_p] + route[0][i:j] + route[0][reloc_p:]
    elif reloc_p < i:
        route[0] = route[0][0:reloc_p] + route[0][i:j] + route[0][reloc_p:i] + route[0][j:]

    route = fun.time_and_sat_calc(route) 

    return route


def variable_neighborhood_search(tour):

    start = fun.time()

    solution = fun.deepcopy(tour) 

    i = 0
    while True:
        if i == 0:
            candidate = stochastic_2_opt(solution)
        elif i == 1:
            candidate = node_swap(solution)
        elif i == 2:
            candidate = chain_relocation(solution)

        candidate = fun.time_and_sat_calc(candidate)

        if candidate[1] > solution[1] or (candidate[1] == solution[1] and candidate[2] < solution[2]): 
            solution = fun.deepcopy(candidate)
            i=0
        else: 
            i+=1
            if i == 3:
                break

    
    #f.write(f"VNS: {fun.time()-start}, {solution}\n")
    return solution