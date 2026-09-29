for numero in [4, 7, 9, 12]:
    if numero == 9: #al llegar a 9 ya no imprime y se detiene, contando el 4, 7 y lo
        break 
    print("con break", numero)

for numero in [4, 7, 9, 12]:
    if numero == 9: 
        continue #salta el numero 9 ya que al llegar ahi hace una pausa para despues "continuar" con lo que sigue
    print(f"con CONTINUE { numero}")
