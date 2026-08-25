numero, binario = 8, ""         #aqui tenemos dos constantes donde guardamos los numeros a convertir o mostrar.
if numero == 0: print("0")      #Si el numero es cero, entonces, imprimir "0"
while numero > 0: binario, numero = str(numero % 2) + binario, numero // 2 # Mientras numero sea mayor a 0, el binario sera igual al al numero modulo 2 convertido en cadena + el binario y al numero lo divide en manera entera entre 2.
print(binario)  #Imprimir el numero binario el cual feu guardado de manera iterada en la primera linea.

