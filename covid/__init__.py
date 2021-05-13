from flask import Flask

app = Flask(__name__) #la app hay que crearla aqui

from covid import views #aqui nos traemos las rutas que vamos a ir guardando en views