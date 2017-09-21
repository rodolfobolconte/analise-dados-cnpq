from pylab import *
from pandas import *

labels = ['regiao', 'estado', 'area', 'quantidade']

arquivo = read_csv('2006.csv',
                   delimiter=';',
                   encoding='iso-8859-1',
                   skiprows=1,
                   usecols=[2, 3, 8, 9],
                   names=labels)

arquivo.drop_duplicates()

def porcentagem(df):
    total = df.sum()
    porcentagem = df * 100 / total

    return porcentagem

bolsas_por_estado = arquivo.groupby(['regiao', 'estado']).sum().sort_values(['quantidade'])
bolsas_por_regiao = bolsas_por_estado.groupby(['regiao']).sum().sort_values(['quantidade'])

porcentagem_bolsas_por_estado = porcentagem(bolsas_por_estado)
porcentagem_bolsas_por_regiao = porcentagem(bolsas_por_regiao)

#print(bolsas_por_estado)
#print(bolsas_por_regiao)

#print(porcentagem_bolsas_por_estado)
#print(porcentagem_bolsas_por_regiao)

#bar(range(len(regioes)), regioes) ; xticks(range(len(regioes)), regioes.index)


def maior_menor(df):
    estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

    maiores_areas_por_estado = list()

    for estado in estados:
        estado_aux = df[df['estado']==estado]
        estado_aux = estado_aux.groupby(['estado', 'area']).sum().sort_values('quantidade', ascending=False).head(3)

        maiores_areas_por_estado.append(estado_aux)

    print(maiores_areas_por_estado)

bolsas_por_area = arquivo.groupby(['estado', 'area']).sum().sort_values(['quantidade'])

maior_menor(arquivo)

#print(arquivo.max())
#print()
#print(arquivo[arquivo['regiao']=='Sul'].max())