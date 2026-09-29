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
main()