from flask import Flask, render_template, redirect, url_for, request, session, jsonify 
from gemini_outfit import gemini_outfit
from utils import order_dict, import_json
import webbrowser

app = Flask(__name__)

@app.route('/producto')
def producto():
    producto = import_json('data/product_details.json')

    return render_template('producto.html', producto=producto)

@app.route('/recomendaciones', methods=['POST'])
def recomendaciones():
    data = request.get_json()
    imageUrl = data['imageUrl']
    
    # Extraer la parte de la ruta después de 'static/'
    user_image_path = imageUrl.split('/static/')[1]

    # Usamos la funcion de gemini y ordenamos el diccionario con todas las imagenes
    outfit_path_dict = gemini_outfit(imageUrl, 'my_closet')
    outfit_path_dict_ordered = order_dict(outfit_path_dict, user_image_path)
    result_image_paths = list(outfit_path_dict_ordered.values())  # Obtener solo las rutas de las imágenes

    # Redirigir a la página de resultados
    return jsonify({'redirect': url_for('resultados', result_image_paths=result_image_paths, producto=producto)})

@app.route('/resultados')
def resultados():
    result_image_paths = request.args.getlist('result_image_paths')
    # user_image_path = request.args.getlist('user_image_path')[0]
    producto = import_json('data/product_details.json')
    
    return render_template('result_v2.html', result_image_paths=result_image_paths, producto=producto)

@app.route('/')
def inicio():
    return redirect(url_for('producto')) 

if __name__ == '__main__':
    port = 5001
    webbrowser.open_new(f'http://127.0.0.1:{port}/')
    app.run(debug=False,host='127.0.0.1', port=port)
