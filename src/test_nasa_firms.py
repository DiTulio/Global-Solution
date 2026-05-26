# import requests

# API_KEY = "z9qtFmVtl57soBw9Bsx1sKyfzAgKKlqfxtGvmFqS"

# url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{API_KEY}/VIIRS_SNPP_NRT/BRA/1"

# response = requests.get(url)

# if response.status_code == 200:
#     print("Dados recebidos com sucesso!")
#     print(response.text[:500])  
# else:
#     print(f"Erro: {response.status_code}")
#     print(response.text)

import requests

API_KEY = "z9qtFmVtl57soBw9Bsx1sKyfzAgKKlqfxtGvmFqS"

url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"

response = requests.get(url)

if response.status_code == 200:
    dados = response.json()
    print("Conexão com a NASA funcionando!")
    print(f"Título: {dados['title']}")
    print(f"Data: {dados['date']}")
    print(f"Explicação: {dados['explanation'][:300]}")
else:
    print(f"Erro: {response.status_code}")
    print(response.text)