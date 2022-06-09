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

    while (True):
        i, j  = fun.r.sample(range(1, len(tour[0])-1), 2) #seleziono due nodi in maniera stocastica dal tour passato in input
        if(not(i == j or i == 0 or j == 0 or i == j-1 or i == j+1)): 
            break
        
    if (i > j):
        i, j = j, i #se 'i' è più grande, scambio i valori per permettere uno switch 2-opt in seguito
    
    route[0][i:j+1] = list(reversed(route[0][i:j+1]))                       
    route = fun.time_and_sat_calc(route)                     
    
    return route
     
def chain_relocation(tour):
    route = fun.deepcopy(tour)

    while True:
        i, j = fun.r.sample(range(1, len(tour[0])-1), 2)
        if i != j:
            break

    if i > j:
        i, j = j, i

    rand = fun.r.randint((j-i+1), (len(tour[0])-(j+1)))
    k, l = (i,j) + rand 
    route[0][i:j] , route[0][k:l] = route[0][k:l], route[0][i:j]

    route = fun.time_and_sat_calc(route) 

    return route

def variable_neighborhood_search(tour):

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
        
    return solution