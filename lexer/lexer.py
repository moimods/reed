
from dataclasses import dataclass
from enum import Enum
import re
from typing import Dict, List, Optional, Tuple


LANG_CONFIG = {
    "python": {
        "keywords": {
            "if", "else", "elif", "for", "while", "def", "class", "return",
            "import", "from", "as", "try", "except", "finally", "with",
            "pass", "break", "continue", "and", "or", "not", "in", "is",
            "lambda", "yield", "async", "await", "global", "nonlocal",
            "assert", "del", "raise", "then",
            # Tipos de datos comunes (para parser académico)
            "int", "float", "double", "string", "boolean", "char", "void",
            "var", "let", "const"
        },
        "booleans": {"True", "False"},
        "nulls": {"None"},
        "line_comment": "#",
        "block_comment": None,
        "operators": {
            "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=",
            "+=", "-=", "*=", "/=", "&", "|", "^", "~", "<<", ">>",
            "//", "**", "//=", "**=", "&=", "|=", "^=", ">>=", "<<=", "->", ":"
        },
        "special_chars": {"(", ")", "{", "}", "[", "]", ";", ",", ".", ":", "\"", "'", "$"}
    },
    "java": {
        "keywords": {
            "abstract", "assert", "boolean", "break", "byte", "case", "catch", "char",
            "class", "const", "continue", "default", "do", "double", "else", "enum",
            "extends", "final", "finally", "float", "for", "goto", "if", "implements",
            "import", "instanceof", "int", "interface", "long", "native", "new", "package",
            "private", "protected", "public", "return", "short", "static", "strictfp",
            "super", "switch", "synchronized", "this", "throw", "throws", "transient",
            "try", "void", "volatile", "while", "then"
        },
        "booleans": {"true", "false"},
        "nulls": {"null"},
        "line_comment": "//",
        "block_comment": ("/*", "*/"),
        "operators": {
            "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=",
            "+=", "-=", "*=", "/=", "%=", "++", "--", "&&", "||", "!", "~",
            "&", "|", "^", "<<", ">>", ">>>", "&=", "|=", "^=", "<<=", ">>=", ">>>=",
            "?", ":", "->", "::"
        },
        "special_chars": {"(", ")", "{", "}", "[", "]", ";", ",", ".", "\"", "'", "$"}
    },
    "javascript": {
        "keywords": {
            "break", "case", "catch", "class", "const", "continue", "debugger", "default",
            "delete", "do", "else", "export", "extends", "finally", "for", "function",
            "if", "import", "in", "instanceof", "let", "new", "return", "super", "switch",
            "this", "throw", "try", "typeof", "var", "void", "while", "with", "yield",
            "await", "async", "then"
        },
        "booleans": {"true", "false"},
        "nulls": {"null", "undefined"},
        "line_comment": "//",
        "block_comment": ("/*", "*/"),
        "operators": {
            "+", "-", "*", "/", "%", "=", "==", "===", "!=", "!==", "<", ">", "<=", ">=",
            "+=", "-=", "*=", "/=", "%=", "++", "--", "&&", "||", "!", "~", "??",
            "&", "|", "^", "<<", ">>", ">>>", "&=", "|=", "^=", "<<=", ">>=", ">>>=",
            "=>", "?", ":", ".", "...", "?."
        },
        "special_chars": {"(", ")", "{", "}", "[", "]", ";", ",", "\"", "'", "`", "$"}
    },
    "c": {
        "keywords": {
            "auto", "break", "case", "char", "const", "continue", "default", "do",
            "double", "else", "enum", "extern", "float", "for", "goto", "if",
            "int", "long", "register", "return", "short", "signed", "sizeof", "static",
            "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while",
            "then"
        },
        "booleans": set(),
        "nulls": {"NULL"},
        "line_comment": "//",
        "block_comment": ("/*", "*/"),
        "operators": {
            "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=",
            "+=", "-=", "*=", "/=", "%=", "++", "--", "&&", "||", "!", "~",
            "&", "|", "^", "<<", ">>", "&=", "|=", "^=", "<<=", ">>=", "->", "?", ":"
        },
        "special_chars": {"(", ")", "{", "}", "[", "]", ";", ",", ".", "\"", "'", "$"}
    },
    "cpp": {
        "keywords": {
            "alignas", "alignof", "asm", "auto", "bool", "break", "case", "catch", "char",
            "class", "const", "constexpr", "continue", "decltype", "default", "delete", "do",
            "double", "else", "enum", "explicit", "export", "extern", "false", "float", "for",
            "friend", "goto", "if", "inline", "int", "long", "mutable", "namespace", "new",
            "noexcept", "nullptr", "operator", "private", "protected", "public", "register", "return",
            "short", "signed", "sizeof", "static", "struct", "switch", "template", "this", "throw",
            "true", "try", "typedef", "typeid", "typename", "union", "unsigned", "using", "virtual",
            "void", "volatile", "while", "then"
        },
        "booleans": {"true", "false"},
        "nulls": {"nullptr", "NULL"},
        "line_comment": "//",
        "block_comment": ("/*", "*/"),
        "operators": {
            "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=",
            "+=", "-=", "*=", "/=", "%=", "++", "--", "&&", "||", "!", "~",
            "&", "|", "^", "<<", ">>", "&=", "|=", "^=", "<<=", ">>=", "->", "::", "?", ":",
            "<=>"
        },
        "special_chars": {"(", ")", "{", "}", "[", "]", ";", ",", ".", "\"", "'", "$"}
    },
}


