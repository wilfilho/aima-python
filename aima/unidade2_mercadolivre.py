from csp import CSP
import math
import time

orders_data = {
    "O0": [3, 0, 1, 0, 0],
    "O1": [0, 1, 0, 1, 0],
    "O2": [0, 0, 1, 0, 2],
    "O3": [1, 0, 2, 1, 1],
    "O4": [0, 1, 0, 0, 0]
}
corridors_data = {
    "A0": [2, 1, 1, 0, 1],
    "A1": [2, 1, 2, 0, 1],
    "A2": [0, 2, 0, 1, 2],
    "A3": [2, 1, 0, 1, 1],
    "A4": [0, 1, 2, 1, 2]
}
LB, UB = 5, 12
orders = list(orders_data.keys())
corridors = list(corridors_data.keys())
variables = orders + corridors
domains = {var: [0, 1] for var in variables}
neighbors = {var: [w for w in variables if w != var] for var in variables}

def constraints(assignment):
    if all(o in assignment for o in orders):
        total = sum(sum(orders_data[o]) for o in orders if assignment[o] == 1)
        if total < LB or total > UB:
            return False
    if all(var in assignment for var in variables):
        num_items = len(next(iter(orders_data.values())))
        for i in range(num_items):
            req = sum(assignment[o] * orders_data[o][i] for o in orders)
            avail = sum(assignment[a] * corridors_data[a][i] for a in corridors)
            if req > avail:
                return False
    return True

def objective_tuple(assignment):
    total = sum(assignment[o] * sum(orders_data[o]) for o in orders)
    num_corridors = sum(assignment[a] for a in corridors)
    if num_corridors == 0:
        return (-math.inf, -math.inf)
    return (total / num_corridors, total)

class OrderCSP(CSP):
    def nconflicts(self, var, val, assignment):
        local = assignment.copy()
        local[var] = val
        return 1 if not constraints(local) else 0
    def assign(self, var, val, assignment):
        assignment[var] = val
    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
    def select_unassigned_variable(self, assignment):
        for var in self.variables:
            if var not in assignment:
                return var
        return None

def all_solutions(csp, assignment={}):
    if len(assignment) == len(csp.variables):
        if constraints(assignment):
            yield assignment.copy()
    else:
        var = csp.select_unassigned_variable(assignment)
        for val in csp.domains[var]:
            if csp.nconflicts(var, val, assignment) == 0:
                assignment[var] = val
                yield from all_solutions(csp, assignment)
                del assignment[var]

start_time = time.time()
csp_instance = OrderCSP(variables, domains, neighbors, lambda A, a, B, b: True)
solutions = list(all_solutions(csp_instance, {}))
print("Todas as soluções encontradas:")
for idx, sol in enumerate(solutions):
    obj = objective_tuple(sol)
    selected_orders = [o for o in orders if sol[o] == 1]
    selected_corridors = [a for a in corridors if sol[a] == 1]
    print(f"Solução {idx+1}: Pedidos {selected_orders}, Corredores {selected_corridors}, Objetivo (média, total) = {obj}")
best_solution = None
best_obj = (-math.inf, -math.inf)
for sol in solutions:
    obj_val = objective_tuple(sol)
    if obj_val > best_obj:
        best_obj = obj_val
        best_solution = sol.copy()
end_time = time.time()
exec_time = end_time - start_time
if best_solution:
    selected_orders = [o for o in orders if best_solution[o] == 1]
    selected_corridors = [a for a in corridors if best_solution[a] == 1]
    total_units = sum(sum(orders_data[o]) for o in selected_orders)
    num_corridors = len(selected_corridors)
    avg_value = best_obj[0]
    print("\n==================== SOLUÇÃO ÓTIMA ====================")
    print("Pedidos selecionados:", selected_orders)
    print("Corredores selecionados:", selected_corridors)
    print("Número de corredores selecionados:", num_corridors)
    print("Total de unidades dos pedidos selecionados:", total_units)
    print("Valor objetivo (média de itens por corredor):", avg_value)
    print("Tempo de execução: {:.4f} segundos".format(exec_time))
    print("==========================================================")
else:
    print("Nenhuma solução encontrada.")
