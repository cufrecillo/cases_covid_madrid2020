# https://github.com/vgenov-py/T-522/blob/master/covid.md

import requests as req
import json

#real_path = os.path.dirname(__file__)
# res = req.get("https://datos.comunidad.madrid/catalogo/dataset/7da43feb-8d4d-47e0-abd5-3d022d29d09e/resource/ead67556-7e7d-45ee-9ae5-68765e1ebf7a/download/covid19_tia_muni_y_distritos.json").json()

# with open("covid.json", "w", encoding="utf8") as file:
#     json.dump(res, file, indent =4, ensure_ascii=True)
#print(data)

def read_json():
    with open("./covid.json", encoding="utf8") as file:
        data = json.load(file)["data"]
    return data

data = read_json()
print(len(data))
print(data[0])
print("--------------")
# Cantidad total de municipios
mun_uniques = []
for mun in data:
    if mun['codigo_geometria'] not in mun_uniques:
        mun_uniques.append(mun['codigo_geometria'])
print("Cantidad total de municipios: ", len(mun_uniques))

def get_muns(dataset, date):
    return len([mun for mun in dataset if mun['fecha_informe'].split(" ")[0] == date])
print("Cantidad total de municipios: ", get_muns(data, '2020/02/26'))
print("--------------")

# confirmados totales a 26-FEB-2020
def get_cases(dataset, date):
    total = 0
    mun_by_date = filter(lambda mun: mun['fecha_informe'].split(" ")[0] == date, dataset)
    for mun in mun_by_date:
        try:
            total += mun['casos_confirmados_totales']
        except KeyError:
            pass
    return total

date = '2020/02/26'
print(f"Casos en el dia {date}: ", get_cases(data, date))
print("--------------")

# confirmados totales a 1-JUL-2020
date = '2020/07/01'
print(f"Casos en el dia {date}: ", get_cases(data, date))
print("--------------")

#Obtener los 10 municipios con mayor cantidad de confirmados totales
