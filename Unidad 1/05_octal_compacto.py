numero, octal = 8, ""  #aqui tenemos dos constantes donde guardamos los numeros a convertir o mostrar.
if numero == 0: print("0")   #Si el numero es cero, entonces, imprimir "0"
while numero > 0: octal, numero = str(numero % 8) + octal, numero // 8 ## Mientras numero sea mayor a 0, el octal sera igual al al numero modulo 8 convertido en cadena + el binario y al numero lo divide en manera entera entre 8
print (octal) #Imprimir el numero octal el cual feu guardado de manera iterada en la primera linea.