import pandas as pd

def readSpecificHeat(material_name:str):
  df = pd.read_csv('materialSummary.csv')
  specific_heat = df.loc[df['Material'] == f'{material_name}', 'Specific Heat'].values[0] #J/kg·K
  #grabs the value of specific heat column where the row is the material_name variable
  specific_heat_value = float(''.join(filter(str.isdigit, specific_heat.split()[0])))
  #turns it into a float
  return specific_heat_value
#returns a heat value

def getTemp(specific_heat_value, mass:float, energy:float)->float:
  
  # Q = cmT, T = Q/cm
  temp_change = energy/(specific_heat_value*mass)
  
  return temp_change
#temp change is energy divided by (specific heat times mass)


# print(getTemp("Steel", 1,  5000000 ))