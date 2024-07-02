
RANGO_NORMAL = range(1, 1006)
RANGO_EXTENDIDO = range(1006, 4095)

numero_vlan = int(input("Ingrese el número de VLAN: "))

if numero_vlan in RANGO_NORMAL:
    print(f"La VLAN {numero_vlan} pertenece al rango normal.")
elif numero_vlan in RANGO_EXTENDIDO:
    print(f"La VLAN {numero_vlan} pertenece al rango extendido.")
else:
    print("Número de VLAN fuera de rango válido.")
