# OrbitWatch — Monitoramento Ambiental via Dados Orbitais NASA

> Global Solution 2026 — FIAP | Engenharia de Software — 1º Semestre  
> Disciplina: Computational Thinking with Python

---

## Definição do Problema

Eventos ambientais críticos como queimadas, desmatamento e anomalias climáticas muitas vezes são detectados tarde demais, agravando seus impactos sociais e ambientais. A falta de acesso a dados de monitoramento contínuo e em tempo real dificulta a resposta rápida de autoridades, pesquisadores e cidadãos.

---

## Solução Proposta

O **OrbitWatch** é uma plataforma de monitoramento ambiental que utiliza dados orbitais de satélites da NASA para detectar e acompanhar em tempo real eventos como queimadas, desmatamento e anomalias climáticas.

A solução transforma dados espaciais brutos em informação acessível, conectando a infraestrutura orbital já existente a problemas ambientais urgentes na Terra. **A plataforma não existiria sem os satélites da NASA** — eles são o sensor; a Terra é o painel de controle.

---

## Funcionalidades

- Eventos naturais ativos em tempo real via **NASA EONET**
- Classificação automática de eventos por categoria (queimada, tempestade, vulcão etc.)
- Menu interativo com navegação por opções e retorno ao menu
- Listagem de satélites, eventos ambientais, APIs NASA e impactos da solução

---

## Estruturas de Programação Utilizadas

| Estrutura | Onde é usada |
|---|---|
| `def` (funções) | `exibir_menu()`, `aguardar_retorno()`, `exibir_lista()`, `classificar_evento()`, `tela_eventos_eonet()`, `main()` e outras |
| `try / except` | Tratamento de erros na requisição HTTP (sem conexão, timeout, erro 503, erros genéricos) |
| `match / case` | Menu principal e classificação automática de eventos por categoria |
| `while` (repetição) | Loop principal do menu interativo |
| `if / elif / else` | Verificação de status HTTP e condições de alerta |
| `for` (repetição) | Iteração sobre as listas de dados |

---

## Explicação do Código

### `import requests`
Importa a biblioteca responsável por fazer requisições à internet. É ela que permite ao programa "ligar" para os servidores da NASA e buscar os dados em tempo real.

### Listas de dados
O programa possui 4 listas com 20 itens cada: satélites e sensores, eventos ambientais, APIs da NASA e impactos da solução. Essas listas armazenam as informações do projeto de forma organizada e são percorridas pelo `for` para exibição.

### `def` — Funções
Cada `def` define uma função, ou seja, um bloco de código com uma responsabilidade específica que pode ser chamado quando necessário. Isso evita repetição de código e deixa o programa mais organizado. Exemplos: `tela_eventos_eonet()` busca os dados da NASA, `classificar_evento()` identifica o tipo de desastre, `exibir_lista()` imprime qualquer lista formatada.

### `try / except`
É o mecanismo de tratamento de erros do Python. O bloco `try` tenta executar uma ação — no caso, conectar na NASA. Se algo der errado (sem internet, servidor fora, timeout), o bloco `except` captura o erro e exibe uma mensagem amigável em vez de travar o programa.

### `while` — Repetição
O `while rodando` mantém o menu ativo enquanto o usuário não escolher sair. A cada volta do loop, o menu é exibido e uma nova opção pode ser escolhida. Quando o usuário digita `0`, a variável `rodando` vira `False` e o loop encerra.

### `for` — Repetição em listas
O `for` percorre uma lista do início ao fim, executando uma ação para cada item. É usado para imprimir cada satélite, cada evento ou cada impacto — um por um — sem precisar escrever um `print` para cada linha manualmente.

### `match / case`
Funciona como um seletor inteligente. No menu, direciona o programa para a função correta conforme o número digitado. Na classificação de eventos, analisa o nome do evento e encaixa na categoria correspondente (ex: se o nome contém "wildfire", retorna "Fogo / Queimada"). É mais limpo e legível do que vários `if/elif` seguidos.

---

## Listas de Dados

O projeto contém **4 listas com 20 itens cada**:

1. **Satélites e Sensores** — equipamentos orbitais usados no monitoramento
2. **Eventos Ambientais** — tipos de ocorrências detectadas via satélite
3. **APIs NASA** — serviços de dados utilizados ou integráveis
4. **Impactos da Solução** — benefícios esperados do OrbitWatch

---

## Estrutura do Projeto

```
orbitwatch/
│
├── orbitwatch_gs.py   # Código principal da entrega
└── README.md          # Este arquivo
```

---

## Como Executar

**Pré-requisitos:**
- Python 3.10 ou superior
- Biblioteca `requests` instalada

**Instalação da dependência:**
```bash
pip install requests
```

**Execução:**
```bash
python orbitwatch_gs.py
```

Ao iniciar, o menu interativo será exibido. Navegue pelas opções e pressione **V** para voltar ao menu ou **0** para sair.

---

## API Key

O projeto utiliza a **NASA Open APIs**. A chave já está configurada no código para fins de demonstração acadêmica.

Para gerar sua própria chave gratuita: [https://api.nasa.gov](https://api.nasa.gov)

A API EONET é pública e **não requer chave de acesso**.

---

## Conexão com a Indústria Espacial

O OrbitWatch se conecta diretamente à Indústria Espacial ao consumir dados gerados por satélites em órbita. Entre os sistemas utilizados estão:

- **MODIS / VIIRS** — sensores a bordo dos satélites TERRA e AQUA para detecção de queimadas (FIRMS)
- **EONET** — rastreador de eventos naturais da NASA em tempo real

Sem a infraestrutura orbital, a plataforma não existiria.

---

## Integrantes do Grupo

| Nome |                            | RM     |
|Felipe Romano de Paula Souza       | 571653 |
| Lucas Zarantonelli Lourenço       | 569164 |
| Nicole Barbosa Oliveira de Lima	| 569505 |
| Ryan Romagnoli Santos             | 568845 |
| Vinicius Di Tulio Gomes Silva     | 573019 |

---

## Licença

Projeto acadêmico desenvolvido para a Global Solution 2026 — FIAP. Dados fornecidos pela [NASA Open APIs](https://api.nasa.gov).
