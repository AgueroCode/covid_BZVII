from covid import app
import csv
import json

@app.route("/provincias")
def provincias():
    fichero = open("data/provincias.csv", "r", encoding="utf8")  # abrir el archivo
    csvreader = csv.reader(fichero, delimiter=",") # leer registro a registro

    lista = []
    for registro in csvreader:   # crear diccionario para que lo pueda usar json
        d = {'codigo': registro[0], 'valor': registro[1]}
        lista.append(d)
    
    fichero.close() # cierro fichero
    print(lista)
    return json.dumps(lista)  # devuelvo el diccionario como json 

@app.route("/provincia/<codigoProvincia>") #al uso <> metemos un parametro, el nombre de nuestra variable que es un recurso dinamico
def laprovincia(codigoProvincia): #entre parantesis siempre se pone lo que has metido en la ruta entre <>
    fichero = open("data/provincias.csv", "r", encoding="utf8")
    dictreader = csv.DictReader(fichero, fieldnames=['codigo', 'provincia']) #otra opcion para leer registro a registro. En fieldnames si no metes nada mete la cabecera (la primera fila) que ya tiene el CSV
    
    for registro in dictreader:
        if registro['codigo'] == codigoProvincia:
            return registro['provincia']
    
    fichero.close()
    return "El valor no existe"

# @app.route("/casos/<int:year>", defaults={'mes':Nones,'dia':None}) #esto daria los casos del año entero
# @app.route("/casos/<int:year>/<int:mes>", defaults={'dia':None}) #esto daria los casos del mes entero

@app.route("/casos/<int:year>/<int:mes>/<int:dia>")
def casos(year, mes, dia):
    pass
    #1er caso devolver el numero total de casos de covid en un dia del año determinado para todas las provincias
    #2do caso. Lo mismo pero detallado por tipo de prueba diagnostica. PCR, AC, AG, ELISA, DESCONOCIDO -> JSON