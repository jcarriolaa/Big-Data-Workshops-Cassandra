#!/usr/bin/env bash
# Revisa que tu entorno este como debe estar antes de seguir.
#
#   bash scripts/check.sh prereq    # Paso 0: Docker y la imagen de Cassandra
#   bash scripts/check.sh nodo      # despues del Paso 3: un nodo con las ventas cargadas
#   bash scripts/check.sh cluster   # despues del Paso 6: tres nodos, tu cluster y tus copias
set -uo pipefail
export MSYS_NO_PATHCONV=1

IMAGEN="cassandra:5.0.8"
FALLOS=0
ok()   { echo "✅ $1"; }
warn() { echo "⚠️  $1"; }
fail() { echo "❌ $1"; FALLOS=$((FALLOS + 1)); }

corriendo() { docker inspect -f '{{.State.Running}}' "$1" 2>/dev/null | grep -q true; }
cql()       { docker exec cassandra1 cqlsh --request-timeout=60 -e "$1" 2>/dev/null; }
filas()     { cql "SELECT count(*) FROM ventas.ventas_por_ciudad;" | awk 'NR==4 {print $1+0}'; }

case "${1:-prereq}" in

  prereq)
    docker compose version >/dev/null 2>&1 \
      && ok "docker compose v2 disponible" \
      || fail "no encuentro 'docker compose'. Instala Docker Desktop y abrelo."

    docker info >/dev/null 2>&1 \
      && ok "Docker esta corriendo" \
      || fail "Docker no responde. Abre Docker Desktop y espera a que diga 'running'."

    MEM=$(docker info --format '{{.MemTotal}}' 2>/dev/null || echo 0)
    [ -z "$MEM" ] && MEM=0
    GB=$(awk -v m="$MEM" 'BEGIN {printf "%.1f", m / 1073741824}')
    if [ "$MEM" -ge 2147483648 ]; then
      ok "Docker tiene $GB GB de RAM"
    else
      warn "Docker tiene $GB GB de RAM. Un nodo usa unos 1.3 GB; se recomiendan 2 GB."
    fi

    docker image inspect "$IMAGEN" >/dev/null 2>&1 \
      && ok "imagen $IMAGEN descargada" \
      || fail "falta la imagen. Ejecuta: docker pull $IMAGEN"
    ;;

  nodo)
    corriendo cassandra1 && ok "Contenedor cassandra1 corriendo" \
      || fail "cassandra1 apagado. Revisa: docker compose logs cassandra1"

    docker exec cassandra1 nodetool status 2>/dev/null | grep -q '^UN' \
      && ok "cassandra1 en estado UN" \
      || fail "cassandra1 todavia no esta listo. Espera un minuto y vuelve a intentar."

    N=$(filas)
    [ "${N:-0}" -eq 75000 ] \
      && ok "ventas.ventas_por_ciudad tiene 75000 filas" \
      || fail "ventas.ventas_por_ciudad tiene ${N:-0} filas, deberian ser 75000 (Pasos 2 y 3)."
    ;;

  cluster)
    # En el cluster del grupo hay un nodo por laptop; en la practica opcional, tres.
    LOCALES=$(docker ps --format '{{.Names}}' | grep -E '^cassandra[1-3]$' | sort)
    if [ -n "$LOCALES" ]; then
      ok "Nodos en esta laptop: $(echo $LOCALES)"
    else
      fail "No hay ningun nodo corriendo en esta laptop. Revisa: docker compose ps -a"
    fi
    NODO=$(echo "$LOCALES" | head -1)
    [ -n "$NODO" ] && [ "$NODO" != cassandra1 ] && cql() { docker exec "$NODO" cqlsh --request-timeout=60 -e "$1" 2>/dev/null; }

    UN=$(docker exec "${NODO:-cassandra1}" nodetool status 2>/dev/null | grep -c '^UN')
    [ "${UN:-0}" -eq 3 ] && ok "Nodos en estado UN: 3" \
      || fail "Nodos en estado UN: ${UN:-0}, deberian ser 3."

    NOMBRE=$(docker exec "${NODO:-cassandra1}" nodetool describecluster 2>/dev/null | awk -F': ' '/Name:/ {print $2; exit}')
    [[ "${NOMBRE:-}" =~ ^UFM-G[1-4]$ ]] && ok "Nombre del cluster: $NOMBRE" \
      || fail "El cluster se llama '${NOMBRE:-?}', deberia ser UFM-G# (Paso 5)."

    DC=$(docker exec "${NODO:-cassandra1}" nodetool status 2>/dev/null | awk '/^Datacenter:/ {print $2; exit}')
    [[ "${DC:-}" =~ ^dc-g[1-4]$ ]] && ok "Datacenter: $DC" \
      || fail "El datacenter es '${DC:-?}', deberia ser dc-g# (Paso 5)."

    cql "DESCRIBE KEYSPACE ventas;" | grep -q "'NetworkTopologyStrategy', '${DC:-x}': '3'" \
      && ok "Keyspace ventas con 3 copias en $DC" \
      || fail "El keyspace ventas no tiene NetworkTopologyStrategy con 3 copias en tu datacenter (Paso 6)."

    N=$(filas)
    [ "${N:-0}" -ge 75000 ] \
      && ok "ventas.ventas_por_ciudad tiene $N filas" \
      || fail "ventas.ventas_por_ciudad tiene ${N:-0} filas, deberian ser al menos 75000 (Paso 6)."
    ;;

  *)
    echo "Uso: bash scripts/check.sh [prereq|nodo|cluster]"
    exit 2
    ;;
esac

echo
if [ "$FALLOS" -eq 0 ]; then
  echo "Todo en orden."
else
  echo "$FALLOS problema(s). Mira la seccion '❌ Si falla' del paso correspondiente."
fi
exit "$FALLOS"
