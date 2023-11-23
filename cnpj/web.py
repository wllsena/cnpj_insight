import pandas as pd
import streamlit as st
# from geopy.geocoders import Nominatim

# geolocator = Nominatim(user_agent="geolocalização")

# Define dataset column names
columns = ['cnpj_basico', 'cnpj_ordem', 'cnpj_dv', 'matriz_filial', 'nome_fantasia', 'situacao_cadastral',
           'data_situacao_cadastral', 'motivo_situacao_cadastral', 'nome_cidade_exterior', 'pais', 'data_inicio_atividade',
           'cnae_fiscal_principal', 'cnae_fiscal_sec', 'tipo_logradouro', 'logradouro', 'numero', 'complemento', 'bairro',
           'cep', 'uf', 'municipio', 'ddd_1', 'telefone_1', 'ddd_2', 'telefone_2', 'ddd_fax', 'fax', 'email']

# Load dataset
data = pd.read_excel(r'dados/estabelecimentos_9.xlsx', names=columns)

# Convert data_situacao_cadastral and data_inicio_atividade to datetime
data['data_situacao_cadastral'] = pd.to_datetime(data['data_situacao_cadastral'], format='%Y%m%d')
data['data_inicio_atividade'] = pd.to_datetime(data['data_inicio_atividade'], format='%Y%m%d')

# map logradouro, municipio, numero and uf to string
data['numero'] = data['numero'].astype(str)
data['logradouro'] = data['logradouro'].astype(str)
data['municipio'] = data['municipio'].astype(str)
data['tipo_logradouro'] = data['tipo_logradouro'].astype(str)
data['uf'] = data['uf'].astype(str)

# Page setup
st.set_page_config(page_title="CorpScan", layout="wide")
st.title("CorpScan - O Procurador de empresas")

# Show the entire dataset as a table
st.write("Tabela completa dos estabelecimentos:")

# Display data
st.write(data)

# Dropdown menu for selecting the search column
search_column = st.selectbox("Escolha a coluna para a busca:", columns)

# Search functionality
search_term = st.text_input("Digite o valor de busca:")

filtered_data = None

if search_term:
    # Use regex to match all words in any order for the selected column
    pattern = r'(?i)' + r'.*'.join(search_term.lower().split())
    filtered_data = data[data[search_column].astype(str).str.contains(pattern)]

    # Display the search results
    if not filtered_data.empty:
        st.write("Resultado da busca:")
        st.write(filtered_data)
    else:
        st.write("Nenhum resultado encontrado.")

if filtered_data is not None:
    # Bar chart for the number of establishments in each year
    st.subheader("Número de estabelecimentos abertos por ano (pela busca):")
    st.bar_chart(data.groupby(filtered_data['data_inicio_atividade'].dt.year)['cnpj_basico'].count())
else:
    # Bar chart for the number of establishments in each year
    st.subheader("Número de estabelecimentos abertos por ano (Total):")
    st.bar_chart(data.groupby(data['data_inicio_atividade'].dt.year)['cnpj_basico'].count())

# location = geolocator.geocode(data['tipo_logradouro'][3] + ' ' + data['logradouro'][3] + ', ' + data['numero'][3] + '-' + data['bairro'][3] + ', ' + data['uf'][3])

# lat = location.latitude
# lon = location.longitude

# # Display leaflet map with the search results
# st.write("Mapa de resultados:")
# st.map((lat, lon), zoom=15)
