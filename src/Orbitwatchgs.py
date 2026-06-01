# =============================================================================
# ORBITWATCH - Gerador de Relatório em Tempo Real
# Global Solution 2025 - FIAP | Engenharia de Software - 1º Semestre
# Disciplina: Computational Thinking Using Python
# =============================================================================

import requests
import webbrowser
import os
from datetime import datetime

API_KEY = "z9qtFmVtl57soBw9Bsx1sKyfzAgKKlqfxtGvmFqS"

# -----------------------------------------------------------------------------
# FUNÇÕES
# -----------------------------------------------------------------------------

def buscar_apod():
    """Busca a imagem astronômica do dia via API APOD da NASA."""
    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✓ APOD carregado.")
            return response.json()
        else:
            print(f"✗ Erro APOD: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Erro APOD: {e}")
        return None


def buscar_eventos_eonet(limite=20):
    """Busca eventos naturais ativos agora via API EONET da NASA (sem chave)."""
    try:
        url = f"https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit={limite}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            eventos = response.json().get("events", [])
            print(f"✓ {len(eventos)} evento(s) EONET carregado(s).")
            return eventos
        else:
            print(f"✗ Erro EONET: {response.status_code}")
            return []
    except Exception as e:
        print(f"✗ Erro EONET: {e}")
        return []


def classificar_evento(titulo):
    """Classifica um evento por categoria usando match/case."""
    t = titulo.lower()
    match True:
        case _ if any(p in t for p in ["fire", "wildfire", "queimada", "fumaça"]):
            return "🔥 Queimada"
        case _ if any(p in t for p in ["storm", "hurricane", "cyclone", "typhoon"]):
            return "🌀 Tempestade"
        case _ if any(p in t for p in ["flood", "inundação"]):
            return "🌊 Inundação"
        case _ if any(p in t for p in ["volcano", "eruption", "vulcão"]):
            return "🌋 Vulcão"
        case _ if any(p in t for p in ["iceberg", "ice", "snow", "gelo"]):
            return "🧊 Criosfera"
        case _ if any(p in t for p in ["drought", "seca"]):
            return "☀️ Seca"
        case _ if any(p in t for p in ["earthquake", "seismic"]):
            return "🌐 Sísmico"
        case _:
            return "🌍 Outros"


