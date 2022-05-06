import funzioni as fun
from funzioni import dist as Xdata

def satisfaction_calc(tour):
    sat = 0
    time = 0

    for k in range(1,len(tour[0])):
        time += Xdata[tour[0][k-1],tour[0][k]]
        open = fun.open_attr(tour[0][k], time/60)
        if(open == 0):
            sat += fun.Grad_pond[tour[0][k]]
        else:
            time += open #attrazione chiusa --> *PENALITA'* = aumenta il tempo trascorso

    tour[2] = time / 60
    M=max(fun.Grad_pond)
    m=min(fun.Grad_pond)
    #sat -= penalty * (M + m)/2 #la penalità corrisponde all'aumento di tempo passato a causa dell'attesa che l'attrazione sia aperta
    tour[1] = sat
    return tour

def first_op():
    
    seed=[[],float("inf"), float("-inf")]
    sequence=[0]
    time=0
    
    while(True):
        n=0
        candidati=[]

        for i in range(len(fun.f["attrazioni"])):
            node=i+1   
            open = fun.open_attr(node, time/60)
            if( (node not in sequence) and open == 0 ):
                candidati.append((fun.f["attrazioni"][i]["tw"]["t_inf"], Xdata[sequence[-1], node], node))
            elif (open > 0):
                candidati.append((fun.f["attrazioni"][i]["tw"]["t_inf"], (Xdata[sequence[-1], node] + open), node))
        
        candidati=sorted(candidati, key=lambda x:(x[0],x[1])) #ordino la lista di candidati possibili in base a chi apre prima
        
        while( n<len(candidati) and fun.end_tour(time/60, sequence[-1], candidati[n][2])):
            n += 1 

        if(n > len(candidati) - 1):
            break

        time += candidati[n][1]
        sequence.append(candidati[n][2])

    sequence.append(0)
    
    seed[0] = sequence
    seed = satisfaction_calc(seed)

    #fun.write_res( seed, "start", 0 )
    #fun.wexcel( seed, "start", 0 )

    return seed

#Greedy
# Function: Rank Cities by Distance
def neighborhood(node = 0):

    rank = [] 
    for i in range(1, Xdata.shape[0]):
        if (i == node) :
            continue
        rank.append( (Xdata[i,node], i) )

    rank.sort()

    return rank

# Function: Rank Cities by Ratio: Grad_pond/Ttot
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

#Local Search
# 2_opt
def ls_2_opt(attr_tour):

    best_route = fun.deepcopy(attr_tour)
    
    for i in range(0, len(attr_tour[0]) - 2):
        for j in range(2, len(attr_tour[0]) - 1):
            tour = fun.deepcopy(attr_tour) 
            if( i == j-1 or i == j+1 or i == j):
                continue
            tour[0][(i+1):(j+1)] = list(reversed(tour[0][(i+1):(j+1)])) #inverto una parte della lista perchè scambio gli archi
            tour = satisfaction_calc(tour) 
            if (best_route[1] < tour[1]):
                best_route = fun.deepcopy(tour)

    return best_route

# Double Bridge
def ls_double_bridge(attr_tour):

    tour=fun.deepcopy(attr_tour)
    best_route=fun.deepcopy(tour)

    for i in range(0,len(tour[0])-7):
        for j in range(i+2,len(tour[0])-5):
            for k in range(j+2,len(tour[0])-3):
                for l in range(k+2,len(tour[0])-1):
                    if(i==0 and l==len(tour[0])-2):
                        continue
                    tour[0] = list(attr_tour[0][:(i+1)] + attr_tour[0][(k+1):(l+1)] + attr_tour[0][(j+1):(k+1)] + attr_tour[0][(i+1):(j+1)] + attr_tour[0][(l+1):])
                    tour = satisfaction_calc(tour)
                    if (best_route[1] < tour[1]):
                        best_route = fun.deepcopy(tour)
    
    return best_route
#-

