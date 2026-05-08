# Documentación de Tipos de Tokens

Este documento describe todos los tipos de tokens que el analizador léxico puede identificar y su función en el análisis de código.

---

## 1. PALABRA_RESERVADA

**Tipo:** `TokenType.PALABRA_RESERVADA`

**Función:** Identificar palabras clave del lenguaje que tienen un significado específico y no pueden usarse como nombres de variables o identificadores.

**Ejemplos por lenguaje:**

### Python
- `if`, `else`, `elif` — Control condicional
- `for`, `while` — Bucles
- `def`, `class` — Definición de funciones y clases
- `return` — Retorno de función
- `import`, `from`, `as` — Importaciones de módulos
- `try`, `except`, `finally` — Manejo de excepciones
- `with` — Gestor de contexto
- `and`, `or`, `not` — Operadores lógicos

### JavaScript
- `let`, `const`, `var` — Declaración de variables
- `function` — Definición de función
- `if`, `else` — Control condicional
- `for`, `while`, `do` — Bucles
- `switch`, `case` — Control de casos
- `return` — Retorno de función
- `new` — Crear nueva instancia
- `async`, `await` — Operaciones asincrónicas

### Java
- `public`, `private`, `protected` — Modificadores de acceso
- `class`, `interface`, `enum` — Definición de tipos
- `if`, `else` — Control condicional
- `for`, `while` — Bucles
- `synchronized` — Sincronización en hilos
- `static`, `final` — Modificadores de clase

---

## 2. IDENTIFICADOR

**Tipo:** `TokenType.IDENTIFICADOR`

**Función:** Representar nombres de variables, funciones, clases, métodos y otros símbolos definidos por el programador.

**Características:**
- Comienza con una letra (`A-Z`, `a-z`) o guion bajo (`_`)
- Puede contener letras, dígitos (`0-9`) y guiones bajos
- No pueden ser palabras reservadas

**Ejemplos:**
- `x`, `nombre`, `_privado` — Variables
- `suma`, `calcularPromedio`, `procesar_datos` — Nombres de funciones
- `Persona`, `Usuario`, `MiClase` — Nombres de clases

---

## 3. ENTERO

**Tipo:** `TokenType.ENTERO`

**Función:** Representar números enteros en el código fuente.

**Características:**
- Secuencia de dígitos (`0-9`)
- Sin punto decimal
- Puede estar precedido de un signo negativo (aunque este se considera un operador separado)

**Ejemplos:**
- `10`, `42`, `0`, `1000`

**Nota:** Los signos `+` y `-` se tokenizean como operadores separados.

---

## 4. FLOAT

**Tipo:** `TokenType.FLOAT`

**Función:** Representar números con punto decimal o notación científica.

**Características:**
- Contiene un punto decimal (`.`)
- Puede incluir dígitos antes y después del punto
- Soporta notación científica con `e` o `E`

**Ejemplos:**
- `3.14`, `0.5`, `10.0`
- `1.5e-3` (notación científica = 0.0015)
- `2.5E+2` (notación científica = 250)
- `.5` (equivalente a 0.5)
- `5.` (equivalente a 5.0)

---

## 5. STRING

**Tipo:** `TokenType.STRING`

**Función:** Representar cadenas de caracteres (textos) definidas en el código.

**Características:**
- Delimitadas por comillas simples (`'...'`), comillas dobles (`"..."`) o backticks (`` `...` ``)
- Pueden contener caracteres de escape (`\n`, `\t`, `\\`, etc.)
- Soportan saltos de línea en casos especiales (multiline strings)

**Ejemplos:**

### Comillas simples y dobles
```
'Hola mundo'
"Texto con espacios"
```

### Backticks (Template strings en JavaScript)
```
`Hola ${nombre}`
`Resultado: ${x + y}`
```

### Multiline strings (Python)
```
'''Este es un
string multilínea'''

"""Docstring
en Python"""
```

---

## 6. OPERADOR

**Tipo:** `TokenType.OPERADOR`

**Función:** Representar operadores aritméticos, lógicos, de comparación y de asignación.

**Categorías de operadores:**

