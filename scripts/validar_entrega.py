#!/usr/bin/env python3
"""Revisa que tu entrega esté completa antes de que el catedrático la califique.

Se corre solo en cada Pull Request, y también lo puedes correr tú:

    python3 scripts/validar_entrega.py entregas/G1/20241234-juan-perez

Solo revisa lo mecánico: que estén los archivos, que las capturas pesen poco, que no hayas dejado
las líneas de ayuda de la plantilla. NO califica: la calidad de tus respuestas y de tu modelo la
evalúa el catedrático.

Termina con código 1 si hay algún ❌.
"""
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

MAX_IMG = 1_000_000            # 1 MB por captura (1 millón de bytes)
CAPTURAS = ["E1", "E2", "E3", "E4", "E5", "E6a", "E6b"]
ARCHIVOS = ["bitacora.md", "check.txt", "compose.yml",
            "mini-reto/modelo.cql", "mini-reto/consultas.cql", "mini-reto/resultados.txt"]
PREGUNTAS = 3
MIN_PALABRAS = 15

# Frases de la plantilla que hay que borrar antes de entregar
AYUDAS = ["Copia este archivo a tu carpeta", "Debajo de cada captura, una o dos frases",
          "si la lectura respondió", "Los archivos van en `mini-reto/`", "Una fila por tabla.",
          "Qué falló, qué intentaste"]

# Lo que tiene que decir check.txt (sale de los ok() de scripts/check.sh cluster)
CADENAS_CHECK = ["Nodos en estado UN: 3", "Nombre del cluster:", "Datacenter:"]

resultados = []


def ok(n, d=""):   resultados.append(("✅", n, d))
def warn(n, d=""): resultados.append(("⚠️", n, d))
def fail(n, d=""): resultados.append(("❌", n, d))


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True).stdout
    except OSError:
        return ""


def palabras(texto):
    texto = "\n".join(l for l in texto.splitlines() if not l.strip().startswith(">"))
    return len(texto.split())


