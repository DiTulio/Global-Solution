"""Servidor local do OrbitWatch: liga a página HTML ao código Python (Orbitwatchgs.py).

Local:  pip install -r requirements.txt  ->  python src/server.py  ->  http://127.0.0.1:5000
Vercel: a página fica em public/index.html (servida como estático) e este arquivo
        vira a função Python (entrypoint "src.server:app" no pyproject.toml).
"""
import os
from flask import Flask, jsonify, request, send_from_directory
try:  # na Vercel o módulo é carregado como "src.server"
    from . import Orbitwatchgs as ow
except ImportError:  # rodando direto: python src/server.py
    import Orbitwatchgs as ow

app = Flask(__name__)
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raiz do projeto


@app.after_request
def liberar_cors(resp):
    # Permite abrir o .html direto do disco e ainda falar com este servidor.
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.get("/")
def index():
    """Só para uso local: na Vercel, public/index.html é servido como arquivo estático."""
    pasta = os.path.join(BASE, "public")
    if not os.path.exists(os.path.join(pasta, "index.html")):
        return jsonify(erro="public/index.html não encontrado"), 404
    return send_from_directory(pasta, "index.html")


def coordenadas(geometria):
    c = geometria["coordinates"]
    while isinstance(c[0], list):  # polígonos: usa o primeiro ponto
        c = c[0]
    return c


@app.get("/api/eventos")
def eventos():
    """Eventos ativos da EONET, buscados e classificados pelo código Python."""
    escopo = request.args.get("escopo", "mundo")
    brutos = ow.buscar_eventos_eonet(ow.BBOX_BRASIL if escopo == "brasil" else None)
    if brutos is None:
        return jsonify(erro="Falha ao consultar a NASA EONET"), 502
    saida = []
    for e in brutos:
        if not e.get("geometry"):
            continue
        geo = e["geometry"][-1]
        lon, lat = coordenadas(geo)[:2]
        cats = e.get("categories") or [{}]
        categoria = cats[0].get("title", "N/A")
        saida.append({
            "id": e["id"], "title": e.get("title", "Sem título"), "cat": categoria,
            "lon": lon, "lat": lat, "date": geo.get("date", "")[:10],
            "classe": ow.classificar_evento(f"{e.get('title', '')} {categoria}"),
        })
    return jsonify(eventos=saida, escopo=escopo, fonte="NASA EONET")


@app.get("/api/listas")
def listas():
    return jsonify(
        satelites=ow.satelites_sensores, eventos=ow.eventos_ambientais,
        apis=ow.apis_nasa, impactos=ow.impactos_solucao,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
