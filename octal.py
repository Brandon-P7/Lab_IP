numero = 8
if numero == 0:
    print("0")

binario = ""
while numero > 0:
    residuo = numero % 8
    binario = str(residuo) + binario
    numero = numero // 8
print (binario)