def gerar_html(dados_apod, eventos_eonet):
    """Monta e abre o relatório HTML com dados em tempo real da NASA."""

    # --- APOD ---
    if dados_apod:
        titulo_apod = dados_apod.get("title", "N/A")
        data_apod   = dados_apod.get("date", "N/A")
        explicacao  = dados_apod.get("explanation", "")
        media_url   = dados_apod.get("url", "")
        media_type  = dados_apod.get("media_type", "image")

        if media_type == "video":
            midia_html = f'<iframe src="{media_url}" width="100%" height="460" frameborder="0" allowfullscreen></iframe>'
        else:
            midia_html = f'<img src="{media_url}" alt="{titulo_apod}">'

        secao_apod = f"""
        <section class="card">
            <h2>📸 Imagem Astronômica do Dia</h2>
            <h3>{titulo_apod}</h3>
            <span class="sub">{data_apod}</span>
            {midia_html}
            <p>{explicacao}</p>
        </section>"""
    else:
        secao_apod = "<section class='card'><h2>📸 APOD</h2><p>Não foi possível carregar os dados.</p></section>"

    # --- EONET ---
    if eventos_eonet:
        linhas = ""
        for ev in eventos_eonet:
            nome      = ev.get("title", "N/A")
            categoria = ev["categories"][0]["title"] if ev.get("categories") else "N/A"
            geo       = ev.get("geometry", [])
            data_ev   = geo[-1]["date"][:10] if geo else "N/A"
            coords    = geo[-1].get("coordinates", None) if geo else None
            coord_str = f"{coords[1]:.2f}, {coords[0]:.2f}" if coords and isinstance(coords[0], float) else "N/A"
            tipo      = classificar_evento(nome)
            maps_url  = f"https://www.google.com/maps?q={coords[1]},{coords[0]}" if coords and isinstance(coords[0], float) else "#"

            linhas += f"""
            <tr>
                <td>{tipo}</td>
                <td><a href="{maps_url}" target="_blank">{nome}</a></td>
                <td>{categoria}</td>
                <td>{data_ev}</td>
                <td>{coord_str}</td>
            </tr>"""

        secao_eonet = f"""
        <section class="card">
            <h2>🌍 Eventos Naturais Ativos Agora — NASA EONET</h2>
            <p class="sub">Dados em tempo real · {len(eventos_eonet)} evento(s) aberto(s) · Fonte: NASA Earth Observatory</p>
            <table>
                <thead>
                    <tr>
                        <th>Tipo</th>
                        <th>Evento</th>
                        <th>Categoria</th>
                        <th>Data</th>
                        <th>Coordenadas</th>
                    </tr>
                </thead>
                <tbody>{linhas}</tbody>
            </table>
        </section>"""
    else:
        secao_eonet = "<section class='card'><h2>🌍 EONET</h2><p>Nenhum evento ativo encontrado.</p></section>"

    # --- HTML FINAL ---
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OrbitWatch — Relatório em Tempo Real</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: #060d1a;
            color: #d0dff0;
            font-family: 'Segoe UI', Arial, sans-serif;
            padding: 40px 20px;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        header h1 {{
            font-size: 2.2rem;
            color: #4fc3f7;
            letter-spacing: 2px;
        }}
        header p {{
            color: #607d9e;
            margin-top: 6px;
            font-size: 0.9rem;
        }}
        .badge {{
            display: inline-block;
            background: #0d2137;
            color: #4fc3f7;
            border: 1px solid #1e4a70;
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            margin: 4px 3px;
        }}
        .card {{
            background: #0b1628;
            border: 1px solid #1a2e47;
            border-radius: 12px;
            padding: 28px;
            margin-bottom: 28px;
            max-width: 960px;
            margin-left: auto;
            margin-right: auto;
        }}
        h2 {{
            color: #81d4fa;
            font-size: 1.2rem;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid #1a2e47;
        }}
        h3 {{ color: #cce8ff; margin: 12px 0 4px; }}
        .sub {{ color: #607d9e; font-size: 0.85rem; display: block; margin-bottom: 12px; }}
        img, iframe {{
            width: 100%;
            border-radius: 8px;
            margin: 16px 0;
        }}
        p {{ line-height: 1.75; color: #9ab5cc; margin-top: 8px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 0.88rem; }}
        th {{
            background: #0d2137;
            color: #4fc3f7;
            padding: 10px 12px;
            text-align: left;
            border-bottom: 2px solid #1a3a5c;
        }}
        td {{
            padding: 9px 12px;
            border-bottom: 1px solid #111d2e;
            color: #b0c8e0;
        }}
        tr:hover td {{ background: #0d1e33; }}
        a {{ color: #4fc3f7; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        footer {{
            text-align: center;
            color: #2a4060;
            font-size: 0.8rem;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #0d1e33;
        }}
    </style>
</head>
<body>
    <header>
        <h1>🛰 OrbitWatch</h1>
        <p>Monitoramento Ambiental via Dados Orbitais NASA</p>
        <div style="margin-top:12px">
            <span class="badge">NASA DATA</span>
            <span class="badge">TEMPO REAL</span>
            <span class="badge">GLOBAL SOLUTION 2025</span>
            <span class="badge">FIAP</span>
        </div>
        <p style="margin-top:14px">Relatório gerado em {agora}</p>
    </header>

    {secao_eonet}
    {secao_apod}

    <footer>
        OrbitWatch &copy; {datetime.now().year} — Global Solution FIAP &nbsp;|&nbsp;
        Dados: <a href="https://api.nasa.gov">NASA Open APIs</a> &amp;
        <a href="https://eonet.gsfc.nasa.gov">NASA EONET</a>
    </footer>
</body>
</html>"""

    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orbitwatch_relatorio.html")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✓ Relatório gerado: {caminho}")
    webbrowser.open(f"file:///{caminho}")


# -----------------------------------------------------------------------------
# EXECUÇÃO DIRETA
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n🛰 OrbitWatch — Gerando relatório em tempo real...\n")
    dados_apod    = buscar_apod()
    eventos_eonet = buscar_eventos_eonet(limite=20)
    gerar_html(dados_apod, eventos_eonet)
    print("\n✓ Pronto! O relatório foi aberto no navegador.")
    