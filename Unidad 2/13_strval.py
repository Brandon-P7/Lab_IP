while True:
    nombre = input("Nombre: ").strip() #strip elimina espacios al inicio y final
    #print(nombre)
    nombre = " ".join(nombre.split())

    if nombre and nombre.replace(" ", "").isalpha():
      #isalpha, valida las letras despues de quitar espacios internos.
       # print(nombre)  #en el parentesis del "replace" como pusims espacio lo remplaza por el segundo despues de la coma, es decir, nada
        break
    print("Usa letras y no dejes el nombre vacio")

nombre_normalizado = nombre.title()# title funciona para poner en mayuscula la primera letra de cada palabra
print(f"Hola, {nombre_normalizado}")