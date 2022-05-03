import pandas as pd
import streamlit as st

import hospitals


def altair_chart(chart_data):
    st.line_chart(chart_data)


def cases_deaths():
    st.header("Casos y muertes")
    data = load_cases_deaths_data()
    if data is None:
        st.stop()
    variable = st.radio("Variable", options=("Cases", "Deaths"), index=1)
    if variable == "Cases":
        cases(data=data)
    elif variable == "Deaths":
        deaths(data=data)
    else:
        raise ValueError(variable)


def cases(data):
    chart_data = data.groupby("fecha")["num_casos"].sum().asfreq("D").rename("Casos")
    st.line_chart(chart_data)
    st.write(chart_data)


def deaths(data):
    chart_data = data.groupby("fecha")["num_def"].sum().asfreq("D").rename("Muertes")
    st.line_chart(chart_data)
    st.write(chart_data)


def load_cases_deaths_data():
    data_src = st.radio("Data source", options=("URL", "Local file"), index=1)
    if data_src == "URL":
        return load_cases_deaths_from_url()
    elif data_src == "Local file":
        return load_cases_deaths_from_file()


def load_cases_deaths_from_url():
    default_url = "https://cnecovid.isciii.es/covid19/resources/casos_hosp_uci_def_sexo_edad_provres.csv"
    url = st.text_input("Data URL")
    default_url
    return parse_cases_deaths_data(url)


def load_cases_deaths_from_file():
    file = st.file_uploader("Data file", type="csv")
    return parse_cases_deaths_data(file)


@st.cache
def parse_cases_deaths_data(io):
    if not io:
        return None
    data = pd.read_csv(io, sep=",", encoding="latin")
    data["fecha"] = pd.to_datetime(data["fecha"], format="%Y-%m-%d")
    return data


def hospitalizations():
    return hospitals.hospitalizations(st=st)


def set_task(task):
    st.session_state.task = task


def run_task():
    st.session_state.task()


st.session_state.setdefault("task", lambda: None)
st.title("COVID-19")

col1, col2 = st.columns(2)
col1.button("Capacidad asistencial", on_click=set_task, args=(hospitalizations,))
col2.button("Casos y muertes", on_click=set_task, args=(cases_deaths,))
run_task()
