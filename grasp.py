#Simple GRASP with two type of greedy, a VNS algorithm can be used
import funzioni as fun
from funzioni import dist as Xdata
from vns import variable_neighborhood_search as vns

#Greedy
def neighborhood(node, time, alfa):
    
    rank = []
    rcl = [] 
    for i in range(1, Xdata.shape[0]):
        if (i == node) :
            continue
        d = (Xdata[i,node] + fun.open_attr(i,time))
        rank.append( (d, i) )
        
    #costruzione rcl
    
    m = min(rank, key=lambda x:x[0])[0]
    M = max(rank, key=lambda x:x[0])[0]
    
    for i in range(len(rank)):
        if(rank[i][0] <= m + alfa*(M-m)):
            rcl.append(rank[i])

    return rcl

"""
#Restituisce una lista di nodi ordinati in base al rapporto di gradimento ponderato e distanza con il nodo passato in input
def ratio(node = 0): 

    candidate = []

    for i in range(len(fun.f["attrazioni"])):

        if(node == (i + 1)):
            continue
        
        Grad_pond = fun.Grad_pond[(i + 1)]
        Ttot = ( Xdata[(i + 1), node] )
        if (Ttot == 0):
            GT=100000
        else:
            GT=Grad_pond/(Ttot/60)
        candidate.append([Ttot, (i + 1), GT])

    candidate = sorted(candidate, reverse = True, key=lambda x:x[2])

    return candidate
#-
"""

#Local Search : Ricerca esaustiva degli ottimi locali
def ls_2_opt(attr_tour):

    best_route = fun.deepcopy(attr_tour)
    
    for i in range(0, len(attr_tour[0]) - 2):
        for j in range(2, len(attr_tour[0]) - 1):
            tour = fun.deepcopy(attr_tour) 
            if( i == j-1 or i == j+1 or i == j):
                continue
            tour[0][(i+1):(j+1)] = list(reversed(tour[0][(i+1):(j+1)])) #inverto una parte della lista perchè scambio gli archi
            tour = fun.time_and_sat_calc(tour) 
            if (best_route[1]/best_route[2] < tour[1]/tour[2]):
                best_route = fun.deepcopy(tour)

    return best_route

def ls_double_bridge(attr_tour):

    tour = fun.deepcopy(attr_tour)
    best_route = fun.deepcopy(tour)

    for i in range(0,len(tour[0])-7):
        for j in range(i+2,len(tour[0])-5):
            for k in range(j+2,len(tour[0])-3):
                for l in range(k+2,len(tour[0])-1):
                    if(i==0 and l==len(tour[0])-2):
                        continue
                    tour[0] = list(attr_tour[0][:(i+1)] + attr_tour[0][(k+1):(l+1)] + attr_tour[0][(j+1):(k+1)] + attr_tour[0][(i+1):(j+1)] + attr_tour[0][(l+1):])
                    tour = fun.time_and_sat_calc(tour)
                    if (best_route[1]/best_route[2] < tour[1]/tour[2]):
                        best_route = fun.deepcopy(tour)
    
    return best_route
#-

#Principal Function
def greedy_randomized_adaptive_search_procedure(iterations, alfa):
    
    count = 0
    start_tour = fun.first_op()
    best_solution = fun.deepcopy(start_tour)

    ls = int(input("\nPress 1 to use VNS, otherwise press 0 \n"))

    while (iterations > count):
        #Creating one solution with one of the two greedy
        first_sol = find_solution(alfa)
        #LS
        if(ls == 0):
            #local search without VNS
            candidate = ls_double_bridge( ls_2_opt( first_sol ) )
        else:
            #local search with VNS
            candidate = vns(first_sol)
        
        if ( (candidate[1] / candidate[2]) > (best_solution[1] / best_solution[2]) ):
            best_solution = fun.deepcopy(candidate)
            count += 1
            #fun.write_res( best_solution, (str(greedy)), count )
            print('Iteration =', count, '-> Satisfaction =', best_solution[1], ', Time =', best_solution[2])

    print("Best Solution =\n", best_solution)
    return best_solution


def find_solution(alfa):

    seed = [[],float("inf"), float("-inf")]
    sequence = [0]
    time = 0
 
    while(True):
  
        RCL = neighborhood(sequence[-1], time/60, alfa)
        #prendo un elemento casuale dalla RCL
        next = fun.r.choice(RCL)

        if( len(sequence) > 2 and fun.end_tour(time/60, sequence[-1], next[1]) ): 
            break
        else:
            time += next[0]
            sequence.append(next[1])    
        
    #solution created
    sequence.append(sequence[0])
    seed[0] = sequence
    seed = fun.time_and_sat_calc(seed)
    return seed


#MAIN
tour = greedy_randomized_adaptive_search_procedure(iterations = 1000, alfa = 0.5)