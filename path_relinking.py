import funzioni as fun

def path_relinking(initial_solution, final_solution):
    
    tour = fun.deepcopy(initial_solution)
    best = []

    for j in range(1,len(tour[0])-1):
    
        if tour[0][j] != final_solution[0][j] :
            temp = fun.deepcopy(tour)
            temp[0][j] = final_solution[0][j] 
            temp = fun.time_and_sat_calc(temp)
    
            if len(best) == 0:
                best = fun.deepcopy(temp)
    
            if temp[1] > best[1] or (temp[1] == best[1] and temp[2] < best[2]):
                best = fun.deepcopy(temp)
    
    tour = fun.deepcopy(best)
                

    return tour