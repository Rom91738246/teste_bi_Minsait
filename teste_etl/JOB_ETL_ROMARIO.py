import pandas as pd
from datetime import datetime

# Definir os caminhos dos arquivos
caminho_origem = 'C:/ETL/origem.csv'
caminho_municipios = 'C:/ETL/d_municipio.csv'
caminho_tempo = 'C:/ETL/d_tempo.csv'
caminho_saida = 'C:/ETL/saida.csv'

# Carregar os dados
df = pd.read_csv(caminho_origem)

# Listar as colunas do DataFrame para verificar os nomes
print("Colunas do DataFrame:", df.columns)

# Filtrar os dados conforme os critérios
df_filtered = df[
    (df['tp_entrada'].isin([1, 4, 6])) &
    (df['tp_forma'].isin([1, 3])) &
    (df['tp_situacao_encerramento'] != 6) &
    (pd.to_datetime(df['dt_diagnostico_sintoma']) >= '2021-01-01')
]

# Verificar se há dados após a filtragem
print("Dados filtrados:", df_filtered.shape)
print(df_filtered.head())

# Carregar a tabela de municípios e filtrar apenas os municípios de Goiás
municipios = pd.read_csv(caminho_municipios)
municipios_goias = municipios[municipios['dmun_uf_nome'] == 'Goiás']

# Converter o código do município para o nome completo
df_filtered = df_filtered.merge(municipios_goias[['dmun_codibge', 'dmun_municipio']], left_on='co_municipio_residencia_atual', right_on='dmun_codibge')

# Verificar a junção e o filtro de estado
print("Dados após junção e filtro de estado:", df_filtered.shape)
print(df_filtered.head())

# Converter a data de diagnóstico para o formato "<Mês> de <Ano>"
df_filtered['Mês'] = pd.to_datetime(df_filtered['dt_diagnostico_sintoma']).dt.strftime('%B de %Y')

# Carregar a tabela de dimensões de tempo
tempo = pd.read_csv(caminho_tempo)

# Garantir que todos os períodos estejam presentes
all_municipios = municipios_goias['dmun_municipio'].unique()
all_months = pd.date_range(start='2021-01-01', end=datetime.now(), freq='MS').strftime('%B de %Y')

df_complete = pd.MultiIndex.from_product([all_municipios, all_months], names=['município', 'mês']).to_frame(index=False)
df_aggregated = df_filtered.groupby(['dmun_municipio', 'Mês']).size().reset_index(name='Quantidade')

# Renomear colunas para o formato final
df_aggregated.rename(columns={'dmun_municipio': 'município', 'Mês': 'mês'}, inplace=True)

# Verificar o agrupamento e contagem
print("Dados agregados:", df_aggregated.head())

df_final = df_complete.merge(df_aggregated, on=['município', 'mês'], how='left').fillna(0)

# Verificar o DataFrame final
print("Dados finais:", df_final.head())

# Salvar o resultado
df_final.to_csv(caminho_saida, index=False)
