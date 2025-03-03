
# part b
import pandas as pd
import gurobipy as gp
from gurobipy import Model, GRB, quicksum

# Load data from CSV files
farms = pd.read_csv('/Users/huiyisang/Desktop/Model & Application/farms.csv')
processing = pd.read_csv('/Users/huiyisang/Desktop/Model & Application/processing.csv')
centers = pd.read_csv('/Users/huiyisang/Desktop/Model & Application/centers.csv')

# Extract data from datasets
num_farms = len(farms)
num_processing = len(processing)
num_centers = len(centers)


# Decision variables:
# x[i][j]: amount transported from farm i to processing facility j
# y[j][k]: amount transported from processing facility j to home center k

# Create model
model = gp.Model("Transportation_Procurement_Plan")

# Decision variables
x = model.addVars(num_farms, num_processing, lb=0, vtype=GRB.CONTINUOUS, name="FarmToProc")
y = model.addVars(num_processing, num_centers, lb=0, vtype=GRB.CONTINUOUS, name="ProcToCenter")

# Objective function: Minimize total cost
model.setObjective(
    gp.quicksum(
        x[i, j] * (farms[f'Transport_Cost_To_Plant_{j+1}'][i] + farms['Cost_Per_Ton'][i] + processing['Processing_Cost_Per_Ton'][j])
        for i in range(num_farms) for j in range(num_processing)
    ) +
    gp.quicksum(
        y[j, k] * (processing[f'Transport_Cost_To_Center_{k+1}'][j])
        for j in range(num_processing) for k in range(num_centers)
    ),
    GRB.MINIMIZE
)

# Constraints
# Supply constraints at farms: Cannot exceed available material
for i in range(num_farms):
    model.addConstr(gp.quicksum(x[i, j] for j in range(num_processing)) <= farms['Bio_Material_Capacity_Tons'][i], name=f"FarmSupply_{i}")

# Capacity constraints at processing facilities
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) <= processing['Capacity_Tons'][j], name=f"ProcCapacity_{j}")

# Demand constraints at home centers
for k in range(num_centers):
    model.addConstr(gp.quicksum(y[j, k] for j in range(num_processing)) == centers['Requested_Demand_Tons'][k], name=f"CenterDemand_{k}")

# Linking constraint: processed material must be transported to centers
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) == gp.quicksum(y[j, k] for k in range(num_centers)), name=f"Balance_{j}")

# Optimize model
model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    print(f"Optimal Total Cost: {model.objVal}")
    for i in range(num_farms):
        for j in range(num_processing):
            if x[i, j].x > 0:
                print(f"Farm {i} to Processing {j}: {x[i, j].x}")
    for j in range(num_processing):
        for k in range(num_centers):
            if y[j, k].x > 0:
                print(f"Processing {j} to Center {k}: {y[j, k].x}")
else:
    print("No optimal solution found.")








# part c
# Create model
model = gp.Model("Transportation_Procurement_Plan")

# Decision variables
x = model.addVars(num_farms, num_processing, lb=0, vtype=GRB.CONTINUOUS, name="FarmToProc")
y = model.addVars(num_processing, num_centers, lb=0, vtype=GRB.CONTINUOUS, name="ProcToCenter")

# Objective function: Minimize total cost
model.setObjective(
    gp.quicksum(
        x[i, j] * (farms[f'Transport_Cost_To_Plant_{j+1}'][i] + farms['Cost_Per_Ton'][i] + processing['Processing_Cost_Per_Ton'][j])
        for i in range(num_farms) for j in range(num_processing)
    ) +
    gp.quicksum(
        y[j, k] * (processing[f'Transport_Cost_To_Center_{k+1}'][j])
        for j in range(num_processing) for k in range(num_centers)
    ),
    GRB.MINIMIZE
)

# Constraints
# Supply constraints at farms: Cannot exceed available material
for i in range(num_farms):
    model.addConstr(gp.quicksum(x[i, j] for j in range(num_processing)) <= farms['Bio_Material_Capacity_Tons'][i], name=f"FarmSupply_{i}")

# Capacity constraints at processing facilities
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) <= processing['Capacity_Tons'][j], name=f"ProcCapacity_{j}")

# Demand constraints at home centers
for k in range(num_centers):
    model.addConstr(gp.quicksum(y[j, k] for j in range(num_processing)) == centers['Requested_Demand_Tons'][k], name=f"CenterDemand_{k}")

