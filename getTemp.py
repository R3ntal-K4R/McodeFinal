import pandas as pd

def readSpecificHeat(material_name:str):
  df = pd.read_csv('materialSummary.csv')
  specific_heat = df.loc[df['Material'] == f'{material_name}', 'Specific Heat'].values[0] #J/kg·K
  specific_heat_value = float(''.join(filter(str.isdigit, specific_heat.split()[0])))
  return specific_heat_value

def getTemp(specific_heat_value, mass:float, energy:float)->float:
  
  # Q = cmT, T = Q/cm
  temp_change = energy/(specific_heat_value*mass)
  
  return temp_change


# print(getTemp("Steel", 1,  5000000 ))