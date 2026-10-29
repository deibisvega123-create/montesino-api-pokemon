
from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def inicio():
    pokemon = None
    error = None

    if request.method == "POST":
        nombre = request.form.get("pokemon", "").strip().lower()

        if nombre:
            url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"
            respuesta = requests.get(url, timeout=10)

            if respuesta.status_code == 200:
                datos = respuesta.json()

                pokemon = {
                    "nombre": datos["name"].capitalize(),
                    "imagen": datos["sprites"]["front_default"],
                    "tipos": [
                        tipo["type"]["name"]
                        for tipo in datos["types"]
                    ],
                    "movimientos": [
                        movimiento["move"]["name"]
                        for movimiento in datos["moves"][:10]
                    ]
                }
            else:
                error = "No se encontró ese Pokémon."

    return render_template(
        "index.html",
        pokemon=pokemon,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