### Operadores Aritméticos
- `+` — Suma
- `-` — Resta
- `*` — Multiplicación
- `/` — División
- `//` — División entera (Python)
- `%` — Módulo (resto)
- `**` — Exponenciación (Python)

### Operadores de Comparación
- `==` — Igual
- `!=` — No igual
- `<` — Menor que
- `>` — Mayor que
- `<=` — Menor o igual
- `>=` — Mayor o igual
- `===` — Igualdad estricta (JavaScript)
- `!==` — Desigualdad estricta (JavaScript)

### Operadores Lógicos
- `&&` — AND lógico (Java, JavaScript)
- `||` — OR lógico (Java, JavaScript)
- `!` — NOT lógico (Java, JavaScript)
- `&` — AND bitwise
- `|` — OR bitwise
- `^` — XOR bitwise
- `~` — NOT bitwise
- `<<`, `>>`, `>>>` — Desplazamiento de bits

### Operadores de Asignación
- `=` — Asignación simple
- `+=`, `-=`, `*=`, `/=` — Asignación compuesta
- `&=`, `|=`, `^=` — Asignación bitwise
- `<<=`, `>>=`, `>>>=` — Asignación con desplazamiento

### Operadores Especiales
- `->` — Tipo de retorno (Java, Python)
- `=>` — Función flecha (JavaScript)
- `::` — Referencia de método (Java)
- `?` — Operador ternario (Java, JavaScript)
- `:` — Separador (Python, Java, JavaScript)
- `??` — Coalescing nulo (JavaScript)
- `?.` — Acceso seguro (JavaScript)
- `...` — Spread/Rest operator (JavaScript)

---

## 7. CARACTER_ESPECIAL

**Tipo:** `TokenType.CARACTER_ESPECIAL`

**Función:** Representar caracteres de puntuación y delimitadores estructurales.

**Función por carácter:**

| Carácter | Función |
|----------|---------|
| `(` | Abre paréntesis (llamadas de función, expresiones) |
| `)` | Cierra paréntesis |
| `{` | Abre bloque (funciones, condicionales, bucles) |
| `}` | Cierra bloque |
| `[` | Abre array/lista |
| `]` | Cierra array/lista |
| `;` | Terminador de sentencia (Java, JavaScript) |
| `,` | Separador de elementos |
| `.` | Acceso a miembros (propiedades, métodos) |
| `"` | Delimitador de string |
| `'` | Delimitador de string |
| `` ` `` | Delimitador de template string (JavaScript) |
| `$` | Interpolación en strings (JavaScript) |

---

## 8. COMENTARIO

**Tipo:** `TokenType.COMENTARIO`

**Función:** Representar comentarios en el código fuente. Son ignorados durante la ejecución pero documentan el código.

**Tipos de comentarios:**

### Comentarios de línea
```
# Comentario en Python
// Comentario en Java o JavaScript
```

### Comentarios de bloque (multilínea)
```
/* Comentario
   en múltiples
   líneas */
