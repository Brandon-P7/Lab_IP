while True:
        edad = int(input("Edad: "))
        
        if 0 <= edad <= 120: and type(edad) == int:
            break
        elif edad >= 0 and edad >= 120:
            print("La edad debe estar entre 0 y 120.") 
        if edad is not type(int):
            print("Escribe un numero entero.")

print(f"Edad registrada: {edad}")