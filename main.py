import locale
import pandas as pd
import streamlit as st

# Definir a localização como português do Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Função para calcular a soma do Saldo Cobrado e formatar como valor de moeda em Real do Brasil
def calcular_saldo_cobrado(filtro_atraso=None, data_inicio=None, data_fim=None):
    # Leia a planilha específica "analitico_2"
    planilha = pd.read_excel("analise_consolidada_compesa.xlsx", sheet_name="analitico_2")

    # Aplicar filtro de atraso se fornecido
    if filtro_atraso:
        planilha = planilha[planilha["ATRASO"].isin(filtro_atraso)]

    # Aplicar filtro de data se fornecido
    if data_inicio and data_fim:
        planilha = planilha[(planilha["mês"] >= data_inicio) & (planilha["mês"] <= data_fim)]

    # Somar a coluna "Saldo Cobrado"
    soma_saldo_cobrado = planilha["Saldo Cobrado"].sum()

    # Verificar se o valor está na faixa dos milhões
    if soma_saldo_cobrado >= 1_000_000:
        # Formatar a soma como valor de moeda em Real do Brasil
        soma_saldo_cobrado_formatada = locale.currency(soma_saldo_cobrado / 1_000_000, grouping=True, symbol=True, international=False)
        # Adicionar a palavra "milhões" ao final da string
        soma_saldo_cobrado_formatada += " Milhões"
    else:
        # Formatar a soma como valor de moeda em Real do Brasil
        soma_saldo_cobrado_formatada = locale.currency(soma_saldo_cobrado, grouping=True, symbol=True, international=False)
    
    return soma_saldo_cobrado_formatada

# Função para calcular a soma do Débito Pago e formatar como valor de moeda em Real do Brasil
def calcular_debito_pago(filtro_atraso=None, data_inicio=None, data_fim=None):
    # Leia a planilha específica "analitico_2"
    planilha = pd.read_excel("analise_consolidada_compesa.xlsx", sheet_name="analitico_2")

    # Aplicar filtro de atraso se fornecido
    if filtro_atraso:
        planilha = planilha[planilha["ATRASO"].isin(filtro_atraso)]

    # Aplicar filtro de data se fornecido
    if data_inicio and data_fim:
        planilha = planilha[(planilha["mês"] >= data_inicio) & (planilha["mês"] <= data_fim)]

    # Somar a coluna "Remuneração À Vista"
    soma_debito_pago = planilha["DEBITO PAGO"].sum()

    # Verificar se o valor está na faixa dos milhões
    if soma_debito_pago >= 1_000_000:
        # Formatar a soma como valor de moeda em Real do Brasil
        soma_remuneracao_avista_formatada = locale.currency(soma_debito_pago / 1_000_000, grouping=True, symbol=True, international=False)
        # Adicionar a palavra "milhões" ao final da string
        soma_remuneracao_avista_formatada += " Milhões"
    else:
        # Formatar a soma como valor de moeda em Real do Brasil
        soma_remuneracao_avista_formatada = locale.currency(soma_debito_pago, grouping=True, symbol=True, international=False)
    
    return soma_remuneracao_avista_formatada

# Função para calcular a soma do Débito Parcelado e formatar como valor de moeda em Real do Brasil
def calcular_debito_parcelado(filtro_atraso=None, data_inicio=None, data_fim=None):
    # Leia a planilha específica "analitico_2"
    planilha = pd.read_excel("analise_consolidada_compesa.xlsx", sheet_name="analitico_2")

    # Aplicar filtro de atraso se fornecido
    if filtro_atraso:
        planilha = planilha[planilha["ATRASO"].isin(filtro_atraso)]

    # Aplicar filtro de data se fornecido
    if data_inicio and data_fim:
        planilha = planilha[(planilha["mês"] >= data_inicio) & (planilha["mês"] <= data_fim)]

    # Somar a coluna "Remuneração À Vista"
    soma_debito_parcelado = planilha["DEBITO PARCELADO"].sum()

    # Verificar se o valor está na faixa dos milhões
    if soma_debito_parcelado >= 1_000_000:
        # Formatar a soma como valor de moeda em Real do Brasil
        soma_debito_parcelado_formatada = locale.currency(soma_debito_parcelado / 1_000_000, grouping=True, symbol=True, international=False)
        # Adicionar a palavra "milhões" ao final da string
        soma_debito_parcelado_formatada += " Milhões"
    else:
        # Formatar a soma como valor de moeda em Real do Brasil
        soma_debito_parcelado_formatada = locale.currency(soma_debito_parcelado, grouping=True, symbol=True, international=False)
    
    return soma_debito_parcelado_formatada

# Título do aplicativo Streamlit
st.title('Análise COMPESA')

# Ler os dados e obter valores únicos da coluna "ATRASO"
planilha = pd.read_excel("analise_consolidada_compesa.xlsx", sheet_name="analitico_2")
valores_atraso = planilha["ATRASO"].unique()

st.sidebar.image("logo_portes.png")

# Adicionar menu lateral para filtro de atraso
filtro_atraso = st.sidebar.multiselect("Filtrar por Atraso:", list(valores_atraso), default=list(valores_atraso))

# Obter datas disponíveis no arquivo
datas_disponiveis = pd.date_range(planilha["mês"].min(), planilha["mês"].max()).strftime("%Y-%m-%d").tolist()

# Adicionar filtro de data
data_inicio, data_fim = st.sidebar.select_slider("Filtrar por Data:", options=datas_disponiveis, value=(datas_disponiveis[0], datas_disponiveis[-1]))

# Calcular e exibir o KPI "Cobrado" com base no filtro selecionado
cobrado_valor = calcular_saldo_cobrado(filtro_atraso=filtro_atraso, data_inicio=data_inicio, data_fim=data_fim)

# Calcular e exibir o KPI "À Vista"
debito_pago_valor = calcular_debito_pago(filtro_atraso=filtro_atraso, data_inicio=data_inicio, data_fim=data_fim)

# Calcular e exibir o KPI "DEBITO PARCELADO"
debito_parcelado_valor = calcular_debito_parcelado(filtro_atraso=filtro_atraso, data_inicio=data_inicio, data_fim=data_fim)

# Dividir a tela em três colunas
col1, col2, col3 = st.columns(3)

# KPI "Cobrado"
with col1:
    st.subheader('Cobrado')
    # Aplicar estilo CSS para o contêiner do KPI com tamanho de fonte menor
    st.write(
        f'<div style="background-color:#172D43; padding: 20px; border-radius: 10px;">'
        f'<span style="color:white; font-size: 20px;">{cobrado_valor}</span>'
        '</div>',
        unsafe_allow_html=True
    )

# KPI "À Vista"
with col2:
    st.subheader('À Vista')
    # Aplicar estilo CSS para o contêiner do KPI com tamanho de fonte menor
    st.write(
        f'<div style="background-color:#172D43; padding: 20px; border-radius: 10px;">'
        f'<span style="color:white; font-size: 20px;">{debito_pago_valor}</span>'
        '</div>',
        unsafe_allow_html=True
    )

# KPI "DEBITO PARCELADO"
with col3:
    st.subheader('Débito Parcelado')
    # Aplicar estilo CSS para o contêiner do KPI com tamanho de fonte menor
    st.write(
        f'<div style="background-color:#172D43; padding: 20px; border-radius: 10px;">'
        f'<span style="color:white; font-size: 20px;">{debito_parcelado_valor}</span>'
        '</div>',
        unsafe_allow_html=True
    )
