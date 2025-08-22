import pulp

# ------ Data -------
orders = ['O1', 'O2', 'O3', 'O4']
machines = ['M1', 'M2']

processing_time = {'O1': 5, 'O2': 7, 'O3': 4, 'O4': 6}
due_date = {'O1': 12, 'O2': 15, 'O3': 10, 'O4': 20}
priority = {'O1': 3, 'O2': 2, 'O3': 4, 'O4': 1}

# Setup times (symmetric for demo, can be asymmetric)
setup = {}
for i in orders:
    for k in orders:
        setup[(i, k)] = 2 if i != k else 0

H = 1000  # big-M

# ----- Model ------
prob = pulp.LpProblem("OrderDrivenScheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, m) for i in orders for m in machines), 0, 1, pulp.LpBinary)  # assignment
S = pulp.LpVariable.dicts("S", orders, lowBound=0)  # start times
C = pulp.LpVariable.dicts("C", orders, lowBound=0)  # completion times
T = pulp.LpVariable.dicts("T", orders, lowBound=0)  # tardiness

# y[i,k,m] = 1 if order i precedes order k on machine m
y = pulp.LpVariable.dicts("y", ((i, k, m) for i in orders for k in orders for m in machines), 0, 1, pulp.LpBinary)

# Objective: minimize weighted tardiness + setups
prob += (
     pulp.lpSum(priority[i] * T[i] for i in orders) + 
     pulp.lpSum(setup[(i, k)] * y[(i, k, m)] for i in orders for k in orders for m in machines)
)

# ------ Constraints --------

# Each order assigned to exactly one machine
for i in orders:
    prob += pulp.lpSum(x[(i, m)] for m in machines) == 1, f"Assign_{i}"

# Completion definition
for i in orders:
    prob += C[i] == S[i] + pulp.lpSum(x[(i, m)] * processing_time[i] for m in machines), f"Completion_{i}"

# Tardiness definition
for i in orders:
    prob += T[i] >= C[i] - due_date[i], f"Tardiness_{i}"

# Sequencing constraints
for m in machines:
    for i in orders:
        for k in orders:
            if i == k:
                continue # skip self-precedence
            # if i precedes k on m
            prob += S[k] >= C[i] + setup[(i, k)] - H * (1 - y[(i, k, m)]), f"Seq_{i}_{k}_{m}"
            # Linking y to assignments
            prob += y[(i, k, m)] <= x[(i, m)], f"Link1_{i}_{k}_{m}"
            prob += y[(i, k, m)] <= x[(k, m)], f"Link2_{i}_{k}_{m}"
        
# Solve
solver = pulp.PULP_CBC_CMD(msg=True)
prob.solve(solver)

# ------- Results -----------
print("Status:", pulp.LpStatus[prob.status])
print("Objective (Weighted Tardiness + Setup):", pulp.value(prob.objective))

print("\nSchedule:")
for i in orders:
    assigned_m = [m for m in machines if pulp.value(x[(i, m)]) > 0.5]
    print(f"{i}: Machine={machines}, Start={pulp.value(S[i]):.2f}, Finish={pulp.value(C[i]):.2f}, Tardiness={pulp.value(T[i]):.2f}")

print("\nSequencing Decisions:")
for m in machines:
    seq_pairs = [(i, k) for i in orders for k in orders if i != k and pulp.value(y[(i, k, m)]) > 0.5]
    if seq_pairs:
        print(f"{m}: {seq_pairs}")
    else:
        print(f"{m}: No sequence enforced")