# Linking constraint: processed material must be transported to centers
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) == gp.quicksum(y[j, k] for k in range(num_centers)), name=f"Balance_{j}")
# Optimize model
model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    print(f"Optimal Total Cost: {model.objVal}")
    for i in range(num_farms):
        for j in range(num_processing):
            if x[i, j].x > 0:
                print(f"Farm {i} to Processing {j}: {x[i, j].x} tons")
    for j in range(num_processing):
        for k in range(num_centers):
            if y[j, k].x > 0:
                print(f"Processing {j} to Center {k}: {y[j, k].x} tons")
else:
    print("No optimal solution found.")









# part d
# Create model
model = gp.Model("Transportation_Procurement_Plan")

# Decision variables
x = model.addVars(num_farms, num_processing, lb=0, vtype=GRB.CONTINUOUS, name="FarmToProc")
y = model.addVars(num_processing, num_centers, lb=0, vtype=GRB.CONTINUOUS, name="ProcToCenter")

# Objective function: Minimize total cost
model.setObjective(
    gp.quicksum(
        x[i, j] * (farms[f'Transport_Cost_To_Plant_{j+1}'][i] + farms['Cost_Per_Ton'][i] + processing['Processing_Cost_Per_Ton'][j])
        for i in range(num_farms) for j in range(num_processing)
    ) +
    gp.quicksum(
        y[j, k] * (processing[f'Transport_Cost_To_Center_{k+1}'][j])
        for j in range(num_processing) for k in range(num_centers)
    ),
    GRB.MINIMIZE
)

# Constraints
# Supply constraints at farms: Cannot exceed available material
for i in range(num_farms):
    model.addConstr(gp.quicksum(x[i, j] for j in range(num_processing)) <= farms['Bio_Material_Capacity_Tons'][i], name=f"FarmSupply_{i}")

# Capacity constraints at processing facilities
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) <= processing['Capacity_Tons'][j], name=f"ProcCapacity_{j}")

# Demand constraints at home centers
for k in range(num_centers):
    model.addConstr(gp.quicksum(y[j, k] for j in range(num_processing)) >= centers['Requested_Demand_Tons'][k], name=f"CenterDemand_{k}")

# Linking constraint: processed material must be transported to centers
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) >= gp.quicksum(y[j, k] for k in range(num_centers)), name=f"Balance_{j}")

# Quality constraint: Only use farms with quality 3 or 4
for i in range(num_farms):
    if farms['Quality'][i] < 3:
        for j in range(num_processing):
            model.addConstr(x[i, j] == 0, name=f"QualityConstraint_Farm{i}_Plant{j}")

# Optimize model
model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    print(f"Optimal Total Cost: {model.objVal}")
    for i in range(num_farms):
        for j in range(num_processing):
            if x[i, j].x > 0:
                print(f"Farm {i} to Processing {j}: {x[i, j].x}")
    for j in range(num_processing):
        for k in range(num_centers):
            if y[j, k].x > 0:
                print(f"Processing {j} to Center {k}: {y[j, k].x}")
else:
    print("No optimal solution found.")










# part e 1
# Create model
model = gp.Model("Transportation_Procurement_Plan")

# Decision variables
x = model.addVars(num_farms, num_processing, lb=0, vtype=GRB.CONTINUOUS, name="FarmToProc")
y = model.addVars(num_processing, num_centers, lb=0, vtype=GRB.CONTINUOUS, name="ProcToCenter")

# Objective function: Minimize total cost
model.setObjective(
    gp.quicksum(
        x[i, j] * (farms[f'Transport_Cost_To_Plant_{j+1}'][i] + farms['Cost_Per_Ton'][i])
        for i in range(num_farms) for j in range(num_processing)
    ) +
    gp.quicksum(
        y[j, k] * (processing[f'Transport_Cost_To_Center_{k+1}'][j] + processing['Processing_Cost_Per_Ton'][j])
        for j in range(num_processing) for k in range(num_centers)
    ),
    GRB.MINIMIZE
)

# Constraints
# Supply constraints at farms: Cannot exceed available material
for i in range(num_farms):
    model.addConstr(gp.quicksum(x[i, j] for j in range(num_processing)) <= farms['Bio_Material_Capacity_Tons'][i], name=f"FarmSupply_{i}")

# Capacity constraints at processing facilities
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) <= processing['Capacity_Tons'][j], name=f"ProcCapacity_{j}")

# Demand constraints at home centers
for k in range(num_centers):
    model.addConstr(gp.quicksum(y[j, k] for j in range(num_processing)) >= centers['Requested_Demand_Tons'][k], name=f"CenterDemand_{k}")

# Linking constraint: processed material must be transported to centers
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) >= gp.quicksum(y[j, k] for k in range(num_centers)), name=f"Balance_{j}")

