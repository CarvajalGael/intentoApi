from flask import Flask, render_template, request, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

api_key = 'fecc058e698d4731970fe29eec678435'
API = "https://api.spoonacular.com/recipes/complexSearch"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recetas", methods=['GET', 'POST'])
def recetas():
    recetas_data = []

    params = {
        'apiKey': api_key,
        'diet': 'vegan',  
        'maxReadyTime': 30,
        'number': 5,
        'instructionsRequired': True,
        'minCalories': 200,
        'maxCalories': 500,
        'addRecipeInformation': True,
        'sort': 'calories',
    }

    if request.method == 'POST':
        dieta = request.form.get('dieta')
        max_tiempo = request.form.get('max_tiempo')
        calorias_min = request.form.get('calorias_min')
        calorias_max = request.form.get('calorias_max')

        if dieta:
            params['diet'] = dieta

        if max_tiempo:
            params['maxReadyTime'] = int(max_tiempo)

        if calorias_min:
            params['minCalories'] = int(calorias_min)

        if calorias_max:
            params['maxCalories'] = int(calorias_max)


    response = requests.get(API, params=params)

    if response.status_code == 200:
        data = response.json()
        recetas_data = data.get('results', [])
    else:
        flash("Error al obtener las recetas. Intenta nuevamente.", 'danger')

    return render_template("recetas.html", recetas=recetas_data)

if __name__ == '__main__':
    app.run(debug=True)
