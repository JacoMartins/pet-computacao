def sqlType(type):
  if type == int:
    return "INTEGER"
  elif type == str:
    return "TEXT"
  elif type == float:
    return "REAL"

def sqlDataType(value):
  return f'"{value}"' if type(value) == str else value

def typeString(type):
  if type == int:
    return "int"
  elif type == str:
    return "str"
  elif type == float:
    return "float"