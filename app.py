from flask import Flask, render_template, request, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Clave de API de Spoonacular
api_key = 'fecc058e698d4731970fe29eec678435'
API = "https://api.spoonacular.com/recipes/complexSearch"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recetas", methods=['GET', 'POST'])
def recetas():
    recetas_data = []

    # Parámetros por defecto de búsqueda
    params = {
        'apiKey': api_key,
        'diet': 'vegan',  # Cambia a 'glutenFree' o 'vegetarian' según lo necesites
        'maxReadyTime': 30,  # Tiempo máximo de preparación en minutos
        'number': 5,  # Número de recetas a retornar
        'instructionsRequired': True,  # Solo recetas con instrucciones
        'minCalories': 200,  # Calorías mínimas por porción
        'maxCalories': 500,  # Calorías máximas por porción
        'addRecipeInformation': True,  # Incluir información adicional de la receta
        'sort': 'calories',  # Ordenar por calorías, también podrías usar 'time', 'difficulty', etc.
    }

    if request.method == 'POST':
        # Obtenemos los datos del formulario si el usuario cambia las preferencias de búsqueda
        dieta = request.form.get('dieta')
        max_tiempo = request.form.get('max_tiempo')
        calorias_min = request.form.get('calorias_min')
        calorias_max = request.form.get('calorias_max')

        # Actualizamos los parámetros con los valores del formulario
        if dieta:
            params['diet'] = dieta
        if max_tiempo:
            params['maxReadyTime'] = int(max_tiempo)
        if calorias_min:
            params['minCalories'] = int(calorias_min)
        if calorias_max:
            params['maxCalories'] = int(calorias_max)

    # Hacemos la solicitud a la API
    response = requests.get(API, params=params)

    # Verificamos el estado de la respuesta
    if response.status_code == 200:
        data = response.json()
        recetas_data = data['results']
    else:
        flash("Error al obtener las recetas. Intenta nuevamente.", 'danger')

    return render_template("recetas.html", recetas=recetas_data)

if __name__ == '__main__':
    app.run(debug=True)
