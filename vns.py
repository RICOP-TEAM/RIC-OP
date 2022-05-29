import funzioni as fun

def stochastic_2_opt(tour):
    
    best_route = fun.deepcopy(tour)

    while (True):
        i, j  = fun.r.sample(range(1, len(tour[0])-1), 2) #seleziono due nodi in maniera stocastica dal tour passato in input
        if(not(i == j or i == 0 or j == 0 or i == j-1 or i == j+1)): 
            break
        
    if (i > j):
        i, j = j, i #se 'i' è più grande, scambio i valori per permettere uno switch 2-opt in seguito
    
    best_route[0][i:j+1] = list(reversed(best_route[0][i:j+1]))                       
    best_route = fun.time_and_sat_calc(best_route)                     
    
    return best_route
     

def variable_neighborhood_search(tour, neighbourhood_size = 5):

    solution = fun.deepcopy(tour) #x=initial_solution
    count = 0 #k=1
    
    while (count < neighbourhood_size): #while k <= kmax do
        candidate = stochastic_2_opt(solution) #shaking

        if ( candidate[1] > solution[1] or (candidate[1] == solution[1] and candidate[2] < solution[2])): #if c(x')> c(x) then
            solution = fun.deepcopy(candidate) #x = x'
            count = 0 #k = 1
       
        else:
            count += 1 #k= k+1                            
     
    print(f"\n\nSOLUZIONE stock-VNS --> {solution}\n\n") 
    
    return solution
    

        