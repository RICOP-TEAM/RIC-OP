def remove_redundancy(self, solution):

    for i in solution:
        sol_aux = solution.copy()
        sol_aux.remove(i)
        if self.is_complete(sol_aux):
            solution = sol_aux.copy()

    return solution


def path_relinking(self, initial_solution, final_solution):

    sym_dif = initial_solution.symmetric_difference(final_solution)

    cost_init_sol = self.evaluate_solution(initial_solution)
    cost_final_sol = self.evaluate_solution(final_solution)

    best_cost = min(cost_init_sol, cost_final_sol)

    if cost_init_sol < cost_final_sol:
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

