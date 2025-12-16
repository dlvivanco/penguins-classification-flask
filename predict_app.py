import pickle
import numpy as np
import os
from flask import Flask, request, jsonify

app = Flask('penguins_predict')

# Mapa inverso para devolver el nombre de la especie
species_map_inv = {0: 'Adelie', 1: 'Chinstrap', 2: 'Gentoo'}
numerical = ['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g']

def predict_single(customer, scaler, dv, model):
    # 1. Escalar variables numéricas
    features_num = np.array([
        customer['culmen_length_mm'],
        customer['culmen_depth_mm'],
        customer['flipper_length_mm'],
        customer['body_mass_g']
    ]).reshape(1, -1)
    
    features_scaled = scaler.transform(features_num)[0]
    
    # Actualizar el diccionario con los valores escalados
    customer_processed = customer.copy()
    for i, col in enumerate(numerical):
        customer_processed[col] = features_scaled[i]
        
    # 2. Vectorizar
    X = dv.transform([customer_processed])
    
    # 3. Predecir
    y_pred = model.predict(X)[0]
    return species_map_inv[y_pred]

def load_model(name):
    # Ajustamos la ruta para salir de 'notebooks' e ir a 'models'
    path = f'./models/{name}.pck'
    print(f"Cargando modelo desde: {path}")
    with open(path, 'rb') as f:
        return pickle.load(f)

# Cargar los 4 modelos en memoria al iniciar la app
try:
    scaler_lr, dv_lr, model_lr = load_model('logistic_regression')
    scaler_svm, dv_svm, model_svm = load_model('svm')
    scaler_dt, dv_dt, model_dt = load_model('decision_tree')
    scaler_knn, dv_knn, model_knn = load_model('knn')
    print("¡Todos los modelos cargados correctamente!")
except FileNotFoundError as e:
    print(f"Error crítico: No se encontró el archivo de modelo. {e}")

@app.route('/predict/lr', methods=['POST'])
def predict_lr():
    penguin = request.get_json()
    prediction = predict_single(penguin, scaler_lr, dv_lr, model_lr)
    return jsonify({'model': 'Logistic Regression', 'species': prediction})

@app.route('/predict/svm', methods=['POST'])
def predict_svm():
    penguin = request.get_json()
    prediction = predict_single(penguin, scaler_svm, dv_svm, model_svm)
    return jsonify({'model': 'SVM', 'species': prediction})

@app.route('/predict/dt', methods=['POST'])
def predict_dt():
    penguin = request.get_json()
    prediction = predict_single(penguin, scaler_dt, dv_dt, model_dt)
    return jsonify({'model': 'Decision Tree', 'species': prediction})

@app.route('/predict/knn', methods=['POST'])
def predict_knn():
    penguin = request.get_json()
    prediction = predict_single(penguin, scaler_knn, dv_knn, model_knn)
    return jsonify({'model': 'KNN', 'species': prediction})

if __name__ == '__main__':
    app.run(debug=True, port=9696)