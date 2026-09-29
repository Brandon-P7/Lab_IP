def consultar_saldo():
    print("tu saldo es 00000, povre")
def depositar():
    print("Deposito realizado")
def retirar():
    print("Retiro realizado")
def salir():
    print("Saliendo del cajero automatico")

def mostrar_menu():
    print("1. Consultar saldo")
    print("2. Despositar")
    print("3. Saldo: $0.00")
    print("4. Salir")
    return input("opcion: ").strip()

def login():
    MAX = 3

    for intento in range(1, MAX + 1):
        usuario = input("Usuario: ").strip().lower()
        clave = input("Contraseña: ")

        if usuario == "alumno" and clave == "python123":
             main()
             break

        print("Credenciales incorrectas")
    else:
        print("Acceso bloqueado")
        
def main():

    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            consultar_saldo()
        elif opcion == "2":
            depositar()
        elif opcion == "3":
            retirar()
        elif opcion == "4":
            salir()
            break
        else:
            print("Opcion invalida")
login()