import requests
import webbrowser
import os

API_KEY = "z9qtFmVtl57soBw9Bsx1sKyfzAgKKlqfxtGvmFqS"

url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"

response = requests.get(url)

if response.status_code == 200:
    dados = response.json()

    titulo = dados['title']
    data = dados['date']
    explicacao = dados['explanation']
    imagem_url = dados['url']

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>NASA - Imagem do Dia</title>
        <style>
            body {{
                background-color: #0a0a0a;
                color: white;
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 40px 20px;
            }}
            h1 {{ color: #4fc3f7; }}
            img {{
                width: 100%;
                border-radius: 12px;
                margin: 20px 0;
            }}
            p {{ line-height: 1.7; color: #cccccc; }}
            span {{ color: #888; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <h1>{titulo}</h1>
        <span>{data}</span>
        <img src="{imagem_url}" alt="{titulo}">
        <p>{explicacao}</p>
    </body>
    </html>
    """

    caminho = r"C:\gs-test\apod.html"
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)

    print("HTML gerado com sucesso!")
    webbrowser.open(f"file:///{caminho}")

else:
    print(f"Erro: {response.status_code}")
    print(response.text)