#Principal Function
def greedy_randomized_adaptive_search_procedure(start_tour, iterations, greediness_value):
    count = 0
    best_solution = fun.deepcopy(start_tour)

    # N 1 --> Neighbor + 2-opt      
    # N 2 --> Neighbor + Double Bridge
    # R 1 --> Ratio + 2-opt
    # R 2 --> Ratio + Double Bridge

    greedy = str(input("\nChoose the Greedy Algorithm:\n -Press 'N' for Neighborhood greedy or 'R' for Ratio greedy.-\n"))
    ls = str(input("\nChoose the Local Search Algorithm:\n -Press '1' for 2-OPT or '2' for Double Bridge-\n"))

    while (count < iterations):
        
        #start_time=fun.time()

        if(ls == '1'):
            candidate = ls_2_opt(find_solution(greediness_value, greedy)) 
        elif(ls == '2'):
            candidate = ls_double_bridge(find_solution(greediness_value, greedy))
    
        '''
            if (candidate[1] > best_solution[1]):
                best_solution = fun.deepcopy(candidate) 
                a = 0
            elif(candidate[1] == best_solution[1] and candidate[2] < best_solution[2]):
                best_solution = fun.deepcopy(candidate) 
                a = 0
            else:
                a = 1
        '''
    
        '''
                rcl_list = []
                start_time=t.time()
                for i in range(0, n_sol):
                    rcl_list.append(find_solution(greediness_value ))
                #candidate = int(fun.r.sample(list(range(0,rcl)), 1)[0]) #viene presa una soluzione candidato in modo casuale
                rcl_list = sorted(rcl_list[:],key=lambda x:x[1], reverse=True)

                for candidate in range(10): #-----> DIFFERENZA SOSTANZIALE RISPETTO ALLE PRECEDENTI RIGHE
                    start_tour=ls_2_opt(rcl_list[candidate])
                    if (start_tour[1] > best_solution[1]):
                        best_solution = fun.deepcopy(start_tour) 
        '''
        if ( (candidate[1] / candidate[2]) > (best_solution[1] / best_solution[2]) ):
            best_solution = fun.deepcopy(candidate)
            count += 1
            fun.write_res( best_solution, (str(greedy)+str(ls)), count )
            print('Iteration =', count, '-> Satisfaction =', best_solution[1], ', Time =', best_solution[2])

    print("Best Solution =\n", best_solution)
    return best_solution

def find_solution(greediness_value, greedy):
    seed = [[],float("inf"), float("-inf")]
    
    sequence = []
    sequence.append(0)
    
    remaining = []
    remaining=list(u for u in range(1,Xdata.shape[0]))
    
    time=0
    
    for i in range(0, Xdata.shape[0]-1):
        count = 0
        rand = fun.r.random()#coefficiente casuale

        if(len(remaining) == 1):
            time += Xdata[sequence[-1], remaining[0]]
            sequence.append(remaining[0])
            break
        
        if (rand <= greediness_value and len(sequence) < Xdata.shape[0]):

            #choose your greedy
            if(greedy == 'N'):
                next = neighborhood(sequence[-1]) 
            elif(greedy == 'R'):
                next = ratio(sequence[-1])
              

            while ( (next[count][1] in sequence) and count < 33 ):
                count += 1
            if( count > 33 or ( len(sequence) > 2 and fun.end_tour(time/60,sequence[-1], next[count][1]) ) ):
                break
            else:
                time += next[count][0]
                sequence.append(next[count][1])
                remaining.remove(next[count][1])
        
        elif (rand > greediness_value and len(sequence) < Xdata.shape[0]):
            next = int(fun.r.sample(remaining, 1)[0])
            while next in sequence:
                next = int(fun.r.sample(remaining, 1)[0])
            if( len(sequence) > 2 and fun.end_tour(time/60,sequence[-1], next) ): #if there isn't other time to continue the tour we close the loop 
                break
            else:
                time += Xdata[sequence[-1], next]
                sequence.append(next)
                remaining.remove(next)
    
    sequence.append(sequence[0])
    seed[0] = sequence
    seed = satisfaction_calc(seed)
    return seed

#MAIN
#tour = greedy_randomized_adaptive_search_procedure(start_tour = first_op() , iterations = 1000, greediness_value = 0.5)
