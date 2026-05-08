import json
from lexer.utils import analizar_codigo

codigo = """{int w,x,y,z;
    { int x,y,z;
        {int w,x;
        }
    }
}"""

resultado = analizar_codigo(codigo)
print(json.dumps(resultado, indent=2))
