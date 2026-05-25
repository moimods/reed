"""Parser sintáctico académico para generar árbol compatible con D3."""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SyntaxNode:
    """Nodo sintáctico académico con tipos: root, non_terminal, terminal."""
    name: str
    type: str  # "root", "non_terminal", "terminal"
    children: List['SyntaxNode'] = field(default_factory=list)

    def to_dict(self):
        """Convierte el nodo a diccionario para JSON."""
        return {
            "name": self.name,
            "type": self.type,
            "children": [child.to_dict() for child in self.children]
        }


class SyntaxParser:
    """Parser recursivo simple para visualización de árbol académico."""

    def __init__(self, tokens):
        # Filtra tokens no sintácticos para construir el árbol semántico.
        self.tokens = [t for t in tokens if t.tipo.value not in ("SALTO_LINEA", "ESPACIO", "COMENTARIO")]
        self.current_index = 0
        self.errors = []
        self.type_keywords = {
            "int", "float", "double", "string", "boolean", "char", "void",
            "long", "short", "byte", "var", "let", "const", "auto"
        }

    def current(self):
        """Retorna el token actual."""
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        return None

    def advance(self):
        """Avanza al siguiente token."""
        if self.current_index < len(self.tokens):
            self.current_index += 1

    def check(self, valor):
        """Verifica si el token actual tiene el valor especificado."""
        token = self.current()
        return token is not None and token.valor == valor

    def check_type(self, tipo_str):
        """Verifica si el token actual es del tipo especificado."""
        token = self.current()
        return token is not None and token.tipo.value == tipo_str

    def consume(self, valor, mandatory=True):
        """Consume un token por valor y registra error si es obligatorio."""
        if not self.check(valor):
            if mandatory:
                token = self.current()
                encontrado = f"'{token.valor}'" if token else "EOF"
                self.errors.append(f"Error: Se esperaba '{valor}', se encontró {encontrado}")
            return False
        self.advance()
        return True

    def _tail(self, node: SyntaxNode) -> SyntaxNode:
        """Retorna el último nodo de la rama principal para encadenar sentencias."""
        current = node
        while current.children:
            current = current.children[-1]
        return current

    def _link_sequence(self, statements: List[SyntaxNode]) -> Optional[SyntaxNode]:
        """Encadena sentencias usando el nodo final de cada sentencia."""
        if not statements:
            return None

        for i in range(len(statements) - 1):
            self._tail(statements[i]).children.append(statements[i + 1])
        return statements[0]

    def _is_assignment_start(self):
        return self.check_type("IDENTIFICADOR")

    def _is_type_keyword(self):
        token = self.current()
        return (
            token is not None
            and token.tipo.value == "PALABRA_RESERVADA"
            and token.valor in self.type_keywords
        )

    def _parse_atom(self):
        token = self.current()
        if token is None:
            return SyntaxNode("ε", "terminal")

        if token.tipo.value in {"IDENTIFICADOR", "ENTERO", "FLOAT", "STRING", "BOOLEANO", "NULL"}:
            self.advance()
            return SyntaxNode(token.valor, "terminal")

        if self.check("("):
            self.advance()
            expr = self._parse_expression()
            self.consume(")", mandatory=False)
            return expr

        self.advance()
        return SyntaxNode(token.valor, "terminal")

    def _parse_expression(self):
        left = self._parse_atom()

        while self.current() is not None and self.current().tipo.value == "OPERADOR" and self.current().valor in {"+", "-", "*", "/", "%"}:
            op = self.current().valor
            self.advance()
            right = self._parse_atom()
            left = SyntaxNode(op, "non_terminal", [left, right])

        return left

    def _parse_condition(self):
        left = self._parse_expression()

        if self.current() is not None and self.current().tipo.value == "OPERADOR" and self.current().valor in {"=", "==", "!=", "<", ">", "<=", ">="}:
            op = self.current().valor
            self.advance()
            right = self._parse_expression()
            return SyntaxNode(op, "non_terminal", [left, right])

        return left

    def _parse_variable_list_node(self):
        comma_node = SyntaxNode(",", "non_terminal", [])

        if self.check_type("IDENTIFICADOR"):
            comma_node.children.append(SyntaxNode(self.current().valor, "terminal"))
            self.advance()
        else:
            self.errors.append("Se esperaba un identificador en la declaración")
            comma_node.children.append(SyntaxNode("ε", "terminal"))
            return comma_node

        while self.check(","):
            self.advance()
            if self.check_type("IDENTIFICADOR"):
                comma_node.children.append(SyntaxNode(self.current().valor, "terminal"))
                self.advance()
            else:
                self.errors.append("Se esperaba identificador después de ','")
                comma_node.children.append(SyntaxNode("ε", "terminal"))
                break

        return comma_node

    def parse_declaration(self):
        type_token = self.current()
        self.advance()

        type_node = SyntaxNode(type_token.valor, "non_terminal", [])
        comma_node = self._parse_variable_list_node()
        semicolon_node = SyntaxNode(";", "terminal", [])

        type_node.children.append(comma_node)
        type_node.children.append(semicolon_node)

        if not self.consume(";", mandatory=False):
            self.errors.append("Se esperaba ';' en declaración")

        return type_node

    def parse_assignment(self):
        target = SyntaxNode(self.current().valor, "terminal")
        self.advance()

        if self.current() is not None and self.current().tipo.value == "OPERADOR" and self.current().valor in {"=", "+=", "-=", "*=", "/="}:
            op_value = self.current().valor
            self.advance()
        else:
            self.errors.append("Se esperaba operador de asignación")
            op_value = "="

        expr = self._parse_expression()
        assign_node = SyntaxNode(op_value, "non_terminal", [target, expr])

        semicolon_node = SyntaxNode(";", "terminal", [])
        assign_node.children.append(semicolon_node)

        if not self.consume(";", mandatory=False):
            self.errors.append("Se esperaba ';' en asignación")

        return assign_node

    def parse_block(self):
        block_node = SyntaxNode("{ }", "non_terminal", [])
        self.consume("{", mandatory=False)

        statements = []
        while self.current() is not None and not self.check("}"):
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
            else:
                self.advance()

        first = self._link_sequence(statements)
        if first is None:
            block_node.children.append(SyntaxNode("ε", "terminal"))
        else:
            block_node.children.append(first)

        if not self.consume("}", mandatory=False):
            self.errors.append("Se esperaba '}' para cerrar bloque")

        return block_node

    def parse_if(self):
        if_node = SyntaxNode("if", "non_terminal", [])
        self.consume("if", mandatory=False)

        condition_node = self._parse_condition()
        if_node.children.append(condition_node)

        if self.check("then"):
            self.advance()
            then_node = SyntaxNode("then", "non_terminal", [])
        else:
            self.errors.append("Se esperaba 'then' después de la condición del if")
            then_node = SyntaxNode("then", "non_terminal", [])

        then_statement = self.parse_statement()
        then_node.children.append(then_statement if then_statement else SyntaxNode("ε", "terminal"))
        if_node.children.append(then_node)

        else_node = None
        if self.check("else"):
            self.advance()
            else_node = SyntaxNode("else", "non_terminal", [])
            else_statement = self.parse_statement()
            else_node.children.append(else_statement if else_statement else SyntaxNode("ε", "terminal"))
            if_node.children.append(else_node)

        return if_node

    def parse_statement(self):
        if self.current() is None:
            return None

        if self._is_type_keyword():
            return self.parse_declaration()

        if self.check("if"):
            return self.parse_if()

        if self.check("{"):
            return self.parse_block()

        if self._is_assignment_start():
            return self.parse_assignment()

        return None

    def parse(self):
        """Punto de entrada del parser."""
        try:
            statements = []
            while self.current() is not None:
                statement = self.parse_statement()
                if statement:
                    statements.append(statement)
                else:
                    self.advance()

            first = self._link_sequence(statements)
            return SyntaxNode(
                "PROGRAMA",
                "root",
                [first] if first else [SyntaxNode("ε", "terminal")]
            )
        except Exception as e:
            self.errors.append(str(e))
            return SyntaxNode(
                "ERROR_SINTACTICO",
                "root",
                [SyntaxNode(str(e), "terminal")]
            )


def analizar_codigo(codigo, lenguaje="python"):
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
        lexer = LexicalAnalyzer(lenguaje=lenguaje)
        tokens, errores_lexicos = lexer.tokenize(codigo)

        parser = SyntaxParser(tokens)
        arbol = parser.parse()

        # Conserva recopilación de errores por compatibilidad futura.
        _ = errores_lexicos + parser.errors

        return arbol.to_dict()

    except Exception as e:
        return {
            "name": "ERROR_SINTACTICO",
            "type": "root",
            "children": [{"name": str(e), "type": "terminal", "children": []}]
        }
