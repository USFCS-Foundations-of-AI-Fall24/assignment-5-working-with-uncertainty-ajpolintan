from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination

car_model = BayesianNetwork(
    [
        ("Battery", "Radio"),
        ("Battery", "Ignition"),
        ("Ignition","Starts"),
        ("Gas","Starts"),
        ("Starts","Moves"),
        ("KeyPresent", "Starts")
    ]
)

# Defining the parameters using CPT
from pgmpy.factors.discrete import TabularCPD

cpd_battery = TabularCPD(
    variable="Battery", variable_card=2, values=[[0.70], [0.30]],
    state_names={"Battery":['Works',"Doesn't work"]},
)

cpd_gas = TabularCPD(
    variable="Gas", variable_card=2, values=[[0.40], [0.60]],
    state_names={"Gas":['Full',"Empty"]},
)

cpd_radio = TabularCPD(
    variable=  "Radio", variable_card=2,
    values=[[0.75, 0.01],[0.25, 0.99]],
    evidence=["Battery"],
    evidence_card=[2],
    state_names={"Radio": ["turns on", "Doesn't turn on"],
                 "Battery": ['Works',"Doesn't work"]}
)

cpd_ignition = TabularCPD(
    variable=  "Ignition", variable_card=2,
    values=[[0.75, 0.01],[0.25, 0.99]],
    evidence=["Battery"],
    evidence_card=[2],
    state_names={"Ignition": ["Works", "Doesn't work"],
                 "Battery": ['Works',"Doesn't work"]}
)

cpd_starts = TabularCPD(
    variable="Starts",
    variable_card=2,
    values=[[0.99, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99]],
    evidence=["Ignition", "Gas", "KeyPresent"],
    evidence_card=[2, 2, 2],
    state_names={"Starts":['yes','no'], "Ignition":["Works", "Doesn't work"], "Gas":['Full',"Empty"], "KeyPresent":['Present','Not Present'],},
)

#print(cpd_starts)

cpd_moves = TabularCPD(
    variable="Moves", variable_card=2,
    values=[[0.8, 0.01],[0.2, 0.99]],
    evidence=["Starts"],
    evidence_card=[2],
    state_names={"Moves": ["yes", "no"],
                 "Starts": ['yes', 'no'] }
)

cpd_key = TabularCPD(
    variable= "KeyPresent", variable_card=2, values=[[0.7],[0.3]],
    state_names ={"KeyPresent":["Present", "Not Present"]}
)


# Associating the parameters with the model structure
car_model.add_cpds(cpd_starts, cpd_ignition, cpd_gas, cpd_radio, cpd_battery, cpd_moves, cpd_key)

car_infer = VariableElimination(car_model)

#print(car_infer.query(variables=["Moves"],evidence={"Radio":"turns on", "Starts":"yes"}))

if __name__ == "__main__":
    #print(car_infer.query(variables=["Moves"],evidence={"Radio":"turns on", "Starts":"yes"}))

    #second part
    #not move, what is the probability that the batter is not working given the car will not move
    q = car_infer.query(variables=["Radio"], evidence={"Moves":"no"})
    print(q)
    #what is the probability the car will not stoiop given the radio is not working
    q = car_infer.query(variables=["Starts"], evidence={"Radio":"Doesn't turn on"})
    print(q)

    #what is the probability of the radio working change if we discover that the car has gas in it given the battery is working
    q = car_infer.query(variables=["Radio", "Gas"], evidence={"Battery":"Works"})
    print(q)

    #what is the probability of the ignition failing change if we observe that the car doesn't have gas in it given the car doesn't move
    q = car_infer.query(variables=["Ignition","Gas"], evidence={"Moves" : "no"})
    print(q)

    #What is the probability that the car starts if the radio works has gas in it?
    q = car_infer.query(variables=["Starts"], evidence={"Radio" : "turns on", "Gas" : "Full"})
    print(q)

    #query. Key is not present given that the car does not move
    q = car_infer.query(variables=["KeyPresent"], evidence={"Moves": "no"})
    print(q)
