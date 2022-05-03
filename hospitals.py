import pandas as pd


def url_by_date(date):
    formatted_date = date.strftime("%d%m%Y")
    return f"https://www.sanidad.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Datos_Capacidad_Asistencial_Historico_{formatted_date}.csv"


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


def parse_data(io):
    if not io:
        return None
    data = pd.read_csv(io, sep=";", encoding="latin")
    data["Fecha"] = pd.to_datetime(data["Fecha"], format="%d/%m/%Y")
    data = data.dropna(subset="Fecha")
    return data
