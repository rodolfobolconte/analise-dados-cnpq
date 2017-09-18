#########################################################################################################
# Projeto de Análise das Bolsas e dos Investimentos do CNPq de 2006 a 2015
# Autor: Rodolfo Bolconte Donato
#
# Site dos dados: http://cnpq.br/dados_abertos/
#
# 3 análises estão no seguinte projeto:
#   1- Média da Quantidade de Bolsas por Região no País;
#   2- Quantidade Média de Bolsas nos Governos de Lula e Dilma;
#   3- Linha do Tempo Média da Quantidade de Bolsas por Região e o Orçamento Total por Região das Bolsas.
#########################################################################################################

from pylab import *
from pandas import *
from numpy import *


#dicionarios para armazenar os DataFrames dos dois tipos de dados
quantidade_bolsas = {}
orcamento_bolsas = {}


#nome das colunas dos respectivos DataFrames
labels_quantidade_bolsas = ['regiao', 'estado', 'area', 'quantidade']
labels_orcamento_bolsas = ['regiao', 'estado', 'area', 'total']


#lendo os arquivos .csv de 2006 a 2015 dos dois tipos de dados e colocando cada ano dentro de seu respectivo dicionario
for i in range(2006, 2016):
    quantidade_bolsas[str(i)] = read_csv('bolsa-pais/'+str(i)+'.csv', delimiter=';', encoding='iso-8859-1', skiprows=1, usecols=[2, 3, 8, 9], names=labels_quantidade_bolsas)
    orcamento_bolsas[str(i)] = read_csv('projeto-pesquisa/'+str(i)+'.csv', delimiter=';', encoding='iso-8859-1', skiprows=1, usecols=[2, 3, 8, 12], names=labels_orcamento_bolsas)


#dicionarios com os dados separados somente por regiao
quantidade_bolsas_por_regiao = {}
orcamento_bolsas_por_regiao = {}


#obtém somente a quantidade(i) e o valor(ii) dos DataFrames separados por região
for i in range(2006, 2016):
    quantidade_bolsas_por_regiao[str(i)] = quantidade_bolsas[str(i)].groupby(['regiao']).sum()
    orcamento_bolsas_por_regiao[str(i)] = orcamento_bolsas[str(i)].groupby(['regiao']).sum()



#Gráfico da Média da Quantidade de Bolsas Dividido por Região
def grafico_media_quantidade_bolsas_por_regiao(index, media_bolsas, eixos, colors):

    x = range(len(media_bolsas))
    barras = eixos[0].bar(x, media_bolsas.media, tick_label=index, color=colors, width=0.5)
    eixos[0].set_title('Média de Bolsas do CNPq (2006-2015)')

    for i in barras:
        height = i.get_height()
        eixos[0].text(i.get_x() + i.get_width() / 2, 1.01 * height, '%.1f' % height, fontsize=8, ha='center',
                      va='bottom')

#Gráfico da Porcentagem da Média de Bolsas Dividido por Região
def grafico_porcentagem_media_quantidade_bolsas_por_regiao(index, media_bolsas, eixos, colors):
    eixos[1].pie(media_bolsas, labels=index, autopct='%1.1f%%', colors=colors)
    eixos[1].set_title('Porcentagem da Média de Bolsas do CNPq (2006-2015)')

#Gráficos com a Média e Porcentagem Total Divididos por Região
def grafico_media_total_por_regioes(bolsas_por_regiao):
    bolsas_por_regiao_geral = concat(bolsas_por_regiao, axis=1, join='inner')

    index = bolsas_por_regiao_geral.index

    media_bolsas = DataFrame(index=index, columns=['media'])

    for i in range(len(bolsas_por_regiao_geral)):
        media_bolsas.loc[index[i]] = [bolsas_por_regiao_geral.ix[i].mean()]

    fig, eixos = plt.subplots(nrows=1, ncols=2, figsize=(80, 7))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    grafico_porcentagem_media_quantidade_bolsas_por_regiao(index, media_bolsas, eixos, colors)
    grafico_media_quantidade_bolsas_por_regiao(index, media_bolsas, eixos, colors)

    subplots_adjust(wspace=0.2)

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()

    show()



#Gráfico da Quantidade Média de Bolsas no Governo Lula
def grafico_governo_lula_quantidade_bolsas_por_regiao(quantidade_bolsas_por_regiao_geral, eixos):
    index = quantidade_bolsas_por_regiao_geral.ix[0].index

    x = linspace(1, 6, 5)
    r1 = eixos[0].barh(x + 0.4, quantidade_bolsas_por_regiao_geral.ix[0][:'2010'], height=0.2)
    eixos[0].set_title('Número de Bolsas do CNPq no Governo Lula\n(2006-2010)')

    r2 = eixos[0].barh(x + 0.2, quantidade_bolsas_por_regiao_geral.ix[1][:'2010'], height=0.2)

    r3 = eixos[0].barh(x, quantidade_bolsas_por_regiao_geral.ix[2][:'2010'], height=0.2, tick_label=index.levels[0][:5])

    r4 = eixos[0].barh(x - 0.2, quantidade_bolsas_por_regiao_geral.ix[3][:'2010'], height=0.2)

    r5 = eixos[0].barh(x - 0.4, quantidade_bolsas_por_regiao_geral.ix[4][:'2010'], height=0.2)

    subplots_adjust(wspace=0.5)

    eixos[0].legend((r1[0], r2[0], r3[0], r4[0], r5[0]), ('Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul'), loc=4)

