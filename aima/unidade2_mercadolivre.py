from csp import CSP
import math
import time

class Data:
    def __init__(self):
        self.orders = {
            "O0": [3, 0, 1, 0, 0],
            "O1": [0, 1, 0, 1, 0],
            "O2": [0, 0, 1, 0, 2],
            "O3": [1, 0, 2, 1, 1],
            "O4": [0, 1, 0, 0, 0]
        }
        self.corridors = {
            "A0": [2, 1, 1, 0, 1],
            "A1": [2, 1, 2, 0, 1],
            "A2": [0, 2, 0, 1, 2],
            "A3": [2, 1, 0, 1, 1],
            "A4": [0, 1, 2, 1, 2]
        }
        self.lb, self.ub = 5, 12
        self.order_ids = list(self.orders.keys())
        self.corridor_ids = list(self.corridors.keys())
        self.variables = self.order_ids + self.corridor_ids
        self.domains = {var: [0, 1] for var in self.variables}
        self.neighbors = {var: [v for v in self.variables if v != var] for var in self.variables}
        self.num_items = len(next(iter(self.orders.values())))

class Validator:
    def __init__(self, data):
        self.data = data
    def validate(self, assignment):
        if all(order in assignment for order in self.data.order_ids):
            total = sum(sum(self.data.orders[order]) for order in self.data.order_ids if assignment[order] == 1)
            if total < self.data.lb or total > self.data.ub:
                return False
        if all(var in assignment for var in self.data.variables):
            for i in range(self.data.num_items):
                req = sum(assignment[order] * self.data.orders[order][i] for order in self.data.order_ids)
                avail = sum(assignment[corridor] * self.data.corridors[corridor][i] for corridor in self.data.corridor_ids)
                if req > avail:
                    return False
        return True

class Objective:
    def __init__(self, data):
        self.data = data
    def evaluate(self, assignment):
        total = sum(assignment[order] * sum(self.data.orders[order]) for order in self.data.order_ids)
        active = sum(assignment[corridor] for corridor in self.data.corridor_ids)
        if active == 0:
            return (-math.inf, -math.inf)
        return (total / active, total)

class OrderCorridorCSP(CSP):
    def __init__(self, data, validator):
        super().__init__(data.variables, data.domains, data.neighbors, lambda A, a, B, b: True)
        self.validator = validator
    def nconflicts(self, var, val, assignment):
        local = assignment.copy()
        local[var] = val
        return 1 if not self.validator.validate(local) else 0
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

class Solver:
    def __init__(self, csp, validator):
        self.csp = csp
        self.validator = validator
    def search(self, assignment={}):
        if len(assignment) == len(self.csp.variables):
            if self.validator.validate(assignment):
                yield assignment.copy()
        else:
            var = self.csp.select_unassigned_variable(assignment)
            for val in self.csp.domains[var]:
                if self.csp.nconflicts(var, val, assignment) == 0:
                    assignment[var] = val
                    yield from self.search(assignment)
                    del assignment[var]

class Runner:
    def __init__(self):
        self.data = Data()
        self.validator = Validator(self.data)
        self.objective = Objective(self.data)
        self.csp = OrderCorridorCSP(self.data, self.validator)
        self.solver = Solver(self.csp, self.validator)
    def run(self):
        start = time.time()
        solutions = list(self.solver.search({}))
        best_sol = None
        best_obj = (-math.inf, -math.inf)
        for sol in solutions:
            obj_val = self.objective.evaluate(sol)
            if obj_val > best_obj:
                best_obj = obj_val
                best_sol = sol.copy()
        elapsed = time.time() - start
        orders_sel = [order for order in self.data.order_ids if best_sol[order] == 1]
        corridors_sel = [corridor for corridor in self.data.corridor_ids if best_sol[corridor] == 1]
        total_units = sum(sum(self.data.orders[order]) for order in orders_sel)
        count_corridors = len(corridors_sel)
        avg_val = best_obj[0]
        print("==================== SOLUÇÃO ÓTIMA ====================")
        print("Pedidos selecionados:", orders_sel)
        print("Corredores selecionados:", corridors_sel)
        print("Número de corredores selecionados:", count_corridors)
        print("Total de unidades dos pedidos selecionados:", total_units)
        print("Valor objetivo (média de itens por corredor):", avg_val)
        print("Tempo de execução: {:.4f} segundos".format(elapsed))
        print("==========================================================")

if __name__ == "__main__":
    Runner().run()
