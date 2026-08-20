numero = 8
if numero == 0:
    print("0")

hexadecimal = ""
while numero > 0:
    residuo = numero % 16
    if residuo < 10: 
        
    hexadecimal = str(residuo) + hexadecimal
    numero = numero // 16
print (hexadecimal)