```

**Características:**
- Los comentarios se tokenizean pero suelen ser ignorados por el parser
- Sirven para documentar el código
- Mejoran la legibilidad

---

## 9. BOOLEANO

**Tipo:** `TokenType.BOOLEANO`

**Función:** Representar valores lógicos verdadero o falso.

**Valores según lenguaje:**

### Python
- `True` — Verdadero
- `False` — Falso

### Java / JavaScript
- `true` — Verdadero
- `false` — Falso

**Uso:**
- Condiciones en sentencias `if`, `while`
- Retorno de funciones booleanas
- Asignación a variables

---

## 10. NULL

**Tipo:** `TokenType.NULL`

**Función:** Representar la ausencia de valor o referencia nula.

**Valores según lenguaje:**

### Python
- `None` — Valor nulo

### Java / JavaScript
- `null` — Referencia nula

### JavaScript (adicional)
- `undefined` — Variable no definida

**Uso:**
- Inicialización de variables sin valor
- Retorno de funciones sin valor de retorno
- Comparaciones nulas

---

## 11. SALTO_LINEA

**Tipo:** `TokenType.SALTO_LINEA`

**Función:** Representar cambios de línea en el código fuente.

**Características:**
- Representado como `\n` en los tokens
- Importante para mantener rastreo de línea y columna
- Afecta a la estructura del análisis sintáctico

**Valor en token:**
```json
{
  "tipo": "SALTO_LINEA",
  "valor": "\\n",
  "linea": 3,
  "columna": 10
}
```

---

## 12. ESPACIO

**Tipo:** `TokenType.ESPACIO`

**Función:** Representar espacios en blanco y tabulaciones (si se incluyen en el análisis).

**Características:**
- Normalmente ignorados por el analizador léxico
- Se incluyen solo si `incluir_espacios=True` en el constructor
- Incluye espacios simples y tabulaciones

**Nota:** Por defecto, estos tokens no se incluyen en el análisis.

---

## 13. ERROR

**Tipo:** `TokenType.ERROR`

**Función:** Marcar caracteres o secuencias que no son válidas en el lenguaje.

**Causas comunes:**
- Caracteres inválidos que no pertenecen a ningún lenguaje
- Strings sin cerrar correctamente
- Números mal formados (ej: `123abc`)
- Comentarios de bloque sin cierre

**Ejemplo:**
```json
{
  "tipo": "ERROR",
  "valor": "@",
  "linea": 5,
  "columna": 12,
  "mensaje": "Carácter no válido '@' en línea 5, columna 12"
}
```

---

## Resumen de Jerarquía de Tokens

```
TOKENS
├── Léxicos
│   ├── PALABRA_RESERVADA (keywords del lenguaje)
│   ├── IDENTIFICADOR (nombres definidos por usuario)
│   ├── BOOLEANO (true/false)
│   └── NULL (null/None/undefined)
├── Literales
│   ├── ENTERO (números sin punto)
│   ├── FLOAT (números con punto decimal)
│   └── STRING (cadenas de caracteres)
├── Operadores y Símbolos
│   ├── OPERADOR (aritméticos, lógicos, etc.)
│   └── CARACTER_ESPECIAL (delimitadores)
├── Estructura
│   ├── SALTO_LINEA (cambios de línea)
│   └── ESPACIO (espacios en blanco)
├── Documentación
│   └── COMENTARIO (comentarios del código)
└── Excepciones
    └── ERROR (caracteres/secuencias inválidas)
```

---

## Ejemplo Completo de Tokenización

### Código fuente (Python)
```python
def suma(a, b):
    # Función que suma dos números
    return a + b
```

### Tokens generados

| Tipo | Valor | Línea | Columna |
|------|-------|-------|---------|
| PALABRA_RESERVADA | `def` | 1 | 1 |
| IDENTIFICADOR | `suma` | 1 | 5 |
| CARACTER_ESPECIAL | `(` | 1 | 9 |
| IDENTIFICADOR | `a` | 1 | 10 |
| CARACTER_ESPECIAL | `,` | 1 | 11 |
| IDENTIFICADOR | `b` | 1 | 13 |
| CARACTER_ESPECIAL | `)` | 1 | 14 |
| OPERADOR | `:` | 1 | 15 |
| SALTO_LINEA | `\n` | 1 | 16 |
| COMENTARIO | `# Función que suma dos números` | 2 | 1 |
| SALTO_LINEA | `\n` | 2 | 31 |
| PALABRA_RESERVADA | `return` | 3 | 1 |
| IDENTIFICADOR | `a` | 3 | 8 |
| OPERADOR | `+` | 3 | 10 |
| IDENTIFICADOR | `b` | 3 | 12 |
| SALTO_LINEA | `\n` | 3 | 13 |

---

## Configuración por Lenguaje

El analizador léxico se configura automáticamente según el lenguaje seleccionado:

- **Python:** Palabras reservadas Python, comentarios `#`, operadores Python
- **Java:** Palabras reservadas Java, comentarios `//` y `/* */`, operadores Java
- **JavaScript:** Palabras reservadas JavaScript, comentarios `//` y `/* */`, template strings con backticks

Para cambiar el lenguaje:
```python
analyzer = LexicalAnalyzer(lenguaje="javascript")
tokens, errores = analyzer.tokenize(codigo)
```
