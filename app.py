from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Conexión MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["pedidosDB"]
coleccion = db["pedidos"]

# LISTAR pedidos
@app.route("/")
def index():
    pedidos = list(coleccion.find())
    return render_template("index.html", pedidos=pedidos)

# FORM crear
@app.route("/crear")
def crear():
    return render_template("crear.html")

# GUARDAR pedido
@app.route("/guardar", methods=["POST"])
def guardar():
    pedido = {
        "cliente": request.form["cliente"],
        "producto": request.form["producto"],
        "cantidad": int(request.form["cantidad"]),
        "estado": "Pendiente"
    }
    coleccion.insert_one(pedido)
    return redirect(url_for("index"))

# ELIMINAR
@app.route("/eliminar/<id>")
def eliminar(id):
    coleccion.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("index"))

# FORM editar
@app.route("/editar/<id>")
def editar(id):
    pedido = coleccion.find_one({"_id": ObjectId(id)})
    return render_template("editar.html", pedido=pedido)

# ACTUALIZAR
@app.route("/actualizar/<id>", methods=["POST"])
def actualizar(id):
    coleccion.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "cliente": request.form["cliente"],
            "producto": request.form["producto"],
            "cantidad": int(request.form["cantidad"]),
            "estado": request.form["estado"]
        }}
    )
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
