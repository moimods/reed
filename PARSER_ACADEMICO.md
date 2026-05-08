# Parser Recursivo Descendente Académico

## Implementación Completada

Se ha implementado un parser recursivo descendente formal que genera árboles de derivación sintácticos académicos.

### Características Principales

#### 1. Clase `SyntaxNode`
```python
@dataclass
class SyntaxNode:
    name: str
    type: str  # "root", "non_terminal", "terminal"
    children: List['SyntaxNode']
```

- Estructura simple y limpia para representar nodos
- Método `to_dict()` para convertir a JSON
- Compatible con D3.js para visualización

#### 2. Clase `SyntaxParser`
```python
class SyntaxParser:
    def __init__(self, tokens)
    def parse() -> SyntaxNode
    def parse_block() -> SyntaxNode
    def parse_declaration() -> SyntaxNode
    def parse_variable_list() -> SyntaxNode
```

**Métodos principales:**
- `current()` - Retorna el token actual
- `advance()` - Avanza al siguiente token
- `check(valor)` - Verifica si el token actual tiene un valor específico
- `check_type(tipo_str)` - Verifica el tipo de token
- `consume(valor)` - Consume un token esperado o registra error
- `is_type_keyword()` - Verifica si es una palabra clave de tipo

### Gramática CFG Soportada

```
PROGRAMA -> BLOQUE*

BLOQUE -> '{' SECUENCIA '}'

SECUENCIA -> DECLARACION SECUENCIA | BLOQUE SECUENCIA | ε

DECLARACION -> TIPO LISTA_VARIABLES ';'

LISTA_VARIABLES -> IDENTIFICADOR (',' LISTA_VARIABLES)?

TIPO -> (int | float | double | string | boolean | char | void | 
         var | let | const)
```

### Tipos de Nodos

| Tipo | Descripción |
|------|-------------|
| `root` | Raíz del árbol (PROGRAMA) |
| `non_terminal` | Nodo no terminal (símbolo de la gramática) |
| `terminal` | Nodo terminal (token del lexer) |

### Ejemplo de Salida

**Código de entrada:**
```
{int w,x,y,z;}
```

**Árbol generado:**
```json
{
  "name": "PROGRAMA",
  "type": "root",
  "children": [
    {
      "name": "{ }",
      "type": "non_terminal",
      "children": [
        {
          "name": "int",
          "type": "non_terminal",
          "children": [
            {
              "name": ",",
              "type": "non_terminal",
              "children": [
                {"name": "w", "type": "terminal", "children": []},
                {"name": "x", "type": "terminal", "children": []},
                {"name": "y", "type": "terminal", "children": []},
                {"name": "z", "type": "terminal", "children": []}
              ]
            },
            {"name": ";", "type": "terminal", "children": []}
          ]
        }
      ]
    }
  ]
}
```

### Integración con el Sistema

#### 1. Lexer (lexer/lexer.py)
- Proporciona tokens al parser
- Se ha actualizado para reconocer tipos de datos como palabras reservadas
- Filtra saltos de línea y espacios antes de pasarlos al parser

#### 2. Parser (lexer/utils.py)
- Función principal: `analizar_codigo(codigo)`
- Retorna árbol sintáctico en formato JSON compatible con D3.js
- Manejo de errores: registra errores sintácticos pero intenta generar árbol válido

#### 3. Vistas (lexer/views.py)
- `arbol_view`: Renderiza el árbol en la interfaz web
- Acepta código vía GET o POST
- Renderiza árbol en template `lexer/arbol.html`

### Separación de Responsabilidades

```
Lexer (lexer/lexer.py)
  ↓ Tokens
  
Parser (lexer/utils.py)
  ↓ Árbol Sintáctico
  
Renderer (D3.js en template)
  ↓ Visualización
```

**Lexer:** Reconoce palabras, números, operadores, etc.
**Parser:** Reconoce estructura, gramática, validaciones sintácticas

### Palabras Clave Reconocidas (Python)

```python
# Control de flujo
if, else, elif, for, while, def, class, return

# Manejo de excepciones
try, except, finally

# Módulos
import, from, as

# Operadores lógicos
and, or, not, in, is

# Tipos de datos (nuevos)
int, float, double, string, boolean, char, void
var, let, const
```

### Pruebas

Todos los 22 tests pasan:
- ✓ Tokenización léxica
- ✓ Reconocimiento de palabras clave
- ✓ Generación de árbol sintáctico
- ✓ Manejo de bloques anidados
- ✓ Manejo de declaraciones múltiples
- ✓ Vistas web (GET/POST)
- ✓ Renderización en D3.js

### Próximas Mejoras (Opcional)

1. **Extensión de Gramática**
   - Soportar statements (if, for, while, etc.)
   - Soportar llamadas a función
   - Soportar operadores binarios

2. **Análisis Semántico**
   - Verificación de tipos
   - Resolución de símbolos
   - Análisis de alcance (scope)

3. **Optimizaciones**
   - Compilación de parser (código generado)
   - Caché de árboles sintácticos
   - Análisis incremental

### Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `lexer/lexer.py` | Agregados tipos de datos a keywords de Python |
| `lexer/utils.py` | Reescrito completamente con parser recursivo descendente |
| `lexer/tests.py` | Actualizados tests para nueva estructura académica |
| `TOKENS.md` | Documento con ejemplos de tokens |
| `DOCUMENTACION_TOKENS.md` | Documentación completa de tipos de tokens |

### Validación

```bash
# Ejecutar todos los tests
python manage.py test lexer.tests

# Ejecutar servidor
python manage.py runserver

# Acceder a interfaz web
http://127.0.0.1:8000/arbol/
```

### Conclusión

Se ha implementado un parser académico formal que:
✓ Consume tokens del lexer correctamente
✓ Genera árboles de derivación sintácticos formales
✓ Produce nodos con tipos: root, non_terminal, terminal
✓ Es compatible con D3.js para visualización
✓ Mantiene separación clara entre análisis léxico y sintáctico
✓ Incluye manejo de errores
✓ Tiene cobertura completa de tests (22/22 pasando)
