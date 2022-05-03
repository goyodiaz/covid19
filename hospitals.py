import pandas as pd


def occupation_by_region(st, data):
    region = st.selectbox("Comunidad", ["ESPAÑA"] + get_regions(data), key=0)
    region_data = get_occupation_by_region(data=data, region=region)

    start, end = region_data.index[[0, -1]].date
    start, end = choose_period(st=st, min_value=start, max_value=end)

    st.write(start, end)
    chart_data = region_data[start:end]

    st.area_chart(chart_data.rename_axis(columns=None))
    st.write(
        chart_data.assign(**{"Total ocupadas COVID-19": chart_data.sum(axis="columns")})
    )


def choose_period(st, min_value, max_value):
    if min_value == max_value:
        return min_value, max_value
    return st.slider("Periodo", min_value=min_value, max_value=max_value, value=(min_value, max_value))


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


def load_data(st):
    return load_from_url(st=st)


def load_from_file(st):
    buf = st.file_uploader("Data file", type="csv")
    return parse_data(io=buf)


def load_from_url(st):
    date = st.date_input("Día")
    formatted_date = date.strftime("%d%m%Y")
    url = f"https://www.sanidad.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Datos_Capacidad_Asistencial_Historico_{formatted_date}.csv"
    st.write(f"Origen de los datos: {url}")
    return st.cache(parse_data)(url)


def parse_data(io):
    if not io:
        return None
    data = pd.read_csv(io, sep=";", encoding="latin")
    data["Fecha"] = pd.to_datetime(data["Fecha"], format="%d/%m/%Y")
    data = data.dropna(subset="Fecha")
    return data
