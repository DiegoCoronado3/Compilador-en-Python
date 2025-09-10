#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Código generado automáticamente desde Cascabel

nombre = ""
print("Por favor, ingrese su nombre:")
nombre = input()
anioNacimiento = 20
print("Por favor, ingrese su aÃ±o de nacimiento:")
anioNacimiento = int(input())
anioActual = 2000
anioActual = (anioActual + 25)
while anioNacimiento > anioActual:
    print("ERROR: El aÃ±o de nacimiento no puede ser mayor que "+str(anioActual)+"")
    anioNacimiento = int(input())
edad = (anioActual - anioNacimiento)
print("Estimado "+str(nombre)+", actualmente tu edad es "+str(edad)+"")