LANGUAGE_ALIASES = {
    "python": "python",
    "phyton": "python",
    "py": "python",
    "java": "java",
    "javascript": "javascript",
    "js": "javascript",
    "c": "c",
    "cpp": "cpp",
    "c++": "cpp",
}


def normalize_language(lenguaje: Optional[str]) -> str:
    if not lenguaje:
        return "python"

    normalized = LANGUAGE_ALIASES.get(lenguaje.strip().lower())
    if not normalized:
        raise ValueError(f"Lenguaje no soportado: {lenguaje}")
    return normalized


class TokenType(Enum):
    PALABRA_RESERVADA = "PALABRA_RESERVADA"
    IDENTIFICADOR = "IDENTIFICADOR"
    ENTERO = "ENTERO"
    FLOAT = "FLOAT"
    STRING = "STRING"
    OPERADOR = "OPERADOR"
    CARACTER_ESPECIAL = "CARACTER_ESPECIAL"
    COMENTARIO = "COMENTARIO"
    SALTO_LINEA = "SALTO_LINEA"
    ESPACIO = "ESPACIO"
    BOOLEANO = "BOOLEANO"
    NULL = "NULL"
    ERROR = "ERROR"


@dataclass
class Token:
    tipo: TokenType
    valor: str
    linea: int
    columna: int

    def to_dict(self) -> Dict:
        return {
            "tipo": self.tipo.value,
            "valor": self.valor,
            "linea": self.linea,
            "columna": self.columna,
        }


