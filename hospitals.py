import pandas as pd


def occupation_by_region(st, data):
    region = st.selectbox("Comunidad", ["ESPAÑA"] + get_regions(data), key=0)
    chart_data = get_occupation_by_region(data=data, region=region)
    st.area_chart(chart_data.rename_axis(columns=None))
    st.write(
        chart_data.assign(**{"Total ocupadas COVID-19": chart_data.sum(axis="columns")})
    )


def get_regions(data):
    return get_unique_values(data, col_name="CCAA")


def get_unique_values(data, col_name):
    values = data[col_name].unique()
    values.sort()
    return list(values)


def get_occupation_by_region(data, region):
    if region != "ESPAÑA":
        data = data.query(f"CCAA == '{region}'")
    return (
        data.groupby(["Fecha", "Unidad"])["OCUPADAS_COVID19"]
        .sum()
        .unstack(level="Unidad")
    )
    # ~ return (
    # ~ data.query(f"CCAA == '{region}'")
    # ~ .groupby(["Fecha", "Unidad"])["OCUPADAS_COVID19"]
    # ~ .sum()
    # ~ .unstack(level="Unidad")
    # ~ )


def load_data(st):
    data_src = st.radio("Data source", options=("URL", "Local file"), index=1)
    if data_src == "URL":
        return load_from_url(st=st)
    elif data_src == "Local file":
        return load_from_file(st=st)


def load_from_file(st):
    buf = st.file_uploader("Data file", type="csv")
    return parse_data(io=buf)


def load_from_url(st):
    default_url = "https://www.sanidad.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Datos_Capacidad_Asistencial_Historico_18032022.csv"
    url = st.text_input("Data URL")
    st.write(default_url)
    return st.cache(parse_data)(url)


def parse_data(io):
    if not io:
        return None
    data = pd.read_csv(io, sep=";", encoding="latin")
    data["Fecha"] = pd.to_datetime(data["Fecha"], format="%d/%m/%Y")
    data = data.dropna(subset="Fecha")
    return data