# Step 4: Sourcing risk mitigation constraints (Part e)
# Calculate the total raw material sourced across all farms
total_raw_material = gp.quicksum(x[i, j] for i in range(num_farms) for j in range(num_processing))
for j in range(num_processing):
    model.addConstr(gp.quicksum(y[j,k] for k in range(num_centers)) <= 0.03 * total_raw_material, name=f"SourcingRisk_Plant{j}")

model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    print(f"Optimal Total Cost: {model.objVal}")
    for i in range(num_farms):
        for j in range(num_processing):
            if x[i, j].x > 0:
                print(f"Farm {i} to Processing {j}: {x[i, j].x} tons")
    for j in range(num_processing):
        for k in range(num_centers):
            if y[j, k].x > 0:
                print(f"Processing {j} to Center {k}: {y[j, k].x} tons")
else:
    print("No optimal solution found.")
    

# part e 2
# Create model
model = gp.Model("Transportation_Procurement_Plan")

# Decision variables
x = model.addVars(num_farms, num_processing, lb=0, vtype=GRB.CONTINUOUS, name="FarmToProc")
y = model.addVars(num_processing, num_centers, lb=0, vtype=GRB.CONTINUOUS, name="ProcToCenter")

# Objective function: Minimize total cost
model.setObjective(
    gp.quicksum(
        x[i, j] * (farms[f'Transport_Cost_To_Plant_{j+1}'][i] + farms['Cost_Per_Ton'][i] + processing['Processing_Cost_Per_Ton'][j])
        for i in range(num_farms) for j in range(num_processing)
    ) +
    gp.quicksum(
        y[j, k] * (processing[f'Transport_Cost_To_Center_{k+1}'][j])
        for j in range(num_processing) for k in range(num_centers)
    ),
    GRB.MINIMIZE
)

# Constraints
# Supply constraints at farms: Cannot exceed available material
for i in range(num_farms):
    model.addConstr(gp.quicksum(x[i, j] for j in range(num_processing)) <= farms['Bio_Material_Capacity_Tons'][i], name=f"FarmSupply_{i}")

# Capacity constraints at processing facilities
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) <= processing['Capacity_Tons'][j], name=f"ProcCapacity_{j}")

# Demand constraints at home centers
for k in range(num_centers):
    model.addConstr(gp.quicksum(y[j, k] for j in range(num_processing)) == centers['Requested_Demand_Tons'][k], name=f"CenterDemand_{k}")

# Linking constraint: processed material must be transported to centers
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) == gp.quicksum(y[j, k] for k in range(num_centers)), name=f"Balance_{j}")

# Supply risk mitigation: No processing facility can supply more than 50% of a single center's demand
for k in range(num_centers):
    center_demand = centers['Requested_Demand_Tons'][k]
    for j in range(num_processing):
        model.addConstr(y[j, k] <= 0.5*center_demand, name=f"SupplyRisk_Plant{j}_Center{k}")


# Optimize model
model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    print(f"Optimal Total Cost: {model.objVal}")
    for i in range(num_farms):
        for j in range(num_processing):
            if x[i, j].x > 0:
                print(f"Farm {i} to Processing {j}: {x[i, j].x}")
    for j in range(num_processing):
        for k in range(num_centers):
            if y[j, k].x > 0:
                print(f"Processing {j} to Center {k}: {y[j, k].x}")
else:
    print("No optimal solution found.")









# part f
# Create model
model = gp.Model("Transportation_Procurement_Plan")

# Decision variables
x = model.addVars(num_farms, num_processing, lb=0, vtype=GRB.CONTINUOUS, name="FarmToProc")
y = model.addVars(num_processing, num_centers, lb=0, vtype=GRB.CONTINUOUS, name="ProcToCenter")

# Objective function: Minimize total cost
model.setObjective(
    gp.quicksum(
        x[i, j] * (farms[f'Transport_Cost_To_Plant_{j+1}'][i] + farms['Cost_Per_Ton'][i] + processing['Processing_Cost_Per_Ton'][j])
        for i in range(num_farms) for j in range(num_processing)
    ) +
    gp.quicksum(
        y[j, k] * (processing[f'Transport_Cost_To_Center_{k+1}'][j])
        for j in range(num_processing) for k in range(num_centers)
    ),
    GRB.MINIMIZE
)

# Constraints
# Supply constraints at farms: Cannot exceed available material
for i in range(num_farms):
    model.addConstr(gp.quicksum(x[i, j] for j in range(num_processing)) <= farms['Bio_Material_Capacity_Tons'][i], name=f"FarmSupply_{i}")