#Gráfico da Quantidade Média de Bolsas no Governo Dilma
def grafico_governo_dilma_quantidade_bolsas_por_regiao(quantidade_bolsas_por_regiao_geral, eixos):
    index = quantidade_bolsas_por_regiao_geral.ix[0].index

    x = linspace(1, 6, 5)
    r1 = eixos[1].barh(x + 0.4, quantidade_bolsas_por_regiao_geral.ix[0]['2011':], height=0.2)
    eixos[1].set_title('Número de Bolsas do CNPq no Governo Dilma\n(2011-2015)')

    r2 = eixos[1].barh(x + 0.2, quantidade_bolsas_por_regiao_geral.ix[1]['2011':], height=0.2)

    r3 = eixos[1].barh(x, quantidade_bolsas_por_regiao_geral.ix[2]['2011':], height=0.2, tick_label=index.levels[0][5:])

    r4 = eixos[1].barh(x - 0.2, quantidade_bolsas_por_regiao_geral.ix[3]['2011':], height=0.2)

    r5 = eixos[1].barh(x - 0.4, quantidade_bolsas_por_regiao_geral.ix[4]['2011':], height=0.2)

    subplots_adjust(wspace=0.5)

    eixos[1].legend((r1[0], r2[0], r3[0], r4[0], r5[0]), ('Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul'), loc=4)

#Gráfico da Quantidade Média de Bolsas nos Governos Lula e Dilma Separados por Região
def grafico_quantidade_bolsas_por_governo(quantidade_bolsas):
    quantidade_bolsas_por_regiao_geral = concat(quantidade_bolsas, axis=1, join='inner')

    fig, eixos = plt.subplots(nrows=1, ncols=2)

    grafico_governo_lula_quantidade_bolsas_por_regiao(quantidade_bolsas_por_regiao_geral, eixos)
    grafico_governo_dilma_quantidade_bolsas_por_regiao(quantidade_bolsas_por_regiao_geral, eixos)

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()

    subplots_adjust(wspace=0.5)

    show()



#Gráfico no Formato Linha do Tempo da Quantidade de Bolsas por Região
def grafico_linha_do_tempo_quantidade_bolsas_por_regiao(quantidade_bolsas_por_regiao_geral, eixos):
    x = arange(2006, 2016, 1)

    for i in range(len(quantidade_bolsas_por_regiao_geral)):
        eixos[0].plot(x, quantidade_bolsas_por_regiao_geral.ix[i], 'o')

    eixos[0].legend(('Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul'), loc=2)

    eixos[0].plot(x, quantidade_bolsas_por_regiao_geral.ix[0], 'k--', color='#1f77b4')
    eixos[0].plot(x, quantidade_bolsas_por_regiao_geral.ix[1], 'k--', color='#ff7f0e')
    eixos[0].plot(x, quantidade_bolsas_por_regiao_geral.ix[2], 'k--', color='#2ca02c')
    eixos[0].plot(x, quantidade_bolsas_por_regiao_geral.ix[3], 'k--', color='#d62728')
    eixos[0].plot(x, quantidade_bolsas_por_regiao_geral.ix[4], 'k--', color='#9467bd')

    eixos[0].grid(True)
    eixos[0].set_title("Quantidade de Bolsas do CNPq por Ano (2006-2015)")

#Gráfico no Formato Linha do Tempo do Orçamento Médio Anual Feito pelo CNPq por Região
def grafico_linha_do_tempo_orcamento_bolsas_por_regiao(orcamento_bolsas_por_regiao_geral, eixos):
    x = arange(2006, 2016, 1)

    for i in range(len(orcamento_bolsas_por_regiao_geral)):
        eixos[1].plot(x, orcamento_bolsas_por_regiao_geral.ix[i], 'o')

    eixos[1].legend(('Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul'), loc=9)

    eixos[1].plot(x, orcamento_bolsas_por_regiao_geral.ix[0], 'k--', color='#1f77b4')
    eixos[1].plot(x, orcamento_bolsas_por_regiao_geral.ix[1], 'k--', color='#ff7f0e')
    eixos[1].plot(x, orcamento_bolsas_por_regiao_geral.ix[2], 'k--', color='#2ca02c')
    eixos[1].plot(x, orcamento_bolsas_por_regiao_geral.ix[3], 'k--', color='#d62728')
    eixos[1].plot(x, orcamento_bolsas_por_regiao_geral.ix[4], 'k--', color='#9467bd')

    eixos[1].grid(True)
    eixos[1].set_title("Investimento em Bolsas do CNPq\npor Ano em Bilhões de R$ (2006-2015)")

#Gráficos no Formato Linha do Tempo da Quantidade de Bolsas por Região e do Orçamento Médio Anual Categorizados por Região
def grafico_orcamento_bolsas_por_regiao(quantidade_bolsas, orcamento_bolsas):
    quantidade_bolsas_por_regiao_geral = concat(quantidade_bolsas, axis=1, join='inner')
    orcamento_bolsas_por_regiao_geral = concat(orcamento_bolsas, axis=1, join='inner')

    fig, eixos = plt.subplots(nrows=1, ncols=2)

    grafico_linha_do_tempo_quantidade_bolsas_por_regiao(quantidade_bolsas_por_regiao_geral, eixos)
    grafico_linha_do_tempo_orcamento_bolsas_por_regiao(orcamento_bolsas_por_regiao_geral, eixos)

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()

    subplots_adjust(wspace=0.5)

    show()


grafico_media_total_por_regioes(quantidade_bolsas_por_regiao)
grafico_quantidade_bolsas_por_governo(quantidade_bolsas_por_regiao)
grafico_orcamento_bolsas_por_regiao(quantidade_bolsas_por_regiao, orcamento_bolsas_por_regiao)