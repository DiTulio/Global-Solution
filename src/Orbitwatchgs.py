"""OrbitWatch - Monitoramento ambiental via dados orbitais da NASA (EONET)."""
import requests

# truststore e opcional: ajuda em redes com certificados corporativos/escolares.
try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

satelites_sensores = [
    "TERRA - satélite NASA lançado em 1999",
    "AQUA - satélite NASA lançado em 2002",
    "SUOMI NPP - monitoramento climático",
    "NOAA-20 - dados atmosféricos",
    "Landsat 8 - imagens de superfície terrestre",
    "Landsat 9 - resolução melhorada",
    "GOES-16 - monitoramento meteorológico",
    "GOES-18 - cobertura do Pacífico",
    "Sentinel-2 - vegetação e solo",
    "Sentinel-5P - qualidade do ar",
    "MODIS - detecção de queimadas (FIRMS)",
    "VIIRS - imagens noturnas e térmicas",
    "ICESat-2 - altimetria polar",
    "GRACE-FO - gravidade e água subterrânea",
    "OCO-2 - concentração de CO₂",
    "CALIPSO - aerossóis e nuvens",
    "CloudSat - estrutura de nuvens",
    "SMAP - umidade do solo",
    "GPM - precipitação global",
    "TRMM - chuvas tropicais"
]

eventos_ambientais = [
    "Queimadas e incêndios florestais",
    "Desmatamento em tempo real",
    "Furacões e ciclones tropicais",
    "Terremotos e atividade sísmica",
    "Erupções vulcânicas",
    "Inundações e enchentes",
    "Secas prolongadas",
    "Derretimento de geleiras",
    "Elevação do nível do mar",
    "Tempestades de areia e poeira",
    "Deslizamentos de terra",
    "Florações de algas (bloom)",
    "Erosão costeira",
    "Anomalias de temperatura superficial",
    "Buracos de ozônio",
    "Poluição atmosférica urbana",
    "Vazamentos de óleo no oceano",
    "Ondas de calor extremas",
    "Neve e cobertura de gelo",
    "Fumaça e aerossóis atmosféricos"
]

apis_nasa = [
    "APOD - Astronomy Picture of the Day",
    "FIRMS - Fire Information for Resource Management",
    "EONET - Earth Observatory Natural Event Tracker",
    "NASA Earthdata - repositório de dados ambientais",
    "GIBS - Global Imagery Browse Services",
    "CMR - Common Metadata Repository",
    "NASA POWER - dados meteorológicos e solares",
    "Exoplanet Archive API",
    "NASA Image and Video Library",
    "Open APIs - dados abertos da NASA",
    "DONKI - notificações de clima espacial",
    "MarsWeather - clima em Marte",
    "NeoWs - objetos próximos da Terra",
    "Insight Mars Lander API",
    "NASA Techport - projetos tecnológicos",
    "GeneLab - biologia no espaço",
    "HelioViewer API - imagens solares",
    "LAADS DAAC - dados atmosféricos",
    "LP DAAC - dados de superfície terrestre",
    "PO.DAAC - dados de oceanografia"
]

impactos_solucao = [
    "Detecção precoce de queimadas no Brasil",
    "Redução do tempo de resposta a desastres naturais",
    "Apoio à fiscalização ambiental com dados reais",
    "Democratização do acesso a dados satelitais",
    "Suporte a pesquisadores e universidades",
    "Monitoramento do desmatamento na Amazônia",
    "Alertas automáticos para defesa civil",
    "Visualização acessível de dados complexos",
    "Integração com sistemas de gestão municipal",
    "Apoio a políticas públicas ambientais",
    "Redução de custos de monitoramento tradicional",
    "Cobertura nacional sem infraestrutura física",
    "Histórico de eventos para análise científica",
    "Transparência de dados ambientais ao cidadão",
    "Complemento a sensores locais (edge computing)",
    "Alerta de fumaça e qualidade do ar",
    "Monitoramento de bacias hidrográficas",
    "Suporte à agricultura de precisão",
    "Identificação de áreas de risco",
    "Contribuição para metas do Acordo de Paris"
]

EONET_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"
BBOX_BRASIL = "-74,5.3,-34.7,-33.8"  # oeste, norte, leste, sul (aproximado)

# Radicais (sem plural/acento) para a classificacao funcionar em PT e EN.
CATEGORIAS = {
    "fogo": ["queimada", "incêndio", "fumaça", "wildfire", "fire", "smoke"],
    "tempestade": ["furac", "ciclone", "tempestade", "storm", "hurricane", "typhoon", "cyclone"],
    "inundacao": ["inunda", "enchente", "flood"],
    "vulcao": ["vulc", "erup", "volcano", "eruption"],
    "vegetacao": ["desmat", "erosão", "alga", "deslizamento", "landslide", "water color"],
    "gelo": ["gelo", "neve", "geleira", "iceberg", "snow", "sea and lake ice"],
    "seca": ["seca", "drought"],
    "sismo": ["terremot", "sism", "earthquake", "seismic"],
}


def classificar_evento(texto):
    """Classifica um evento (titulo ou categoria) usando match/case."""
    t = texto.lower()
    chave = next(
        (c for c, palavras in CATEGORIAS.items() if any(p in t for p in palavras)),
        "outros",
    )
    match chave:
        case "fogo":
            return "Fogo / Queimada"
        case "tempestade":
            return "Tempestade"
        case "inundacao":
            return "Inundação"
        case "vulcao":
            return "Vulcânico"
        case "vegetacao":
            return "Vegetação / Solo"
        case "gelo":
            return "Criosfera"
        case "seca":
            return "Seca"
        case "sismo":
            return "Sísmico"
        case _:
            return "Atmosférico / Outros"


