import funzioni as fun

def path_relinking(initial_solution, final_solution):
    
    tour = fun.deepcopy(initial_solution)
    min_len = min(len(initial_solution[0]), len(final_solution[0]))

    while (tour != final_solution):#crea funzione 'condition' per uscire dal while

        best = [[],0, 0]
        for j in range(1, min_len-1):
        
            if tour[0][j] != final_solution[0][j] :
                temp = fun.deepcopy(tour)
                temp[0][j] = final_solution[0][j] 
                temp = fun.time_and_sat_calc(temp)

                if  best[2] == 0 or (temp[1] > best[1] or (temp[1] == best[1] and temp[2] < best[2])):
                    best = fun.deepcopy(temp)
                    tour = fun.deepcopy(best)

        
        if (tour[1] > final_solution[1] or (tour[1] == final_solution[1] and tour[2] < final_solution[2])):
            break
    return tour