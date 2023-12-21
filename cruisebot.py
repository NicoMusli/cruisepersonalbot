import requests
import openpyxl
import pandas as pd
from bs4 import BeautifulSoup

prezzolista = []
imbarco = []
sbarco = []
partenza = []
rientro = []
notti = []
nave = []

for i in range(1, 100):
    URL = f'https://www.fersinaviaggi.it/crociere-mobile/z_mediterraneo/m_febbraio_2024/g_{i}'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all(id="specifica")
    number = 0
    for crociera in results:
        prezzo = crociera.find(id=f'Repeater1_prezzoi_{number}').string.replace(".","")
        try:      
            prezzo=float(prezzo)
            if (prezzo<400):
                imbarco.append(crociera.find(id=f'Repeater1_imbarco_{number}').string)
                sbarco.append(crociera.find(id=f'Repeater1_sbarco_{number}').string)
                partenza.append(crociera.find(id=f'Repeater1_dal_{number}').string)
                rientro.append(crociera.find(id=f'Repeater1_al_{number}').string)
                notti.append(crociera.find(id=f'Repeater1_Label6_{number}').string)
                nave.append(soup.find(id=f'Repeater1_HyperNave_{number}').string)
                prezzolista.append(prezzo)
        except ValueError:
            number += 1
            continue
        number += 1

data = {
    'Nave': nave,
    'Prezzo': prezzolista,
    'Imbarco': imbarco,
    'Sbarco': sbarco,
    'Notti': notti,
    'Partenza': partenza,
    'Rientro': rientro
}
df = pd.DataFrame(data)
nome_file = 'dati.xlsx'
df.to_excel(nome_file, index=False)