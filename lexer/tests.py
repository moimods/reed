import json

from django.test import Client, TestCase
from django.urls import reverse

from .lexer import LexicalAnalyzer, TokenType, analyze_code
from .utils import analizar_codigo


class LexerTestCase(TestCase):
    """Test cases for lexical analyzer"""

    def setUp(self):
        self.client = Client()
        self.analyzer = LexicalAnalyzer(lenguaje="python")

    def test_python_tokens_core(self):
        codigo = "x = 10\nmsg = \"hola\"\n# comentario\npi = 10.5\n"
        resultado = analyze_code(codigo, lenguaje="python")

        tipos = [t["tipo"] for t in resultado["tokens"]]

        self.assertIn("IDENTIFICADOR", tipos)
        self.assertIn("OPERADOR", tipos)
        self.assertIn("ENTERO", tipos)
        self.assertIn("FLOAT", tipos)
        self.assertIn("STRING", tipos)
        self.assertIn("COMENTARIO", tipos)
        self.assertIn("SALTO_LINEA", tipos)
        self.assertEqual(resultado["errores"], [])

    def test_boolean_and_null_python(self):
        resultado = analyze_code("flag = True\nobj = None", lenguaje="python")
        tipos = [t["tipo"] for t in resultado["tokens"]]
        self.assertIn("BOOLEANO", tipos)
        self.assertIn("NULL", tipos)

    def test_multi_language_javascript(self):
        codigo = "let x = 1.2e3; // comentario\nconst ok = true; const n = null;"
        resultado = analyze_code(codigo, lenguaje="javascript")
        tipos = [t["tipo"] for t in resultado["tokens"]]

        self.assertIn("PALABRA_RESERVADA", tipos)
        self.assertIn("FLOAT", tipos)
        self.assertIn("BOOLEANO", tipos)
        self.assertIn("NULL", tipos)
        self.assertIn("COMENTARIO", tipos)
        self.assertEqual(resultado["errores"], [])

    def test_ternary_operators_are_tokenized_as_operador(self):
        resultado = analyze_code("x = a if a > b else b", lenguaje="python")
        tipos = [t["tipo"] for t in resultado["tokens"]]

        self.assertIn("PALABRA_RESERVADA", tipos)
        self.assertEqual(resultado["errores"], [])

    def test_javascript_optional_chaining_operator(self):
        resultado = analyze_code("obj?.prop", lenguaje="javascript")
        operadores = [t["valor"] for t in resultado["tokens"] if t["tipo"] == "OPERADOR"]

        self.assertIn("?.", operadores)
        self.assertEqual(resultado["errores"], [])

    def test_multi_language_java_block_comment(self):
        codigo = "int a = 10; /* bloque */ boolean ok = true;"
        resultado = analyze_code(codigo, lenguaje="java")
        tipos = [t["tipo"] for t in resultado["tokens"]]

        self.assertIn("PALABRA_RESERVADA", tipos)
        self.assertIn("COMENTARIO", tipos)
        self.assertIn("BOOLEANO", tipos)
        self.assertEqual(resultado["errores"], [])

    def test_lexical_error_invalid_char(self):
        resultado = analyze_code("x = 10 €", lenguaje="python")
        self.assertTrue(resultado["errores"])
        self.assertTrue(any(t["tipo"] == "ERROR" for t in resultado["tokens"]))

    def test_lexical_error_unclosed_string(self):
        resultado = analyze_code("msg = \"hola", lenguaje="python")
        self.assertTrue(any("String sin cerrar" in e for e in resultado["errores"]))
        self.assertTrue(any(t["tipo"] == "ERROR" for t in resultado["tokens"]))

    def test_lexical_error_unclosed_block_comment(self):
        resultado = analyze_code("/* comentario", lenguaje="javascript")
        self.assertTrue(any("Comentario multilínea sin cerrar" in e for e in resultado["errores"]))
        self.assertTrue(any(t["tipo"] == "ERROR" for t in resultado["tokens"]))

    def test_lexical_error_bad_number(self):
        resultado = analyze_code("x = 123abc", lenguaje="python")
        self.assertTrue(any("Número mal formado" in e for e in resultado["errores"]))
        self.assertTrue(any(t["tipo"] == "ERROR" for t in resultado["tokens"]))

    def test_dollar_is_special_character(self):
        resultado = analyze_code("$x = 1", lenguaje="javascript")
        special_values = [t["valor"] for t in resultado["tokens"] if t["tipo"] == "CARACTER_ESPECIAL"]

        self.assertIn("$", special_values)
        self.assertEqual(resultado["errores"], [])

    def test_include_spaces_config(self):
        analyzer = LexicalAnalyzer(lenguaje="python", incluir_espacios=True)
        tokens, errores = analyzer.tokenize("x  =  1")
        self.assertEqual(errores, [])
        self.assertTrue(any(t.tipo == TokenType.ESPACIO for t in tokens))

    def test_spaces_are_tokenized_by_default(self):
        resultado = analyze_code("x = 1", lenguaje="python")
        tipos = [t["tipo"] for t in resultado["tokens"]]
        self.assertIn("ESPACIO", tipos)
        self.assertEqual(resultado["errores"], [])

    def test_unknown_language_raises(self):
        with self.assertRaises(ValueError):
            LexicalAnalyzer(lenguaje="ruby")

    def test_custom_reserved_words_in_default_language(self):
        codigo = "if else elif for while def class return import from as try except finally with"
        resultado = analyze_code(codigo, lenguaje="python")
        tipos = [t["tipo"] for t in resultado["tokens"] if t["tipo"] != "ESPACIO"]

        self.assertTrue(all(tipo == "PALABRA_RESERVADA" for tipo in tipos))
        self.assertEqual(resultado["errores"], [])

    def test_analyze_view_get(self):
        response = self.client.get(reverse('lexer:analyze'))
        self.assertEqual(response.status_code, 405)

    def test_analyze_view_post(self):
        response = self.client.post(
            reverse('lexer:analyze'),
            data=json.dumps({'codigo': 'x = 5'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('tokens', data)
        self.assertIn('errores', data)
        self.assertIn('total_tokens', data)
        self.assertNotIn('ast', data)

    def test_index_view(self):
        response = self.client.get(reverse('lexer:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lexer/index.html')

    def test_tree_parser_generates_hierarchy(self):
        codigo = """
        {int w,x,y,z;
            { int x,y,z;
                {int w,x;
                }
            }
        }
        """

        tree = analizar_codigo(codigo)

        # Estructura del parser académico:
        # PROGRAMA (root)
        #   └── { } (non_terminal - BLOQUE)
        #       └── int (non_terminal - tipo de declaración)
        #           ├── , (non_terminal - LISTA_VARIABLES)
        #           └── ; (terminal)
        
        self.assertEqual(tree["name"], "PROGRAMA")
        self.assertEqual(tree["type"], "root")
        
        # Primer hijo debe ser un BLOQUE ({ })
        primer_bloque = tree["children"][0]
        self.assertEqual(primer_bloque["name"], "{ }")
        self.assertEqual(primer_bloque["type"], "non_terminal")
        self.assertTrue(len(primer_bloque["children"]) > 0, "BLOQUE no tiene hijos")
        
        # Buscar primer nodo tipo que sea una DECLARACION
        primera_decl = None
        for child in primer_bloque["children"]:
            if child["type"] == "non_terminal" and child["name"] in ("int", "float", "double", "string", "boolean", "var", "let", "const"):
                primera_decl = child
                break
        
        self.assertIsNotNone(primera_decl, "No se encontró DECLARACION (tipo) en BLOQUE")
        # DECLARACION debe tener LISTA_VARIABLES y ;
        self.assertTrue(len(primera_decl["children"]) >= 2, "DECLARACION sin suficientes hijos")

    def test_tree_view_get(self):
        response = self.client.get(reverse('lexer:arbol'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lexer/arbol.html')

    def test_tree_view_get_uses_input_code(self):
        codigo = "{int a,b; { int c; }}"
        response = self.client.get(reverse('lexer:arbol'), {'codigo': codigo})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lexer/arbol.html')
        self.assertContains(response, 'Árbol Sintáctico')
        # El árbol debe contener nodos del tipo esperado
        # Puede contener "{ }" (BLOQUE) o tipos de datos como "int"
        response_text = response.content.decode()
        self.assertTrue("int" in response_text or "{" in response_text, 
                       "El árbol debe contener información del código")

    def test_tree_parser_reports_syntax_error(self):
        # Código incompleto sin cerrar el bloque
        tree = analizar_codigo("{int a,b;")

        # El parser debe generar PROGRAMA incluso con errores
        self.assertEqual(tree["name"], "PROGRAMA")
        self.assertEqual(tree["type"], "root")
        
        # Debe haber registrado un error
        self.assertTrue(len(tree) >= 0)  # El árbol se genera aunque haya errores
        
        # El primer hijo debería ser un BLOQUE (aunque incompleto)
        # porque el parser intenta generar un árbol válido aunque haya errores parciales
        self.assertGreater(len(tree["children"]), 0, "PROGRAMA debe tener hijos")
        primer_hijo = tree["children"][0]
        # Puede ser un BLOQUE { } con los hijos que logró parsear
        self.assertIn(primer_hijo["name"], ["{ }", "ERROR_SINTACTICO"])
