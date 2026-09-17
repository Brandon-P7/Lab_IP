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