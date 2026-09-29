while True:
    opcion = input("Elige A, B, o C:").strip().upper() #El strip toma todos los valores uno por uno,
    # el upper las convierte a mayuscula, por lo que  si se pone en minuscula se reconoce como una de las opciones.

    if opcion in ("A", "B", "C"):
        break

    print("opcion Invalida. Intenta de nuevo.")

print(f"Elegiste {opcion}  (señal de rankeo)")