def main():
    carpeta = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else detectar()
    if not carpeta:
        print("No supe qué carpeta revisar. Uso: python3 scripts/validar_entrega.py entregas/G1/<tu-carpeta>")
        return 2

    dir_ = RAIZ / carpeta

    # --- T1: la carpeta se llama como debe
    m = re.fullmatch(r"entregas/(G[1-4])/(\d+)-([a-z][a-z0-9-]*[a-z0-9])", carpeta)
    if m:
        ok("T1 carpeta", carpeta)
    else:
        fail("T1 carpeta", f"{carpeta} no sigue entregas/G#/<carné>-<nombre>-<apellido>, "
                           "todo en minúsculas y sin tildes ni ñ")
    if not dir_.is_dir():
        fail("T1 carpeta", f"no existe {carpeta}")
        return terminar(carpeta)

    # --- T2: no tocaste nada fuera de tu carpeta
    base = os.environ.get("BASE_REF") or base_local()
    cambios = [l for l in git("diff", "--name-only", f"{base}...HEAD").splitlines() if l.strip()]
    fuera = [c for c in cambios if not c.startswith(carpeta + "/")]
    if not cambios:
        warn("T2 solo tu carpeta", "no pude comparar con main")
    elif fuera:
        fail("T2 solo tu carpeta", "tocas archivos fuera: " + ", ".join(fuera[:3]))
    else:
        ok("T2 solo tu carpeta")

    # --- T3: la rama se llama como debe
    rama = (os.environ.get("RAMA") or git("rev-parse", "--abbrev-ref", "HEAD")).strip()
    if rama and rama not in ("HEAD", "main"):
        if re.fullmatch(r"entrega-\d+-[a-z][a-z0-9-]*[a-z0-9]", rama):
            ok("T3 rama", rama)
        else:
            warn("T3 rama", f"{rama}: se esperaba entrega-<carné>-<nombre>-<apellido> en minúsculas")

    # --- T4: están todos los archivos
    faltan = [a for a in ARCHIVOS if not (dir_ / a).exists()]
    if not list((dir_ / "mini-reto").glob("carga.*")):
        faltan.append("mini-reto/carga.*")
    if faltan:
        fail("T4 archivos", "faltan: " + ", ".join(faltan))
    else:
        ok("T4 archivos", f"los {len(ARCHIVOS) + 1} archivos están")

    # --- T5: las capturas (E1 puede venir partida en E1a y E1b, etc.)
    caps = dir_ / "capturas"
    imagenes = [p for p in caps.iterdir() if p.is_file()] if caps.is_dir() else []
    vistas = []
    for e in CAPTURAS:
        patron = re.compile(rf"^{e}([ab])?[-_.]", re.I) if len(e) == 2 else re.compile(rf"^{e}[-_.]", re.I)
        suyas = [p for p in imagenes if patron.match(p.name)]
        if not suyas:
            fail(f"T5 captura {e}", "no está")
            continue
        for img in suyas:
            vistas.append(img)
            if img.suffix.lower() not in (".png", ".jpg", ".jpeg"):
                fail(f"T5 captura {e}", f"{img.name} no es PNG ni JPG")
            elif img.stat().st_size > MAX_IMG:
                fail(f"T5 captura {e}", f"{img.name} pesa {img.stat().st_size / 1_000_000:.2f} MB y el máximo es 1 MB")
            else:
                ok(f"T5 captura {e}", f"{img.name} ({img.stat().st_size / 1000:.0f} KB)")

    # --- T5b: no vale subir la misma imagen para varias evidencias
    hashes = {}
    for img in vistas:
        hashes.setdefault(hashlib.sha256(img.read_bytes()).hexdigest(), []).append(img.name)
    repetidas = [v for v in hashes.values() if len(v) > 1]
    if repetidas:
        fail("T5b capturas repetidas", "la misma imagen en varias evidencias: " + ", ".join(repetidas[0]))
    elif vistas:
        ok("T5b capturas repetidas", "las capturas son distintas entre sí")

    # --- T6: check.txt
    chk = dir_ / "check.txt"
    if chk.exists():
        txt = chk.read_text(errors="replace")
        locales = re.search(r"Nodos en esta laptop:\s*(.*)", txt)
        if "❌" in txt:
            fail("T6 check.txt", "tu check.txt trae ❌: el clúster no estaba completo")
        elif locales and len(locales.group(1).split()) > 1:
            fail("T6 check.txt", "check.txt de tres nodos en una laptop; se espera el del clúster del grupo")
        else:
            faltantes = [c for c in CADENAS_CHECK if c not in txt]
            if faltantes:
                warn("T6 check.txt", "no encuentro: " + "; ".join(faltantes))
            else:
                ok("T6 check.txt", "cluster en verde")

    # --- T7: el compose tiene tres nodos de Cassandra
    comp = dir_ / "compose.yml"
    if comp.exists():
        c = comp.read_text(errors="replace")
        nodos = set(re.findall(r"^\s+[\"']?(cassandra[1-3])[\"']?\s*:", c, re.M))
        con_broadcast = re.search(r"^\s*-?\s*[^#\n]*broadcast_address\S*\s*[:=]\s*\S", c, re.I | re.M)
        if len(nodos) == 1 and con_broadcast:
            ok("T7 compose", f"tu nodo del clúster del grupo: {nodos.pop()}")
        else:
            fail("T7 compose", f"se espera un solo nodo, el tuyo, con su broadcast_address; encuentro "
                               f"{len(nodos)} (Paso 5)")

    # --- T8: la bitácora
    bit_f = dir_ / "bitacora.md"
    if not bit_f.exists():
        fail("T8 bitácora", "no existe bitacora.md")
        return terminar(carpeta)
    bit = bit_f.read_text(errors="replace")

    ay = [a for a in AYUDAS if a in bit]
    if ay:
        fail("T8 plantilla", f"quedaron {len(ay)} líneas de ayuda sin borrar (las que empiezan con >)")
    else:
        ok("T8 plantilla", "sin líneas de ayuda")

    tabla = re.search(r"### Tabla del Paso 8(.*?)(?=\n## |\Z)", bit, re.S)
    marcas = len(re.findall(r"[✅❌]", "\n".join(l for l in tabla.group(1).splitlines() if not l.lstrip().startswith(">")))) if tabla else 0
    if marcas >= 9:
        ok("T8 tabla del Paso 8", "las 9 celdas llenas")
    else:
        fail("T8 tabla del Paso 8", f"{marcas} de 9 celdas llenas")

    respuestas = []
    for i in range(1, PREGUNTAS + 1):
        mm = re.search(rf"\*\*{i}\.\s.*?\*\*(.*?)(?=\n\*\*{i+1}\.\s|\n---\s*\n## |\n## |\Z)", bit, re.S)
        t = (mm.group(1) if mm else "").strip()
        respuestas.append(" ".join(t.split()).lower())
        n = palabras(t)
        if n < MIN_PALABRAS:
            fail(f"T8 pregunta {i}", f"{n} palabras: está vacía o incompleta")
        else:
            ok(f"T8 pregunta {i}", f"{n} palabras")
    llenas = [r for r in respuestas if r]
    if len(llenas) != len(set(llenas)):
        fail("T8 respuestas", "hay respuestas iguales entre sí")

    # --- T9: el mini-reto
    sec = re.search(r"## 3\. Mini-reto(.*?)(?=\n## 4|\Z)", bit, re.S)
    sec = sec.group(1) if sec else ""
    filas = [l for l in sec.splitlines()
             if re.match(r"\s*\|[^|]*\w[^|]*\|[\s`*]*C[1-4]\b[^|]*\|", l)]
    if len(filas) >= 4:
        ok("T9 tablas", "las 4 filas de la tabla del mini-reto llenas")
    else:
        fail("T9 tablas", f"{len(filas)} de 4 filas con nombre de tabla")
    for rotulo in ("Por qué esas llaves", "Qué datos quedaron duplicados",
                   "Qué hace la aplicación si cambia"):
        mm = re.search(rf"\*\*{rotulo}[^*]*\*\*(.*?)(?=\n\*\*(?:Por qué esas|Qué datos|Qué hace)|\n---\s*\n## |\n## |\Z)", sec, re.S)
        n = palabras(mm.group(1)) if mm else 0
        if n < MIN_PALABRAS:
            fail("T9 justificación", f"'{rotulo}': {n} palabras")
        else:
            ok("T9 justificación", f"'{rotulo}': {n} palabras")

    modelo = dir_ / "mini-reto/modelo.cql"
    if modelo.exists():
        mt = modelo.read_text(errors="replace")
        n_tablas = len(re.findall(r"create\s+table", mt, re.I))
        if re.search(r"create\s+keyspace", mt, re.I) and n_tablas >= 4:
            ok("T9 modelo.cql", f"keyspace y {n_tablas} tablas")
        else:
            fail("T9 modelo.cql", f"se esperan CREATE KEYSPACE y 4 CREATE TABLE; hay {n_tablas} tablas")

    cons = dir_ / "mini-reto/consultas.cql"
    if cons.exists():
        ct = re.sub(r"--[^\n]*|//[^\n]*|/\*.*?\*/", "", cons.read_text(errors="replace"), flags=re.S)
        n_sel = len(re.findall(r"\bselect\b", ct, re.I))
        if re.search(r"allow\s+filtering", ct, re.I):
            fail("T9 consultas.cql", "usa ALLOW FILTERING")
        elif n_sel < 4:
            fail("T9 consultas.cql", f"{n_sel} consultas; se esperan 4")
        else:
            ok("T9 consultas.cql", f"{n_sel} consultas, sin ALLOW FILTERING")

    res = dir_ / "mini-reto/resultados.txt"
    if res.exists():
        rt = res.read_text(errors="replace")
        if re.search(r"InvalidRequest|SyntaxException|Error from server", rt):
            fail("T9 resultados.txt", "trae errores de cqlsh")
        elif len(re.findall(r"\(\d+ rows?\)", rt)) < 4:
            fail("T9 resultados.txt", "no encuentro la salida de las 4 consultas")
        else:
            ok("T9 resultados.txt", "salida de las 4 consultas")

    # --- T10: las imágenes que enlaza la bitácora existen
    sin_ayuda = "\n".join(l for l in re.sub(r"<!--.*?-->", "", bit, flags=re.S).splitlines()
                          if not l.lstrip().startswith(">"))
    enlaces = re.findall(r"!\[[^\]]*\]\(([^)\s]+)", sin_ayuda)
    rotos = [e for e in enlaces if not (dir_ / e).exists()]
    if enlaces and rotos:
        fail("T10 enlaces", "la bitácora enlaza imágenes que no están: " + ", ".join(rotos[:3]))
    elif enlaces:
        ok("T10 enlaces", f"las {len(enlaces)} imágenes enlazadas existen")

    # --- T11: tu carné aparece en la bitácora
    if m:
        carne = m.group(2)
        if carne in bit:
            ok("T11 carné", f"{carne} aparece en la bitácora")
        else:
            warn("T11 carné", f"tu carpeta dice {carne} pero ese carné no aparece en la bitácora")

    return terminar(carpeta)


