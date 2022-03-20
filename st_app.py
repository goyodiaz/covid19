import streamlit as st
import pandas as pd


def load_data():
    data_src = st.radio('Data source', options=('URL', 'Local file'), index=1)
    if data_src == 'URL':
        return load_from_url()
    elif data_src == 'Local file':
        return load_from_file()


def load_from_url():
    default_url = 'https://www.sanidad.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Datos_Capacidad_Asistencial_Historico_18032022.csv'
    url = st.text_input('Data URL')
    default_url
    return parse_data(url)


def load_from_file():
    file = st.file_uploader('Data file', type='csv')
    return parse_data(file)


@st.cache
def parse_data(io):
    if not io:
        return None
    data = pd.read_csv(io, sep=';', encoding='latin')
    data['Fecha'] = pd.to_datetime(data['Fecha'], format='%d/%m/%Y')
    return data


@st.cache
def get_regions(data):
    return get_unique_values(data, col_name='CCAA')


# ~ @st.cache
def get_units(data):
    return get_unique_values(data, col_name='Unidad')


def get_unique_values(data, col_name):
    values = data[col_name].unique()
    values.sort()
    return values


def altair_chart(chart_data):
    st.line_chart(chart_data)


def occupation_by_region(data):
    ca = st.selectbox('Comunidad', get_regions(data), key=0)
    chart_data = data.query(f'CCAA == \'{ca}\'').groupby(['Fecha', 'Unidad'])['OCUPADAS_COVID19'].sum().unstack(level='Unidad')
    st.area_chart(chart_data.rename_axis(columns=None))
    st.write(chart_data.assign(**{'Total ocupadas COVID-19': chart_data.sum(axis='columns')}))


st.title('Capacidad asistencial')
st.write('Ocupación de camas hospitalarias por COVID-19')
data = load_data()
if data is None:
    st.stop()
occupation_by_region(data)
