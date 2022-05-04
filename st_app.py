import pandas as pd
import streamlit as st

import hospitals


def main():
    TITLE = "Hospitalizaciones COVID-19"
    st.set_page_config(
        page_title=TITLE,
        layout="wide",
        menu_items={"About": "Brough to you by Goyo"},
    )
    st.title(TITLE)

    date = st.date_input("Día")

    url = hospitals.url_by_date(date=date)

    st.write(f"[Origen de los datos]({url})")

    # XXX decouple streamlit and parsing
    data = st.cache(hospitals.parse_data)(url)
    if data is None:
        st.stop()

    region = st.selectbox("Comunidad", ["ESPAÑA"] + hospitals.get_regions(data), key=0)

    region_data = hospitals.get_occupation_by_region(data=data, region=region)
    min_date, max_date = region_data.index[[0, -1]].date

    if min_date < max_date:
        start, end = st.slider(
            "Periodo",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
        )
    else:
        start, end = min_date, max_date
    st.write(start, end)

    chart_data = region_data[start:end]

    st.area_chart(chart_data.rename_axis(columns=None))
    st.write(
        chart_data.assign(**{"Total ocupadas COVID-19": chart_data.sum(axis="columns")})
    )


if __name__ == "__main__":
    main()
