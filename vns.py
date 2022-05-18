import funzioni as fun
from funzioni import dist as Xdata


def stochastic_2_opt(tour):
    
    best_route = fun.deepcopy(tour)      
    
    i, j  = fun.r.sample(range(1, len(tour[0])-1), 2) #seleziono due nodi in maniera stocastica dal tour passato in input
    if (i > j):
        i, j = j, i #se 'i' è più grande, scambio i valori per permettere uno switch 2-opt in seguito
    
    best_route[0][i:j+1] = list(reversed(best_route[0][i:j+1]))           
    best_route[0][-1] = best_route[0][0]              
    best_route = fun.time_and_sat_calc(best_route)                     
    
    return best_route


def local_search(tour, attemps = 20, neighbourhood_size = 5):
    
    count = 0
    solution = fun.deepcopy(tour) 
    
    while (count < attemps): 
        for i in range(0, neighbourhood_size):
            candidate = stochastic_2_opt(solution)
            
            if ( (candidate[1] / candidate[2]) > (solution[1] / solution[2]) ):
                solution = fun.deepcopy(candidate)
                count = 0
            else:
                count += 1                             
    
    return solution 


def variable_neighborhood_search(tour, neighbourhood_size = 5):

    solution = fun.deepcopy(tour)
    best_solution = fun.deepcopy(tour)
    
    for i in range(0, neighbourhood_size):
        #solution = stochastic_2_opt(best_solution) 
        solution = local_search(solution, neighbourhood_size)
        
        if ( (solution[1] / solution[2]) > (best_solution[1] / best_solution[2]) ):
            best_solution = fun.deepcopy(solution) 
            

    return best_solution