# Capacity constraints at processing facilities
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) <= processing['Capacity_Tons'][j], name=f"ProcCapacity_{j}")

# Demand constraints at home centers
for k in range(num_centers):
    model.addConstr(gp.quicksum(y[j, k] for j in range(num_processing)) == centers['Requested_Demand_Tons'][k], name=f"CenterDemand_{k}")

# Linking constraint: processed material must be transported to centers
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) == gp.quicksum(y[j, k] for k in range(num_centers)), name=f"Balance_{j}")

# Region constraints: Processing plants can only send to centers in the same region
for j in range(num_processing):
    for k in range(num_centers):
        if processing['Region'][j] != centers['Region'][k]:
            model.addConstr(y[j, k] == 0, name=f"RegionConstraint_Plant{j}_Center{k}")

# Supply risk mitigation: No processing facility can supply more than 50% of a single center's demand
for k in range(num_centers):
    center_demand = centers['Requested_Demand_Tons'][k]
    for j in range(num_processing):
        model.addConstr(y[j, k] <= 0.5*center_demand, name=f"SupplyRisk_Plant{j}_Center{k}")

# Optimize the model
model.optimize()

if model.status == GRB.OPTIMAL:
    print(f"Optimal Cost: {model.objVal}")
    print("Farm to Plant Transportation:")
    for i in range(len(farms)):
        for j in range(len(processing)):
            if x[i, j].x > 0:
                print(f"Farm {i} to Plant {j}: {x[i, j].x} tons")
    print("\nPlant to Center Transportation:")
    for j in range(len(processing)):
        for k in range(len(centers)):
            if y[j, k].x > 0:
                print(f"Plant {j} to Center {k}: {y[j, k].x} tons")
else:
    print("No optimal solution found.")








# part h
# Create model
model = gp.Model("Transportation_Procurement_Plan")

# Decision variables
x = model.addVars(num_farms, num_processing, lb=0, vtype=GRB.CONTINUOUS, name="FarmToProc")
y = model.addVars(num_processing, num_centers, lb=0, vtype=GRB.CONTINUOUS, name="ProcToCenter")

# Objective function: Minimize total cost
model.setObjective(
    gp.quicksum(
        x[i, j] * (farms[f'Transport_Cost_To_Plant_{j+1}'][i] + farms['Cost_Per_Ton'][i] )
        for i in range(num_farms) for j in range(num_processing)
    ) +
    gp.quicksum(
        y[j, k] * (processing[f'Transport_Cost_To_Center_{k+1}'][j] + processing['Processing_Cost_Per_Ton'][j])
        for j in range(num_processing) for k in range(num_centers)
    ),
    GRB.MINIMIZE
)

# Constraints
# Supply constraints at farms: Cannot exceed available material
for i in range(num_farms):
    model.addConstr(gp.quicksum(x[i, j] for j in range(num_processing)) <= farms['Bio_Material_Capacity_Tons'][i], name=f"FarmSupply_{i}")

# Capacity constraints at processing facilities
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) <= processing['Capacity_Tons'][j], name=f"ProcCapacity_{j}")

# Demand constraints at home centers
for k in range(num_centers):
    model.addConstr(gp.quicksum(y[j, k] for j in range(num_processing)) >= centers['Requested_Demand_Tons'][k], name=f"CenterDemand_{k}")

# Linking constraint: processed material must be transported to centers
for j in range(num_processing):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_farms)) >= gp.quicksum(y[j, k] for k in range(num_centers)), name=f"Balance_{j}")

# Region constraints: Processing plants can only send to centers in the same region
for j in range(num_processing):
    for k in range(num_centers):
        if processing['Region'][j] != centers['Region'][k]:
            model.addConstr(y[j, k] == 0, name=f"RegionConstraint_Plant{j}_Center{k}")

# Supply risk mitigation: No processing facility can supply more than 50% of a single center's demand
for k in range(num_centers):
    center_demand = centers['Requested_Demand_Tons'][k]
    for j in range(num_processing):
        model.addConstr(y[j, k] <= 0.5*center_demand, name=f"SupplyRisk_Plant{j}_Center{k}")

# Step 4: Sourcing risk mitigation constraints (Part e)
# Calculate the total raw material sourced across all farms
total_raw_material = gp.quicksum(x[i, j] for i in range(num_farms) for j in range(num_processing))

for j in range(num_processing):
    model.addConstr(gp.quicksum(y[j,k] for k in range(num_centers)) <= 0.024 * total_raw_material, name=f"SourcingRisk_Plant{j}")

model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    print(f"Optimal Total Cost: {model.objVal}")
else:
    print("No optimal solution found.")


