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


def hospitalizations():
    st.header('Ocupación hospitalaria')
    data = load_data()
    if data is None:
        st.stop()
    occupation_by_region(data)


def deaths():
    st.header('Muertes confirmadas')
    data = load_deaths_data()
    if data is None:
        st.stop()
    chart_data = data.groupby('fecha')['num_def'].sum().asfreq('D').rename('Muertes')
    st.line_chart(chart_data)
    st.write(chart_data)


def load_deaths_data():
    data_src = st.radio('Data source', options=('URL', 'Local file'), index=1)
    if data_src == 'URL':
        return load_deaths_from_url()
    elif data_src == 'Local file':
        return load_deaths_from_file()


def load_deaths_from_url():
    default_url = 'https://cnecovid.isciii.es/covid19/resources/casos_hosp_uci_def_sexo_edad_provres.csv'
    url = st.text_input('Data URL')
    default_url
    return parse_deaths_data(url)


def load_deaths_from_file():
    file = st.file_uploader('Data file', type='csv')
    return parse_deaths_data(file)


@st.cache
def parse_deaths_data(io):
    if not io:
        return None
    data = pd.read_csv(io, sep=',', encoding='latin')
    data['fecha'] = pd.to_datetime(data['fecha'], format='%Y-%m-%d')
    return data
    

def set_task(task):
    st.session_state.task = task


def run_task():
    st.session_state.task()


st.session_state.setdefault('task', lambda: None)
st.title('COVID-19')

col1, col2 = st.columns(2)
col1.button('Capacidad asistencial', on_click=set_task, args=(hospitalizations,))
col2.button('Deaths', on_click=set_task, args=(deaths,))
run_task()