def base_local():
    """Contra qué comparar en la máquina del estudiante: el repo del curso si lo agregó como
    upstream (su fork puede ir atrasado), si no su origin."""
    return "upstream/main" if git("rev-parse", "--verify", "-q", "upstream/main").strip() else "origin/main"


def detectar():
    """Si no me dan la carpeta, la deduzco de los archivos que cambió el PR."""
    base = os.environ.get("BASE_REF") or base_local()
    for linea in git("diff", "--name-only", f"{base}...HEAD").splitlines():
        m = re.match(r"(entregas/G[1-4]/[^/]+)/", linea)
        if m:
            return m.group(1)
    return None


def terminar(carpeta="?"):
    fails = sum(1 for e, _, _ in resultados if e == "❌")
    warns = sum(1 for e, _, _ in resultados if e == "⚠️")
    lineas = [f"## Validación de `{carpeta}`", "",
              f"**{len(resultados) - fails - warns} ✅ · {warns} ⚠️ · {fails} ❌**", "",
              "| | Verificación | Detalle |", "|---|---|---|"]
    lineas += [f"| {e} | {n} | {d} |" for e, n, d in resultados]
    lineas += ["", "Los ⚠️ no bloquean. Los ❌ conviene corregirlos, pero **corregir después de la "
                   "hora de entrega hace tardía toda la entrega**: revisa esto antes de subir, con "
                   "`python3 scripts/validar_entrega.py entregas/G#/<tu-carpeta>`. "
                   "El detalle de la entrega está en "
                   "[ENTREGA.md](https://github.com/jcarriolaa/Big-Data-Workshops-Cassandra/blob/main/ENTREGA.md)."]
    salida = "\n".join(lineas)
    print(salida)
    ruta = os.environ.get("GITHUB_STEP_SUMMARY")
    if ruta:
        with open(ruta, "a") as f:
            f.write(salida + "\n")
    archivo = os.environ.get("SALIDA_MD")
    if archivo:
        Path(archivo).write_text(salida + "\n")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
