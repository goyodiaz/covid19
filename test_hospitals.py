from io import StringIO
import unittest

import pandas as pd

import hospitals


class TestHospitals(unittest.TestCase):
    def test_parse_data_discards_nat(self):
        text = (
            "Fecha;Unidad;COD_CCAA;CCAA;Cod_Provincia;Provincia;TOTAL_CAMAS;OCUPADAS_COVID19;OCUPADAS_NO_COVID19;INGRESOS_COVID19;ALTAS_24h_COVID19\n"
            "18/04/2022;U. Críticas SIN respirador;16;PAÍS VASCO;1;Araba/Álava;8;0;0;0;0\n"
            ";;;;;;;;;;\n"
        )
        data = hospitals.parse_data(io=StringIO(text))
        self.assertTrue(data["Fecha"].notna().all())

    def test_get_regions(self):
        text = (
            "Fecha;Unidad;COD_CCAA;CCAA;Cod_Provincia;Provincia;TOTAL_CAMAS;OCUPADAS_COVID19;OCUPADAS_NO_COVID19;INGRESOS_COVID19;ALTAS_24h_COVID19\n"
            "18/04/2022;U. Críticas SIN respirador;16;ANDALUCÍA;1;Araba/Álava;8;0;0;0;0\n"
            "18/04/2022;U. Críticas SIN respirador;16;ARAGÓN;1;Araba/Álava;8;0;0;0;0\n"
            "18/04/2022;U. Críticas SIN respirador;16;ARAGÓN;1;Araba/Álava;8;0;0;0;0\n"
        )
        data = hospitals.parse_data(io=StringIO(text))
        regions = hospitals.get_regions(data=data)
        self.assertEqual(["ANDALUCÍA", "ARAGÓN"], list(regions))

    def test_get_occupation_all_regions(self):
        text = (
            "Fecha;Unidad;COD_CCAA;CCAA;Cod_Provincia;Provincia;TOTAL_CAMAS;OCUPADAS_COVID19;OCUPADAS_NO_COVID19;INGRESOS_COVID19;ALTAS_24h_COVID19\n"
            "01/08/2020;Hospitalización convencional;9;CATALUÑA;17;Girona;2105;33;1468;3;3\n"
            "01/08/2020;U. Críticas CON respirador;6;CANTABRIA;39;Cantabria;89;5;43;0;1\n"
            "01/08/2020;U. Críticas SIN respirador;12;GALICIA;15;Coruña, A;211;2;72;0;0\n"
        )
        data = hospitals.parse_data(io=StringIO(text))
        reg_data = hospitals.get_occupation_by_region(data, region="ESPAÑA")
        expected = pd.DataFrame(
            [[33, 5, 2]],
            columns=[
                "Hospitalización convencional",
                "U. Críticas CON respirador",
                "U. Críticas SIN respirador",
            ],
            index=[pd.Timestamp("2020-08-01")],
        )
        pd.testing.assertFrameEqual(expected, reg_data)


if __name__ == "__main__":
    unittest.main()
