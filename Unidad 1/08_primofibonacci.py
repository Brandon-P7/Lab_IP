numero = int(input("Ingresa un numero: "))
es_primo = True
a = 0
b = 1
siguiente = {}

if numero <= 1:
    es_primo = False
else:
    i = 2
while i < numero:
    if numero % i == 0:
        es_primo = False
        break
    i = i + 1
if es_primo == True:
    print("Es primo")
    while a < numero:
            siguiente = a + b
            a = b
            b = siguiente
    if a == numero:
        print("si esta en fibonacci")
    else:
        print("no esta en fibonacci")
        
else:
    print("no es primo")
