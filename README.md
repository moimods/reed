# Proyecto Automatas

Aplicación Django para analizar código y visualizar su estructura léxica y sintáctica.

## Estructura del proyecto

```text
automatas/
├── manage.py
├── requirements.txt
├── automatasproject/
├── lexer/
├── templates/
└── static/
```

## Requisitos

- Python instalado en el sistema.
- Bash o una terminal compatible.

## Configuración inicial

1. Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Aplicar migraciones:

```bash
python manage.py migrate
```

## Correr el proyecto

Para iniciar el servidor local:

```bash
python manage.py runserver
```

Luego abre en el navegador:

```text
http://127.0.0.1:8000/
```

## Ejecutar pruebas

Para validar el proyecto con la suite de tests:

```bash
python manage.py test lexer.tests -v 1
```

## Acceso al panel de administración

Si necesitas entrar al admin de Django, crea un superusuario:

```bash
python manage.py createsuperuser
```

## Archivos estáticos

Si vas a preparar un despliegue o necesitas compilar los estáticos:

```bash
python manage.py collectstatic --noinput
```

## Notas

-- Si Bash no permite activar el entorno, asegúrate de ejecutar el comando desde una sesión compatible con `source`.

- El proyecto usa Django y SQLite por defecto para desarrollo local.
