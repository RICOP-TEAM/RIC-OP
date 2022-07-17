#Simple GRASP with two type of greedy, a VNS algorithm can be used
import funzioni as fun
from funzioni import dist as Xdata
from vns import variable_neighborhood_search as vns
from path_relinking import path_relinking as p_rel


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
    lim = m + alfa*(M-m)

    for i in range(len(rank)):
        if rank[i][0] <= lim :
            rcl.append(rank[i])

    return rcl


#Local Search : Ricerca esaustiva degli ottimi locali
def ls_2_opt(attr_tour, count):

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
    fun.write_res( best_route, "2-opt", count )
    return best_route

def ls_double_bridge(attr_tour, count):

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
    fun.write_res( best_route, "DoubleBr", count)
    return best_route
#-

#Principal Function
def greedy_randomized_adaptive_search_procedure(iterations, alfa):
    
    count = 0
    #start_tour = fun.first_op()
    best_solution = [[], 0, 0]

    s = int(input("\nSelect what algorithms' sequence you want to use.\n\n\t1) GRASP with exaustive local search\n\t2) GRASP with stock-VNS\n\n"))

    while (iterations > count):
        first_sol = find_solution(alfa)
    
        if(len(first_sol[0])>=5):
            if(s == 1):
                #exaustive local search
                candidate = ls_double_bridge( ls_2_opt( first_sol ,count) , count)
            elif(s == 2):
                #stock-VNS
                candidate = vns(first_sol)
        else:
            continue

        if ( candidate[1] > best_solution[1] or (candidate[1] == best_solution[1] and candidate[2] < best_solution[2])):    
            best_solution = fun.deepcopy(candidate)
            count += 1
            fun.write_res( best_solution, s, count )
            print('Iteration =', count, ' --> Satisfaction =', best_solution[1], ', Time =', best_solution[2])
        else:
            count += 1
            print('Iteration =', count, '   --> The best solution is the same that was found in last iteration!')
            if(s == 3 or s == 4):
                best_solution = p_rel(candidate, best_solution)
                if ( candidate[1] > best_solution[1] or (candidate[1] == best_solution[1] and candidate[2] < best_solution[2])):   
                    print("\n\t\tBut Path relinking helped to find a better solution...\n")
                    fun.write_res( best_solution, s, count )
                    print(' -> Satisfaction =', best_solution[1], ', Time =', best_solution[2])

    print("\n\nBest Solution Found\n", best_solution)
    return best_solution
#-

#Construciton of the initial solution
def find_solution(alfa):

    seed = [[], 0, 0]
    sequence = [0]
    time = 0
 
    while(True):
  
        RCL = neighborhood(sequence[-1], time/60, alfa)
        #prendo un elemento casuale dalla RCL
        next = fun.r.choice(RCL)

        while fun.end_tour(time/60, sequence[-1], next[1]) : 
            #se trovo un'attrazione che non è raggiungibile dal nodo precedente allora la rimuovo dalla RCL e continuo a cercare se trovo una possibile attrazione da visitare
            RCL.remove(next)
            if len(RCL) == 0:
                break
            next = fun.r.choice(RCL)
        
        #se la RCL è vuota allora non ho trovato nessuna possibile attrazione da visitare
        if (len(RCL) == 0):
            break
        
        time += next[0]
        sequence.append(next[1])    
        
    #solution created
    sequence.append(sequence[0])
    seed[0] = sequence
    seed = fun.time_and_sat_calc(seed)
    if len(seed [0]) <5:
        print( "ops", seed[0] )
    return seed


#MAIN
tour = greedy_randomized_adaptive_search_procedure(iterations = 1000, alfa = 0.5)