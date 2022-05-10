#Simple GRASP with two type of greedy, a VNS algorithm can be used
import funzioni as fun
from funzioni import dist as Xdata
from vns import variable_neighborhood_search as vns 

#Greedy
def neighborhood(node = 0):

    rank = [] 
    for i in range(1, Xdata.shape[0]):
        if (i == node) :
            continue
        rank.append( (Xdata[i,node], i) )

    rank.sort()

    return rank

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
def ls_2_opt(attr_tour):

    best_route = fun.deepcopy(attr_tour)
    
    for i in range(0, len(attr_tour[0]) - 2):
        for j in range(2, len(attr_tour[0]) - 1):
            tour = fun.deepcopy(attr_tour) 
            if( i == j-1 or i == j+1 or i == j):
                continue
            tour[0][(i+1):(j+1)] = list(reversed(tour[0][(i+1):(j+1)])) #inverto una parte della lista perchè scambio gli archi
            tour = fun.time_and_sat_calc(tour) 
            if (best_route[1] < tour[1]):
                best_route = fun.deepcopy(tour)

    return best_route

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
                    tour = fun.time_and_sat_calc(tour)
                    if (best_route[1] < tour[1]):
                        best_route = fun.deepcopy(tour)
    
    return best_route
#-

#Principal Function
def greedy_randomized_adaptive_search_procedure(start_tour, iterations, greediness_value):
    count = 0
    best_solution = fun.deepcopy(start_tour)

    greedy = str(input(
        "\nChoose the Greedy Algorithm:\n -Press 'N' for Neighborhood greedy or 'R' for Ratio greedy.-\n"))

    while (count < iterations):
        first_sol = find_solution(greediness_value, greedy)
        #local search without VNS
        candidate = ls_double_bridge( ls_2_opt( first_sol ) )
        #local search with VNS
        candidate = vns(Xdata, first_sol)

        if ( (candidate[1] / candidate[2]) > (best_solution[1] / best_solution[2]) ):
            best_solution = fun.deepcopy(candidate)
            count += 1
            #fun.write_res( best_solution, (str(greedy)), count )
            print('Iteration =', count, '-> Satisfaction =', best_solution[1], ', Time =', best_solution[2])

    print("Best Solution =\n", best_solution)
    return best_solution

def find_solution(greediness_value, greedy):
    seed = [[],float("inf"), float("-inf")]
    
    sequence = [0]
    
    remaining = []
    remaining = list(u for u in range(1,Xdata.shape[0]))#lista con i nodi che non sono presenti nella soluzione 
    
    time = 0
    
    for i in range(0, Xdata.shape[0]-1):
        count = 0
        rand = round(fun.r.random(), 2) #coefficiente casuale con due cifre dopo la virgola

        if(len(remaining) == 1):#se rimane un solo nodo non visitato lo inserisco nel tour e chiudo il ciclo
            time += Xdata[sequence[-1], remaining[0]]
            sequence.append(remaining[0])
            break
        
        #greedy construction
        if (rand <= greediness_value and len(sequence) < Xdata.shape[0]):
            if(greedy == 'N' or 'n'):
                next = neighborhood(sequence[-1]) 
            elif(greedy == 'R' or 'r'):
                next = ratio(sequence[-1])

            while ( (next[count][1] in sequence) and count < 33 ):
                count += 1
            if( count > 33 or ( len(sequence) > 2 and fun.end_tour(time/60,sequence[-1], next[count][1]) ) ):
                break
            else:
                time += next[count][0]
                sequence.append(next[count][1])
                remaining.remove(next[count][1])

        #random construction
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
    #solution created
    sequence.append(sequence[0])
    seed[0] = sequence
    seed = fun.time_and_sat_calc(seed)
    return seed

#MAIN
tour = greedy_randomized_adaptive_search_procedure(start_tour = fun.first_op() , iterations = 1000, greediness_value = 0.5)