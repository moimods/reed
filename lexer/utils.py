"""
Parser Recursivo Descendente Académico
Genera árboles de derivación sintácticos formales.
Consume tokens del lexer y produce nodos tipo: root, non_terminal, terminal.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SyntaxNode:
    """Nodo sintáctico académico con tipos: root, non_terminal, terminal"""
    name: str
    type: str  # "root", "non_terminal", "terminal"
    children: List['SyntaxNode'] = field(default_factory=list)

    def to_dict(self):
        """Convierte el nodo a diccionario para JSON"""
        return {
            "name": self.name,
            "type": self.type,
            "children": [child.to_dict() for child in self.children]
        }


class SyntaxParser:
    """
    Parser recursivo descendente que consume tokens del lexer.
    Genera árboles de derivación sintácticos formales.
    
    Gramática CFG soportada:
    
    PROGRAMA -> BLOQUE
    BLOQUE -> '{' SECUENCIA '}'
    SECUENCIA -> DECLARACION SECUENCIA | ε
    DECLARACION -> TIPO LISTA_VARIABLES ';'
    LISTA_VARIABLES -> IDENTIFICADOR (',' LISTA_VARIABLES)?
    TIPO -> (int | float | double | string | boolean | var | let | const)
    """

    def __init__(self, tokens):
        """
        Inicializa el parser con una lista de tokens.
        
        Args:
            tokens: Lista de Token objects del lexer
        """
        # Filtra saltos de línea y espacios (no relevantes para sintaxis)
        self.tokens = [t for t in tokens if t.tipo.value not in ("SALTO_LINEA", "ESPACIO", "COMENTARIO")]
        self.current_index = 0
        self.errors = []

    def current(self):
        """Retorna el token actual"""
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        return None

    def advance(self):
        """Avanza al siguiente token"""
        if self.current_index < len(self.tokens):
            self.current_index += 1

    def check(self, valor):
        """Verifica si el token actual tiene el valor especificado"""
        token = self.current()
        return token is not None and token.valor == valor

    def check_type(self, tipo_str):
        """Verifica si el token actual es del tipo especificado"""
        token = self.current()
        return token is not None and token.tipo.value == tipo_str

    def consume(self, valor):
        """Consume un token con valor esperado o lanza error"""
        if not self.check(valor):
            token = self.current()
            esperado = valor
            encontrado = f"'{token.valor}'" if token else "EOF"
            self.errors.append(f"Error: Se esperaba '{esperado}', se encontró {encontrado}")
            return False
        self.advance()
        return True

    def parse(self):
        """
        Punto de entrada del parser.
        Retorna: SyntaxNode con raíz PROGRAMA
        """
        try:
            # Un programa es una secuencia de bloques/declaraciones
            children = []
            
            while self.current() is not None:
                if self.check("{"):
                    children.append(self.parse_block())
                elif self.is_type_keyword():
                    children.append(self.parse_declaration())
                else:
                    self.advance()

            return SyntaxNode(
                "PROGRAMA",
                "root",
                children if children else [SyntaxNode("ε", "terminal")]
            )

        except Exception as e:
            self.errors.append(str(e))
            return SyntaxNode(
                "ERROR_SINTACTICO",
                "root",
                [SyntaxNode(str(e), "terminal")]
            )

    def parse_block(self):
        """
        Parsea un bloque: { SECUENCIA }
        Gramática: BLOQUE -> '{' SECUENCIA '}'
        """
        if not self.consume("{"):
            return SyntaxNode("{ }", "non_terminal", [])

        children = []

        # SECUENCIA
        while not self.check("}") and self.current() is not None:
            if self.is_type_keyword():
                children.append(self.parse_declaration())
            elif self.check("{"):
                children.append(self.parse_block())
            else:
                self.advance()

        if not self.consume("}"):
            return SyntaxNode("{ }", "non_terminal", children)

        return SyntaxNode(
            "{ }",
            "non_terminal",
            children if children else [SyntaxNode("ε", "terminal")]
        )

    def parse_declaration(self):
        """
        Parsea una declaración: TIPO LISTA_VARIABLES ;
        Gramática: DECLARACION -> TIPO LISTA_VARIABLES ';'
        """
        if not self.is_type_keyword():
            self.errors.append("Se esperaba un tipo de dato")
            return SyntaxNode("ERROR", "non_terminal")

        tipo_token = self.current()
        tipo = tipo_token.valor
        self.advance()

        # LISTA_VARIABLES
        lista_vars = self.parse_variable_list()

        if not self.consume(";"):
            self.errors.append("Se esperaba ';' después de lista de variables")
            return SyntaxNode(
                tipo,
                "non_terminal",
                [lista_vars, SyntaxNode(";", "terminal")]
            )

        return SyntaxNode(
            tipo,
            "non_terminal",
            [lista_vars, SyntaxNode(";", "terminal")]
        )

    def parse_variable_list(self):
        """
        Parsea lista de variables: id (',' id)*
        Gramática: LISTA_VARIABLES -> IDENTIFICADOR (',' LISTA_VARIABLES)?
        """
        variables = []

        while self.current() is not None:
            if self.check_type("IDENTIFICADOR"):
                id_token = self.current()
                variables.append(SyntaxNode(id_token.valor, "terminal"))
                self.advance()

                # Verifica coma para siguiente variable
                if self.check(","):
                    self.advance()
                else:
                    break
            else:
                break

        # Retorna nodo con lista de variables
        return SyntaxNode(
            ",",
            "non_terminal",
            variables if variables else [SyntaxNode("ε", "terminal")]
        )

    def is_type_keyword(self):
        """Verifica si el token actual es una palabra clave de tipo"""
        type_keywords = {
            "int", "float", "double", "string", "boolean",
            "char", "long", "short", "byte",
            "var", "let", "const",
            "void"
        }
        token = self.current()
        return (
            token is not None and
            token.tipo.value == "PALABRA_RESERVADA" and 
            token.valor in type_keywords
        )


def analizar_codigo(codigo):
    """
    Analiza código usando el parser recursivo descendente.
    Retorna árbol sintáctico JSON.
    
    Args:
        codigo: String con código a analizar
        
    Returns:
        dict: Árbol sintáctico en formato JSON con estructura para D3
    """
    from .lexer import LexicalAnalyzer

    try:
        # Análisis léxico
        lexer = LexicalAnalyzer()
        tokens, errores_lexicos = lexer.tokenize(codigo)

        # Análisis sintáctico
        parser = SyntaxParser(tokens)
        arbol = parser.parse()

        # Recopila todos los errores
        todos_errores = errores_lexicos + parser.errors

        # Retorna estructura compatible con D3
        return arbol.to_dict()

    except Exception as e:
        return {
            "name": "ERROR_SINTACTICO",
            "type": "root",
            "children": [{"name": str(e), "type": "terminal", "children": []}]
        }
