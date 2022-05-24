import funzioni as fun

def path_relinking(self, initial_solution, final_solution):

    sym_dif = initial_solution.symmetric_difference(final_solution)

    initial_solution = fun.time_and_sat_calc(initial_solution)
    final_solution = fun.time_and_sat_calc(final_solution)

    best_cost = max(initial_solution[1], final_solution[1])

    if initial_solution[1] > final_solution[1]:
        best_sol = initial_solution
    else:
        best_sol = final_solution

    current_sol = initial_solution.copy()

    best_dif_cost = 0
    best_change_cost = best_cost

    while len(sym_dif) > 0:

        new_it = True

        for i in sym_dif:

            if i in current_sol:
                dif_cost = -self.subsets_cost[i]

            else:
                dif_cost = self.subsets_cost[i]

            current_sol.symmetric_difference_update({i})

            if (dif_cost < best_dif_cost or new_it) and self.is_complete(current_sol):
                new_it = False

                best_i = i
                best_dif_cost = dif_cost

            current_sol.symmetric_difference_update({i})

        current_sol.symmetric_difference_update({best_i})

        best_change_cost += best_dif_cost

        if best_change_cost < best_cost:
            best_cost = best_change_cost
            best_sol = current_sol.copy()

        sym_dif.remove(best_i)

    return best_sol