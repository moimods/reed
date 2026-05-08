import json
from lexer.lexer import LexicalAnalyzer

samples = [
    (
        "python",
        "x = 10\ny = x + 5\nprint(y)\n",
    ),
    (
        "javascript",
        "let a = 1;\nlet b = `template ${a}`;\nswitch(a){case 1:break;}\n",
    ),
]

analyzer = LexicalAnalyzer()
result = {"samples": []}

for lang, code in samples:
    tokens, errors = analyzer.tokenize(code, lenguaje=lang)
    result["samples"].append({
        "language": lang,
        "code": code,
        "tokens": [t.to_dict() for t in tokens],
        "errors": errors,
    })

# Write JSON output and a Markdown document
with open("TOKENS.md", "w", encoding="utf-8") as f_md:
    f_md.write("# Tokens generados por el analizador léxico\n\n")
    for sample in result["samples"]:
        f_md.write(f"## Lenguaje: {sample['language']}\n\n")
        f_md.write("```\n")
        f_md.write(sample["code"])
        f_md.write("```\n\n")
        f_md.write("**Tokens (lista):**\n\n````json\n")
        json.dump(sample["tokens"], f_md, ensure_ascii=False, indent=2)
        f_md.write("\n````\n\n")
        if sample["errors"]:
            f_md.write("**Errores detectados:**\n\n````json\n")
            json.dump(sample["errors"], f_md, ensure_ascii=False, indent=2)
            f_md.write("\n````\n\n")

# Also print JSON to stdout for quick verification
print(json.dumps(result, ensure_ascii=False, indent=2))