def buscar_eventos_eonet(bbox=None):
    """Busca eventos abertos na NASA EONET. Retorna a lista ou None em caso de erro."""
    params = {"status": "open", "limit": 100}
    if bbox:
        params["bbox"] = bbox
    try:
        response = requests.get(EONET_URL, params=params, timeout=15)
        if response.status_code == 200:
            return response.json().get("events", [])
        elif response.status_code == 503:
            print("\n⚠ EONET temporariamente indisponível (503). Tente novamente em instantes.")
        else:
            print(f"\n✗ Erro EONET: status {response.status_code}")
    except requests.exceptions.Timeout:
        print("\n✗ A NASA demorou demais para responder.")
    except requests.exceptions.SSLError as e:
        print(f"\n✗ Erro de certificado SSL.\nDetalhes: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"\n✗ Não foi possível conectar à NASA EONET.\nDetalhes: {e}")
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Erro na requisição HTTP.\nDetalhes: {e}")
    except Exception as e:
        print(f"\n✗ Erro inesperado: {e}")
    return None


def exibir_eventos(eventos, escopo):
    """Imprime a tabela de eventos, incluindo a classificação OrbitWatch."""
    if eventos is None:
        return
    if not eventos:
        print(f"\n⚠ Nenhum evento natural ativo encontrado ({escopo}).")
        return
    print(f"\n✓ {len(eventos)} evento(s) ATIVO(S) — {escopo} — Fonte: NASA EONET\n")
    print(f"{'#':<4} {'Evento':<38} {'Categoria NASA':<20} {'Classe OrbitWatch':<22} Data")
    print("-" * 100)
    for i, evento in enumerate(eventos, start=1):
        titulo = evento.get("title", "Sem título")[:36]
        cats = evento.get("categories", [])
        categoria = cats[0].get("title", "N/A") if cats else "N/A"
        geo = evento.get("geometry", [])
        data = geo[-1].get("date", "N/A")[:10] if geo else "N/A"
        classe = classificar_evento(f"{evento.get('title', '')} {categoria}")
        print(f"{i:<4} {titulo:<38} {categoria[:18]:<20} {classe:<22} {data}")


def tela_eventos_eonet():
    """Eventos naturais ativos no mundo."""
    print("\nConsultando eventos naturais ativos no mundo...")
    exibir_eventos(buscar_eventos_eonet(), "mundo")


def tela_eventos_brasil():
    """Eventos naturais ativos na região do Brasil (bounding box aproximada)."""
    print("\nConsultando eventos naturais ativos na região do Brasil...")
    exibir_eventos(buscar_eventos_eonet(BBOX_BRASIL), "região do Brasil")


def aguardar_retorno():
    """Pausa e pergunta se o usuário quer voltar ao menu ou sair."""
    print("\n" + "-" * 55)
    print("  V. Voltar ao menu principal")
    print("  0. Sair")
    print("-" * 55)
    while True:
        acao = input("  Escolha: ").strip().upper()
        if acao == "V":
            return True
        elif acao == "0":
            return False
        else:
            print("  ✗ Digite V para voltar ou 0 para sair.")


def exibir_lista(nome_lista, itens):
    """Exibe os itens de uma lista numerada."""
    print(f"\n{'=' * 55}")
    print(f"  {nome_lista} ({len(itens)} itens)")
    print(f"{'=' * 55}")
    for i, item in enumerate(itens, start=1):
        print(f"  {i:02d}. {item}")


def tela_satelites():
    exibir_lista("Satélites e Sensores NASA", satelites_sensores)


def tela_eventos_ambientais():
    exibir_lista("Eventos Ambientais Monitorados", eventos_ambientais)
    print("\n  --- Classificação automática ---")
    for evento in eventos_ambientais:
        print(f"  • {evento:<40} → {classificar_evento(evento)}")


def tela_apis():
    exibir_lista("APIs NASA Utilizadas", apis_nasa)


def tela_impactos():
    exibir_lista("Impactos da Solução OrbitWatch", impactos_solucao)


def exibir_menu():
    """Exibe o menu principal (numeração igual à do match/case em main)."""
    print("\n" + "=" * 55)
    print("        ORBITWATCH - Monitoramento Orbital")
    print("=" * 55)
    print("  1. Eventos naturais ativos agora (mundo)")
    print("  2. Eventos naturais ativos agora (Brasil)")
    print("  3. Satélites e sensores")
    print("  4. Eventos ambientais monitorados")
    print("  5. APIs NASA utilizadas")
    print("  6. Impactos da solução")
    print("  0. Sair")
    print("=" * 55)


def main():
    """Função principal do OrbitWatch."""
    print("\n🛰  Bem-vindo ao OrbitWatch — Monitoramento Ambiental via Satélite NASA")

    rodando = True
    while rodando:
        exibir_menu()
        try:
            opcao = int(input("\n  Escolha uma opção: "))
        except ValueError:
            print("  ✗ Digite apenas números.")
            continue

        match opcao:
            case 1:
                tela_eventos_eonet()
                rodando = aguardar_retorno()
            case 2:
                tela_eventos_brasil()
                rodando = aguardar_retorno()
            case 3:
                tela_satelites()
                rodando = aguardar_retorno()
            case 4:
                tela_eventos_ambientais()
                rodando = aguardar_retorno()
            case 5:
                tela_apis()
                rodando = aguardar_retorno()
            case 6:
                tela_impactos()
                rodando = aguardar_retorno()
            case 0:
                rodando = False
            case _:
                print("\n  ✗ Opção inválida. Tente novamente.")

    print("\n  Encerrando OrbitWatch. Até logo!\n")


if __name__ == "__main__":
    main()
