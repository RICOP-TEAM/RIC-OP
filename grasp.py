import funzioni as fun
from funzioni import dist as Xdata


#Construciton of the initial solution
def find_solution(alfa):

    start = fun.time()
    seed = [[], 0, 0]
    sequence = [0]
    time = 0
 
    while(True):
  
        RCL = neighborhood(sequence, time/60, alfa)
        #prendo un elemento casuale dalla RCL
        next = fun.r.choice(RCL)

        while fun.end_tour(time/60, sequence[-1], next[1]): 
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
        
    neig[str(alfa)][str(esec)].append([fun.time()-start, seed[1], seed[2], seed[0], False])#exectime, sat, tourtime, how many times the best
    with open("neigh_data.json","w") as data_neigh:
        fun.json.dump(neig, data_neigh, indent=4)

    return seed
#-


#Greedy
def neighborhood(sequence, time, alfa):
    node = sequence[-1]
    rank = []
    rcl = [] 
    for i in range(1, Xdata.shape[0]):
        if i == node or i in sequence :
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
#-


#Local Search : Ricerca esaustiva degli ottimi locali
def ls_2_opt(attr_tour):
    start = fun.time()

    best_route = fun.deepcopy(attr_tour)
    
    for i in range(0, len(attr_tour[0]) - 2):
        for j in range(2, len(attr_tour[0]) - 1):
            tour = fun.deepcopy(attr_tour) 
            if( i == j-1 or i == j+1 or i == j):
                continue
            tour[0][(i+1):(j+1)] = list(reversed(tour[0][(i+1):(j+1)])) #inverto una parte della lista perchè scambio gli archi
            tour = fun.time_and_sat_calc(tour) 
            
            if ( tour[1] > best_route[1] or (tour[1] == best_route[1] and tour[2] < best_route[2])):    
                best_route = fun.deepcopy(tour)

    opt2[str(alfa)][str(esec)].append([fun.time()-start, best_route[1], best_route[2], best_route[0], False])#exectime, sat, tourtime
    with open("2opt_data.json","w") as data_2opt:
        fun.json.dump(opt2, data_2opt, indent=4)
    
    return best_route

def ls_double_bridge(attr_tour):

    start = fun.time() 

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
                    
                    if ( tour[1] > best_route[1] or (tour[1] == best_route[1] and tour[2] < best_route[2])):    
                        best_route = fun.deepcopy(tour)

    dbrdg[str(alfa)][str(esec)].append([fun.time()-start, best_route[1], best_route[2], best_route[0], False])#exectime, sat, tourtime
    with open("dbridge_data.json","w") as data_dbridge:
            fun.json.dump(dbrdg, data_dbridge, indent=4)
    
    return best_route
#-

#VNS
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

    dvns[str(alfa)][str(esec)].append([fun.time()-start, solution[1], solution[2], solution[0],False])#exectime, sat, tourtime
    with open("vns_data.json","w") as data_vns:
        fun.json.dump(dvns, data_vns,  indent=4)
    
    return solution
#-


#Principal Function
def greedy_randomized_adaptive_search_procedure(iterations, alfa):
    
    count = 0
    best_solution = [[], 0, 0]

    while (iterations > count):

        count+=1
        first_sol = find_solution(alfa)
    
        if(len(first_sol[0])>=5):            
            opt_2_sol = ls_2_opt(first_sol)
            dbridge_sol = ls_double_bridge(first_sol)
            vns_sol = variable_neighborhood_search(first_sol)
        else:
            continue

        #comparing solutions
        if (opt_2_sol[1] > dbridge_sol[1] or (opt_2_sol[1] == dbridge_sol[1] and opt_2_sol[2] < dbridge_sol[2])):
            candidate = fun.deepcopy(opt_2_sol)
            opt2[str(alfa)][str(esec)][count-1][4] = True
        else:
            candidate = fun.deepcopy(dbridge_sol)
            dbrdg[str(alfa)][str(esec)][count-1][4] = True


        if ( vns_sol[1] > candidate[1] or ( vns_sol[1] == candidate[1] and vns_sol[2] < candidate[2])):
            candidate = fun.deepcopy(vns_sol) 
            dvns[str(alfa)][str(esec)][count-1][4] = True

        #comparing best solution in this iteration with global best solution
        if ( candidate[1] > best_solution[1] or (candidate[1] == best_solution[1] and candidate[2] < best_solution[2])):    
            best_solution = fun.deepcopy(candidate)
            print(f'Iteration = {count} --> Satisfaction =  {best_solution[1]}; Time = {best_solution[2]} \n\n')
        else:
            print(f'Iteration = {count} \t--> The best solution is the same that was found in last iteration!\n\n')
        
        print('___________________\n\n')

    print("---END---")
    print(f"\n\n---\n\nBest Solution Found\n{best_solution}")
    return best_solution


#MAIN

neig = {
    "0":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.25":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.5":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.75":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "1":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    }
    }
opt2 = {
    "0":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.25":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.5":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.75":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "1":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    }
    }
dbrdg = {
    "0":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.25":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.5":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.75":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "1":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    }
    }
dvns = {
    "0":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.25":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.5":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "0.75":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    },
    "1":{
        "1":[],
        "2":[],
        "3":[],
        "4":[],
        "5":[],
        "6":[],
        "7":[],
        "8":[],
        "9":[],
        "10":[]
    }
    }

for esec in range(1,11):
    for alfa in [0, 0.25, 0.5, 0.75, 1]:
        tour = greedy_randomized_adaptive_search_procedure(iterations = 100, alfa = alfa)
        print ('ok')
        

