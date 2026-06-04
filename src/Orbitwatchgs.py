# ============================================================================
# ORBITWATCH - Plataforma de Monitoramento Ambiental via Dados Orbitais NASA
# Global Solution 2026 - FIAP | Engenharia de Software - 1º Semestre
# Disciplina: Computational Thinking Using Python
# ============================================================================

# -----------------------------------------------------------------------------
# 1. DEFINIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Eventos ambientais críticos como queimadas, desmatamento e anomalias
# climáticas muitas vezes são detectados tarde demais, agravando seus impactos.
# A falta de acesso a dados de monitoramento contínuo e em tempo real dificulta
# a resposta rápida de autoridades, pesquisadores e cidadãos.
#
# SOLUÇÃO: O OrbitWatch utiliza dados orbitais de satélites da NASA para
# monitorar em tempo real esses eventos, transformando dados espaciais brutos
# em informação acessível. A solução conecta a infraestrutura espacial já
# existente (satélites FIRMS, EONET, APOD) a um problema ambiental urgente
# na Terra — e não existiria sem essa infraestrutura orbital.
# -----------------------------------------------------------------------------

import requests

API_KEY = "z9qtFmVtl57soBw9Bsx1sKyfzAgKKlqfxtGvmFqS"

# -----------------------------------------------------------------------------
# 2. LISTAS DE DADOS DO PROJETO (4 listas com 20 itens cada)
# -----------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------
# 3. FUNÇÕES AUXILIARES
# -----------------------------------------------------------------------------

def aguardar_retorno():
    """Pausa e pergunta se o usuário quer voltar ao menu ou sair."""
    print("\n" + "-"*55)
    print("  V. Voltar ao menu principal")
    print("  0. Sair")
    print("-"*55)
    while True:
        acao = input("  Escolha: ").strip().upper()
        if acao == "V":
            return True   # voltar ao menu
        elif acao == "0":
            return False  # sair
        else:
            print("  ✗ Digite V para voltar ou 0 para sair.")


def exibir_lista(nome_lista, itens):
    """Exibe os itens de uma lista numerada."""
    print(f"\n{'='*55}")
    print(f"  {nome_lista} ({len(itens)} itens)")
    print(f"{'='*55}")
    for i, item in enumerate(itens, start=1):
        print(f"  {i:02d}. {item}")


def classificar_evento(evento):
    """Classifica um evento ambiental por categoria usando match/case."""
    t = evento.lower()
    match True:
        case _ if any(p in t for p in ["queimada", "incêndio", "fumaça", "wildfire", "fire"]):
            return "🔥 Fogo / Queimada"
        case _ if any(p in t for p in ["furacão", "ciclone", "tempestade", "storm", "hurricane", "typhoon"]):
            return "🌀 Tempestade"
        case _ if any(p in t for p in ["inundação", "enchente", "flood"]):
            return "🌊 Inundação"
        case _ if any(p in t for p in ["vulcão", "erupção", "volcano", "eruption"]):
            return "🌋 Vulcânico"
        case _ if any(p in t for p in ["desmatamento", "erosão", "alga"]):
            return "🌿 Vegetação / Solo"
        case _ if any(p in t for p in ["gelo", "neve", "geleira", "ice", "iceberg", "snow"]):
            return "🧊 Criosfera"
        case _ if any(p in t for p in ["seca", "drought"]):
            return "☀️ Seca"
        case _ if any(p in t for p in ["earthquake", "seismic"]):
            return "🌐 Sísmico"
        case _:
            return "🌍 Atmosférico / Outros"


# -----------------------------------------------------------------------------
# 4. FUNÇÕES DE CADA OPÇÃO DO MENU
# -----------------------------------------------------------------------------

def tela_eventos_eonet():
    """Busca e exibe eventos naturais ativos via NASA EONET."""
    try:
        url = "https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=100"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            eventos = response.json().get("events", [])
            if not eventos:
                print("\n⚠ Nenhum evento ativo no momento.")
            else:
                print(f"\n✓ {len(eventos)} evento(s) ATIVO(S) agora — Fonte: NASA EONET\n")
                print(f"{'#':<4} {'Evento':<40} {'Categoria':<22} {'Data'}")
                print("-" * 85)
                for i, evento in enumerate(eventos, start=1):
                    titulo    = evento.get("title", "Sem título")[:38]
                    categoria = evento["categories"][0]["title"] if evento.get("categories") else "N/A"
                    geo       = evento.get("geometry", [])
                    data      = geo[-1]["date"][:10] if geo else "N/A"
                    print(f"{i:<4} {titulo:<40} {categoria:<22} {data}")

        elif response.status_code == 503:
            print("\n⚠ EONET temporariamente indisponível (503). Tente novamente em instantes.")
        else:
            print(f"\n✗ Erro EONET: status {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("\n✗ Sem conexão com a internet.")
    except requests.exceptions.Timeout:
        print("\n✗ Tempo de resposta esgotado.")
    except Exception as e:
        print(f"\n✗ Erro inesperado: {e}")


def tela_satelites():
    """Exibe a lista de satélites e sensores com classificação."""
    exibir_lista("Satélites e Sensores NASA", satelites_sensores)


def tela_eventos_ambientais():
    """Exibe a lista de eventos ambientais com classificação automática."""
    exibir_lista("Eventos Ambientais Monitorados", eventos_ambientais)
    print("\n  --- Classificação automática ---")
    for evento in eventos_ambientais:
        print(f"  • {evento:<40} → {classificar_evento(evento)}")


def tela_apis():
    """Exibe a lista de APIs NASA utilizadas."""
    exibir_lista("APIs NASA Utilizadas", apis_nasa)


def tela_impactos():
    """Exibe a lista de impactos esperados da solução."""
    exibir_lista("Impactos da Solução OrbitWatch", impactos_solucao)


# -----------------------------------------------------------------------------
# 5. MENU PRINCIPAL E LOOP
# -----------------------------------------------------------------------------

def exibir_menu():
    """Exibe o menu principal."""
    print("\n" + "="*55)
    print("        ORBITWATCH - Monitoramento Orbital")
    print("="*55)
    print("  1. Eventos naturais ativos agora (EONET)")
    print("  2. Satélites e sensores")
    print("  3. Eventos ambientais monitorados")
    print("  4. APIs NASA utilizadas")
    print("  5. Impactos da solução")
    print("  0. Sair")
    print("="*55)


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
                tela_satelites()
                rodando = aguardar_retorno()
            case 3:
                tela_eventos_ambientais()
                rodando = aguardar_retorno()
            case 4:
                tela_apis()
                rodando = aguardar_retorno()
            case 5:
                tela_impactos()
                rodando = aguardar_retorno()
            case 0:
                rodando = False
            case _:
                print("\n  ✗ Opção inválida. Tente novamente.")

    print("\n  Encerrando OrbitWatch. Até logo!\n")


if __name__ == "__main__":
    main()
    
    