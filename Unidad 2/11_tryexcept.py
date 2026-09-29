while True:
    try: #cuando no hay errores procesa de manera normal lo de dentro.
        edad = int(input("Edad: "))
        
        if 0 <= edad <= 120:
        
            break
#al crear una funcion, preguntar si es un verbo, y si lo es se puede sacar una funcion de el.
        print("La edad debe estar entre 0 y 120.")
    except ValueError: #en este caso el value error verifica que lo ingresado sea de tipo "int" si es contrario al rango de if
                        #y no es del 
        print("Escribe un numero entero.")

print(f"Edad registrada: {edad}")


