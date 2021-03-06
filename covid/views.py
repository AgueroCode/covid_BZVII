from os import error
from flask import render_template, request #va a la carpeta template, busca el template y lo devuelve - request es una instancia en la que esta toda la informacion de la peticion
from covid import app
import csv
import json
from datetime import date

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

@app.route("/casos/<int:year>", defaults={'mes':None,'dia':None}) 
@app.route("/casos/<int:year>/<int:mes>", defaults={'dia':None}) 
@app.route("/casos/<int:year>/<int:mes>/<int:dia>") #ponemos int para que sean numero enteros
def casos(year, mes, dia):

    if not mes:
        fecha = "{:04d}".format(year, mes)
    elif not dia: 
        fecha = "{:04d}-{:02d}".format(year, mes)
    else:
        fecha = "{:04d}-{:02d}-{:02d}".format(year, mes, dia) #equivale a f"{:04d}-{:02d}-{:02d}"
    
    fichero = open("data/casos_diagnostico_provincia.csv", "r", encoding="utf8")
    dictreader = csv.DictReader(fichero) 
    
    res = {
        'num_casos': 0,
        'num_casos_prueba_pcr': 0,
        'num_casos_prueba_test_ac': 0,
        'num_casos_prueba_ag': 0,
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0
    }

    for registro in dictreader: #iteramos el diccionario de todos los registros
        if fecha in registro['fecha']:
            for clave in res: #iteramos el diccionario que hemos creado
                res[clave] += int(registro[clave])

        elif registro['fecha'] > fecha:
            break

    fichero.close()
    return json.dumps(res)

@app.route("/incidenciasdiarias", methods = ['GET', 'POST'])
def incidencia():
    formulario = {
        'provincia': '',
        'fecha': str(date.today()),
        'num_casos_prueba_pcr': 0,
        'num_casos_prueba_test_ac': 0,
        'num_casos_prueba_ag': 0,
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0
    }

    fichero = open('data/provincias.csv', 'r', encoding="utf8")
    csvreader = csv.reader(fichero, delimiter=",")
    # next(csvreader)
    lista = []
    for registro in csvreader: 
        d = {'codigo': registro[0], 'descripcion': registro[1]}
        lista.append(d)

    fichero.close()

    if request.method == 'GET':
        return render_template("alta.html", datos=formulario, 
                               provincias=lista, error="") #aqui renderiza el template que hemos creado en templates - datos es lo que va a usar (es la clave) jinja basado en el formulario (que es el valor)
    
    for clave in formulario:  #aqui vamos a informar el formulario para que 'recuerde' los datos
        formulario[clave] = request.form[clave]      

    #validamos que num_casos en general es entero no negativo
    num_pcr = request.form['num_casos_prueba_pcr']
    try:
        num_pcr = int(num_pcr)
        if num_pcr < 0:
            raise ValueError('Debe ser positivo') #raise lanza una excepcion de forma automatica
    except ValueError: #captura solo el error en ese valor, no cualquier error
        return render_template("alta.html", datos=formulario, error = "PCR no puede ser negativa") #devolvemos algo al servidor gracias jinja   
    
    return "Se ha hecho un post"


   

    

