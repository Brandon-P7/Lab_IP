total = input("Total De Cuenta:")
total = int
propina = input("Ingresa el porcentaje de propina:")
propina = int
personas = input("Cantidad de personas:")
personas = int

propina = total*propina/100
individual = (total + propina)/personas 

print(f"{total:.2}")
print(f"{individual:.2}")