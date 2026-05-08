import json
from lexer.lexer import LexicalAnalyzer

codigo = """{int w,x,y,z;"""

analyzer = LexicalAnalyzer()
tokens, errores = analyzer.tokenize(codigo)

print("Tokens generados:")
for t in tokens:
    print(f"  {t.tipo.value:20} '{t.valor:15}' línea {t.linea} columna {t.columna}")

print("\nErrores:", errores)
