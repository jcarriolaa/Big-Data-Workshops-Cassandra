#!/usr/bin/env python3
"""Desnormaliza los CSV de G1-spotify para las tablas de modelo.cql (joins hechos aquí)."""
import csv, sys
from pathlib import Path
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "G1-spotify"
OUT = Path(__file__).resolve().parent
rd = lambda n: list(csv.DictReader(open(SRC / f"{n}.csv", encoding="utf-8")))
def wr(n, cols, rows):
    with open(OUT / f"{n}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(cols); w.writerows(rows)
can = {c["cancion_id"]: c for c in rd("canciones")}
rep = rd("reproducciones")
wr("usuarios", ["usuario_id", "nombre", "pais", "plan"],
   [[u[k] for k in ("usuario_id", "nombre", "pais", "plan")] for u in rd("usuarios")])
wr("reproducciones_por_usuario", ["usuario_id", "reproducida_en", "reproduccion_id", "cancion_id", "titulo", "artista"],
   [[r["usuario_id"], r["reproducida_en"], r["reproduccion_id"], r["cancion_id"],
     can[r["cancion_id"]]["titulo"], can[r["cancion_id"]]["artista"]] for r in rep])
wr("canciones_por_playlist", ["playlist_id", "posicion", "cancion_id", "titulo", "artista"],
   [[p["playlist_id"], p["posicion"], p["cancion_id"], can[p["cancion_id"]]["titulo"],
     can[p["cancion_id"]]["artista"]] for p in rd("playlist_canciones")])
wr("reproducciones_por_cancion_dia", ["cancion_id", "dia", "reproducida_en", "reproduccion_id", "usuario_id"],
   [[r["cancion_id"], r["reproducida_en"][:10], r["reproducida_en"], r["reproduccion_id"], r["usuario_id"]] for r in rep])