class LexicalAnalyzer:
    """Analizador léxico configurable por lenguaje."""

    def __init__(self, lenguaje: str = "python", incluir_espacios: bool = False):
        lenguaje_normalizado = normalize_language(lenguaje)
        if lenguaje_normalizado not in LANG_CONFIG:
            raise ValueError(f"Lenguaje no soportado: {lenguaje}")
        self.lenguaje = lenguaje_normalizado
        self.incluir_espacios = incluir_espacios
        self.config = LANG_CONFIG[lenguaje_normalizado]

        # Operadores ordenados por longitud descendente para priorizar multi-caracter.
        self._ops_sorted = sorted(self.config["operators"], key=len, reverse=True)

        # Patrones base
        self._identifier_re = re.compile(r"[A-Za-z_]\w*")
        self._float_re = re.compile(r"(?:\d+\.\d+|\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?|\d+[eE][+-]?\d+")
        self._int_re = re.compile(r"\d+")
        self._bad_number_re = re.compile(r"\d+[A-Za-z_]\w*")

    def _append_error(self, tokens: List[Token], errores: List[str], mensaje: str, valor: str, linea: int, columna: int) -> None:
        errores.append(mensaje)
        tokens.append(Token(TokenType.ERROR, valor, linea, columna))

    def _consume_line_comment(self, codigo: str, indice: int, linea: int, columna: int, marker: str) -> Tuple[str, int, int, int]:
        start = indice
        while indice < len(codigo) and codigo[indice] != "\n":
            indice += 1
            columna += 1
        return codigo[start:indice], indice, linea, columna

    def _consume_block_comment(
        self,
        codigo: str,
        indice: int,
        linea: int,
        columna: int,
        start_marker: str,
        end_marker: str,
    ) -> Tuple[str, int, int, int, Optional[str]]:
        start_line, start_col = linea, columna
        start = indice
        indice += len(start_marker)
        columna += len(start_marker)

        while indice < len(codigo):
            if codigo.startswith(end_marker, indice):
                indice += len(end_marker)
                columna += len(end_marker)
                return codigo[start:indice], indice, linea, columna, None

            if codigo[indice] == "\n":
                indice += 1
                linea += 1
                columna = 1
            else:
                indice += 1
                columna += 1

        return (
            codigo[start:indice],
            indice,
            linea,
            columna,
            f"Comentario multilínea sin cerrar en línea {start_line}, columna {start_col}",
        )

    def _consume_string(self, codigo: str, indice: int, linea: int, columna: int) -> Tuple[str, int, int, int, Optional[str]]:
        quote = codigo[indice]
        start_line, start_col = linea, columna
        start = indice
        triple = False

        if codigo[indice:indice + 3] == quote * 3:
            triple = True
            indice += 3
            columna += 3
        else:
            indice += 1
            columna += 1

        escaped = False
        while indice < len(codigo):
            ch = codigo[indice]

            if escaped:
                escaped = False
                if ch == "\n":
                    linea += 1
                    columna = 1
                else:
                    columna += 1
                indice += 1
                continue

            if ch == "\\":
                escaped = True
                indice += 1
                columna += 1
                continue

            if triple:
                if codigo[indice:indice + 3] == quote * 3:
                    indice += 3
                    columna += 3
                    return codigo[start:indice], indice, linea, columna, None
            else:
                if ch == quote:
                    indice += 1
                    columna += 1
                    return codigo[start:indice], indice, linea, columna, None

            if ch == "\n":
                if not triple:
                    return (
                        codigo[start:indice],
                        indice,
                        linea,
                        columna,
                        f"String sin cerrar en línea {start_line}, columna {start_col}",
                    )
                linea += 1
                columna = 1
                indice += 1
                continue

            indice += 1
            columna += 1

        return (
            codigo[start:indice],
            indice,
            linea,
            columna,
            f"String sin cerrar en línea {start_line}, columna {start_col}",
        )

    def tokenize(self, codigo: str, lenguaje: Optional[str] = None) -> Tuple[List[Token], List[str]]:
        # Manejo de lenguaje dinámico sin reinicializar
        config = self.config
        ops_sorted = self._ops_sorted
        
        if lenguaje and normalize_language(lenguaje) != self.lenguaje:
            lenguaje_normalizado = normalize_language(lenguaje)
            if lenguaje_normalizado not in LANG_CONFIG:
                raise ValueError(f"Lenguaje no soportado: {lenguaje}")
            config = LANG_CONFIG[lenguaje_normalizado]
            ops_sorted = sorted(config["operators"], key=len, reverse=True)

        tokens: List[Token] = []
        errores: List[str] = []

        # Parámetros internos obligatorios
        linea = 1
        columna = 1
        indice = 0

        line_comment = config["line_comment"]
        block_comment = config["block_comment"]

        while indice < len(codigo):
            ch = codigo[indice]

            # 1) SALTO_LINEA
            if ch == "\n":
                tokens.append(Token(TokenType.SALTO_LINEA, "\\n", linea, columna))
                indice += 1
                linea += 1
                columna = 1
                continue

            # 2) ESPACIOS/TABS
            if ch in (" ", "\t"):
                start = indice
                col_ini = columna
                while indice < len(codigo) and codigo[indice] in (" ", "\t"):
                    indice += 1
                    columna += 1
                if self.incluir_espacios:
                    tokens.append(Token(TokenType.ESPACIO, codigo[start:indice], linea, col_ini))
                continue

            # 3) COMENTARIOS
            if line_comment and codigo.startswith(line_comment, indice):
                col_ini = columna
                valor, indice, linea, columna = self._consume_line_comment(codigo, indice, linea, columna, line_comment)
                tokens.append(Token(TokenType.COMENTARIO, valor, linea, col_ini))
                continue

            if block_comment and codigo.startswith(block_comment[0], indice):
                col_ini = columna
                valor, indice, linea, columna, err = self._consume_block_comment(
                    codigo,
                    indice,
                    linea,
                    columna,
                    block_comment[0],
                    block_comment[1],
                )
                if err:
                    self._append_error(tokens, errores, err, valor, linea, col_ini)
                else:
                    tokens.append(Token(TokenType.COMENTARIO, valor, linea, col_ini))
                continue

            # 4) STRINGS
            if ch in ('"', "'", "`"):
                col_ini = columna
                valor, indice, linea, columna, err = self._consume_string(codigo, indice, linea, columna)
                if err:
                    self._append_error(tokens, errores, err, valor, linea, col_ini)
                else:
                    tokens.append(Token(TokenType.STRING, valor, linea, col_ini))
                continue

            # 5) PALABRAS RESERVADAS / VARIABLES / BOOLEANO / NULL
            ident_match = self._identifier_re.match(codigo, indice)
            if ident_match:
                valor = ident_match.group(0)
                col_ini = columna

                if valor in config["booleans"]:
                    tipo = TokenType.BOOLEANO
                elif valor in config["nulls"]:
                    tipo = TokenType.NULL
                elif valor in config["keywords"]:
                    tipo = TokenType.PALABRA_RESERVADA
                else:
                    tipo = TokenType.IDENTIFICADOR

                tokens.append(Token(tipo, valor, linea, col_ini))
                avance = len(valor)
                indice += avance
                columna += avance
                continue

            # 6) NÚMEROS (ENTERO/FLOAT)
            bad_num = self._bad_number_re.match(codigo, indice)
            if bad_num:
                valor = bad_num.group(0)
                self._append_error(
                    tokens,
                    errores,
                    f"Número mal formado '{valor}' en línea {linea}, columna {columna}",
                    valor,
                    linea,
                    columna,
                )
                indice += len(valor)
                columna += len(valor)
                continue

            float_match = self._float_re.match(codigo, indice)
            if float_match:
                valor = float_match.group(0)
                tokens.append(Token(TokenType.FLOAT, valor, linea, columna))
                indice += len(valor)
                columna += len(valor)
                continue

            int_match = self._int_re.match(codigo, indice)
            if int_match:
                valor = int_match.group(0)
                tokens.append(Token(TokenType.ENTERO, valor, linea, columna))
                indice += len(valor)
                columna += len(valor)
                continue

            # 7) OPERADORES (multi-caracter primero)
            operador_encontrado = None
            for op in ops_sorted:
                if codigo.startswith(op, indice):
                    operador_encontrado = op
                    break

            if operador_encontrado:
                tokens.append(Token(TokenType.OPERADOR, operador_encontrado, linea, columna))
                indice += len(operador_encontrado)
                columna += len(operador_encontrado)
                continue

            # 8) CARACTERES ESPECIALES
            if ch in config["special_chars"]:
                tokens.append(Token(TokenType.CARACTER_ESPECIAL, ch, linea, columna))
                indice += 1
                columna += 1
                continue

            # 9) ERROR
            self._append_error(
                tokens,
                errores,
                f"Carácter no válido '{ch}' en línea {linea}, columna {columna}",
                ch,
                linea,
                columna,
            )
            indice += 1
            columna += 1

        return tokens, errores


def analyze_code(codigo: str, lenguaje: str = "python", incluir_espacios: bool = True) -> Dict:
    analyzer = LexicalAnalyzer(lenguaje=normalize_language(lenguaje), incluir_espacios=incluir_espacios)
    tokens, errores = analyzer.tokenize(codigo)

    return {
        "tokens": [token.to_dict() for token in tokens],
        "errores": errores,
        "total_tokens": len(tokens),
    }

