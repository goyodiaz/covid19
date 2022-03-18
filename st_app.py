import streamlit as st
import pandas as pd
import numpy as np


@st.cache
def load_data():
    DATA_URL = 'https://www.sanidad.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Datos_Capacidad_Asistencial_Historico_18032022.csv'
    data = pd.read_csv(DATA_URL, sep=';', encoding='latin')
    data['Fecha'] = pd.to_datetime(data['Fecha'], format='%d/%m/%Y')
    return data


@st.cache
def get_regions(data):
    col_name = 'CCAA'
    values = data[col_name].unique()
    values.sort()
    return values


@st.cache
def get_units(data):
    col_name = 'Unidad'
    values = data[col_name].unique()
    values.sort()
    return values


def altair_chart(chart_data):
    st.line_chart(chart_data)


st.title('Capacidad asistencial')
data = load_data()

st.subheader('Datos')
st.write(data)

left, right = st.columns(2)
ca = left.selectbox('Comunidad', get_regions(data))
unit = right.selectbox('Unidad', get_units(data))

chart_data = data.query(f'CCAA == \'{ca}\' & Unidad == \'{unit}\'').groupby('Fecha')['OCUPADAS_COVID19'].sum()
altair_chart(chart_data)
