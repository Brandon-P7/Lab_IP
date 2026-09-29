edad = 18
tiene_credencial = True
tiene_adeudo = False

if edad >= 18:
    es_mayor = True
else:
    es_mayor = False

if tiene_credencial == True:
    documento_valido = True
else:
    es_mayor = False

if tiene_adeudo == False:
    sin_adeudo = not tiene_adeudo
else:
    sin_adeudo = False

if es_mayor and documento_valido and sin_adeudo:
    autorizado = True
else:
    autorizado = False
print(autorizado)

#en condicionales, el if siempre debe ir primero, el elif siempre va antes del Else y else al final de todo
# elif se ejecuta si se cumple o no el "if" es un "entonces" realmente va a creatividad para usarla junto a la eficacia
#Siempre optimizar el codigo, se llama perdida en costo computacional porque el sistema se hace  