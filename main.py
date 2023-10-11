import matplotlib.pyplot as plt
import pandas as pd
import re

# Ler csv e criar df
df = pd.read_csv('starbucks_drinkMenu_expanded.csv')

# Substituindo o "NAN" da coluna "Caffeine" por valor referencia da categoria do drink
df['Caffeine (mg)'].fillna('90', inplace=True)

# Removendo o espaço no inicio/final das colunas
df.rename(columns=lambda x: x.strip(), inplace=True)

# Remover caracteres especiais das linhas da coluna 'Beverage_category'
df['Beverage_category'] = df['Beverage_category'].apply(
    lambda x: re.sub(r'\W+', '', x))

# Remover itens que possuem 'varies' e 'Varies' na coluna Caffeine

df.drop(df[df['Caffeine (mg)'].isin(['varies', 'Varies'])].index, inplace=True)

# Converter coluna 'Caffeine' para int
df['Caffeine (mg)'] = df['Caffeine (mg)'].astype(int)

# Criar uma coluna que represente, em porcentagem, a quantidade de cafeína presente em cada bebida, levando em consideração o consumo máximo recomendado pela FDA(400mg)

df['Caffeine (% DV)'] = df['Caffeine (mg)'] / 400 * 100

# Criar uma coluna que represente, em porcentagem, a quantidade de açucar presente em cada bebida, levando em consideração o consumo máximo recomendado pela FDA(50g)

df['Sugar (% DV)'] = df['Sugars (g)'] / 50 * 100

# Filtrar as linhas com Sugar (% DV) > 100 * Alto indice de açucar *

df[df['Sugar (% DV)'] > 100]

# Quais categorias de bebidas possuem opções "Sugar-free"? * Considerando Daily Value
print(f'Minimo de cada categoria, identificar as opções sem açucar: \n')

print(df.groupby('Beverage_category')['Sugar (% DV)'].min(), '\n')

# Quais categorias de bebidas em média possuem mais açucar? * Considerando Daily Value
print(f'Média de açucar em cada categoria: \n')
print(df.groupby('Beverage_category')['Sugar (% DV)'].mean(), '\n')

# Observa quantos % dos itens da categoria "FrappuccinoBlendedCoffee" estão acima da recomendação diaria de ingestão de açucar

print(
    f'60% dos drinks da categoria FrappuccinoBlendedCoffee estão acima da recomendação diaria de ingestão de açucar \n'
)

print(
    df['Sugar (% DV)'][df['Beverage_category'] ==
                       'FrappuccinoBlendedCoffee'].quantile(0.40), '\n')

# Quais categorias de bebidas possuem opções 'Sem cafeina'?

print(
    f'Minimo de cada categoria, identificar as categorias com opções sem cafeina: \n'
)
print(df.groupby('Beverage_category')['Caffeine (mg)'].min(), '\n')

# Salvar DF com colunas adicionais, formato "csv"

df.to_csv(path_or_buf='drinkmenu_v2')

# pd.cut para dividir os valores em categorias ('sem cafeína', 'pouca', 'média', 'muita', 'muita+')

# Definir os limites dos intervalos
limits = [-float('inf'), 0, 20, 60, 90, float('inf')]

# Definir as categorias
categories = ['sem cafeína', 'pouca', 'média', 'muita', 'muita+']

# Criar os intervalos e atribuir as categorias
intervalo_caffeine = pd.cut(df['Caffeine (% DV)'],
                            bins=limits,
                            labels=categories)
print(f'Intervalo:\n')
print(intervalo_caffeine, '\n')
print(f'Contagem de categorias:\n')
print(intervalo_caffeine.value_counts(), '\n')

# Grafico da média de açucar para cada categoria de bebida
# Finalidade verificar quais categorias possuem o maior indice de açucar considerando o valor diario recomendado(FDA)

# Agrupar os dados pela coluna 'Beverage_category' e calcular a média da coluna 'Sugar (% DV)'
dados = df.groupby('Beverage_category')['Sugar (% DV)'].mean().sort_values(
    ascending=True)

# Criar o gráfico de barras
plt.barh(dados.index, dados.values, color='red')

# Adicionar rótulos aos eixos
plt.xlabel('Açúcar (% DV)')
plt.ylabel('Categoria de Bebida')

# Adicionar título ao gráfico
plt.title('Média de Açúcar por Categoria de Bebida')

# Exibir o gráfico
plt.show()
