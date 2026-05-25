"""
Django views para el analizador léxico
"""
import json
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

from .lexer import analyze_code, normalize_language
from .utils import analizar_codigo


logger = logging.getLogger(__name__)


DEFAULT_TREE_CODE = """
{int w,x,y,z;
    { int x,y,z;
        {int w,x;
        }
    }
    { int w,x;
        { int y,z;
        }
    }
}
""".strip()


@ensure_csrf_cookie
def index(request):
    return render(request, 'lexer/index.html')


@require_http_methods(["POST"])
def analyze_lexer(request):
    try:
        body_text = request.body.decode('utf-8') if request.body else '{}'
        logger.debug('analyze_lexer request.body=%s', body_text)
        logger.debug('analyze_lexer request.headers.X-CSRFToken=%s', request.headers.get('X-CSRFToken'))

        data = json.loads(body_text)
        codigo = data.get('codigo', '')
        lenguaje = normalize_language(data.get('lenguaje', 'python'))
        logger.debug('analyze_lexer codigo_length=%s', len(codigo))
        
        resultado = analyze_code(codigo, lenguaje=lenguaje)
        logger.debug('analyze_lexer tokens=%s errores=%s', len(resultado.get('tokens', [])), len(resultado.get('errores', [])))
        return JsonResponse(resultado)
    
    except json.JSONDecodeError:
        logger.exception('analyze_lexer received invalid JSON')
        return JsonResponse({
            "tokens": [],
            "errores": ["Error: JSON inválido en la petición"],
            "total_tokens": 0
        }, status=400)
    except Exception as e:
        logger.exception('analyze_lexer failed')
        return JsonResponse({
            "tokens": [],
            "errores": [f"Error en el servidor: {str(e)}"],
            "total_tokens": 0
        }, status=500)


@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def arbol_view(request):
    codigo = DEFAULT_TREE_CODE
    lenguaje = "python"

    if request.method == "POST":
        codigo = request.POST.get("codigo", DEFAULT_TREE_CODE)
        lenguaje = normalize_language(request.POST.get("lenguaje", "python"))
    elif request.GET.get("codigo"):
        codigo = request.GET.get("codigo", DEFAULT_TREE_CODE)
        lenguaje = normalize_language(request.GET.get("lenguaje", "python"))

    try:
        datos_arbol = analizar_codigo(codigo, lenguaje=lenguaje)
        json_data = json.dumps(datos_arbol)
        error = None
    except Exception as exc:
        json_data = json.dumps({"name": f"Error: {exc}"})
        error = str(exc)

    return render(request, 'lexer/arbol.html', {
        'codigo': codigo,
        'json_data': json_data,
        'error': error,
    })
