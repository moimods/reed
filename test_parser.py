#!/usr/bin/env python
"""Test script para el nuevo parser"""
from lexer.utils import analizar_codigo
import json

codigo = """let opcion = 1;
let a = 10, b = 5;

switch (opcion) {
    case 1:
        console.log(a + b);
        break;
    case 2:
        console.log(a - b);
        break;
    default:
        console.log('Opción no válida');
}"""

print("Analizando código JavaScript...")
resultado = analizar_codigo(codigo)
print(json.dumps(resultado, indent=2))
