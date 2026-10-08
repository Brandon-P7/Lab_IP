from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")

def hola_mundo():
    return "<h1> ¡Hola mundo desde Fa¿lask! </h1>]"

if 