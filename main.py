# https://github.com/vgenov-py/T-522/blob/master/covid.md

import requests as req
import json
import time
import collections
import matplotlib.pyplot as plt
from estad_covid import Statistics

# res = req.get("https://datos.comunidad.madrid/catalogo/dataset/7da43feb-8d4d-47e0-abd5-3d022d29d09e/resource/ead67556-7e7d-45ee-9ae5-68765e1ebf7a/download/covid19_tia_muni_y_distritos.json").json()

# with open("covid.json", "w", encoding="utf8") as file:
#     json.dump(res, file, indent =4, ensure_ascii=True)

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
rank = 10
print(f"TOP {rank} casos confirmados totales")
def get_worst(dataset):
    filtered_list = []
    for mun in dataset:
        try:
            mun['casos_confirmados_totales']
            filtered_list.append(mun)
        except KeyError:
            pass
    result = sorted(filtered_list, key= lambda mun: mun['casos_confirmados_totales'], reverse=True)[0:rank]
    [print(f"{mun['municipio_distrito']}: {mun['casos_confirmados_totales']}") for mun in result]

get_worst(data[0:199])
print("--------------")

#Crear una lista con la sumatoria de los casos confirmados totales por d??a
start = time.perf_counter()
fechas_uniques = []
for mun in data:
    if mun['fecha_informe'].split(" ")[0] not in fechas_uniques:
        fechas_uniques.append(mun['fecha_informe'].split(" ")[0])
print("Cantidad total de fechas: ", len(fechas_uniques))

def cases_date(data, fechas_uniques):
    dict_dates = {}
    #list_cases = []
    for date in fechas_uniques:
        dict_dates[date] = get_cases(data, date)
        #list_cases.append(get_cases(data, date))
        #print(f"Casos en el dia {fecha}: ", get_cases(data, fecha))
    return dict_dates

dict_dates = cases_date(data, fechas_uniques)
#print(dict_dates)
finish = time.perf_counter()
print("tiempo ejecucion: ", finish - start)
print("--------------")

#   CREACION LISTAS X e Y PARA EL GRAFICO POSTERIOR.
#Y =create_y(data)
#Y = dict(sorted(Y.items(), key= lambda tupla: tupla[0]))

# encontre esta forma para ordenar el diccionario y funciona.
result = collections.OrderedDict(sorted(dict_dates.items()))
y = dict(result)
Y = list(y.values())
#X = list(y.keys())
X = [num for num in range(1, len(Y)+1)]
print(Y)
print(X)
print("--------------")

# Crear un objeto estad??stica que reciba un valor X y otro valor Y, deben ser listas
# REALIZADO EN EL ARCHIVO estad_covid.py

covid_data = Statistics(X, Y)
# plt.plot(X, Y)
# plt.xlabel('26/02/2020 - 01/07/2021')
# plt.ylabel('CASOS COVID MADRID')
# plt.show()

Y_until65 = Y[:66]
X_until65 = [num for num in range(1, len(Y_until65)+1)]
# plt.plot(X_until65, Y_until65)
# plt.xlabel('Primeros 65 dias')
# plt.ylabel('CASOS COVID MADRID')
# plt.show()

Y_after65 = Y[66:]
X_after65 = [num for num in range(1, len(Y_after65)+1)]
plt.plot(X_after65, Y_after65)
plt.xlabel('Despues de los 65 primeros dias')
plt.ylabel('CASOS COVID MADRID')
plt.show()

# Cu??ntos confirmados tendremos el 1 de agosto del a??o 2020?
after65 = Statistics(X_after65, Y_after65)
# print(len(X_after65))
# print(after65.rxy)

# como la fecha que queremos predecir es 31 dias posterior a la ultima toma de datos
# he calculado la longitud de la muestra que tengo con len() y le sumo 31 dias asi me da el resultado.
date_topredict = len(X_after65) + 31
print("La prediccion de casos confirmados para el 01/08/2021 sera: ", after65.prediction(date_topredict))

