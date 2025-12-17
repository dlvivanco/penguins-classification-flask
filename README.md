# 🐧 Clasificación de Pingüinos del Archipiélago Palmer

Este proyecto implementa una solución completa de *Machine Learning* para predecir la especie de un pingüino basándose en sus medidas físicas. El flujo de trabajo abarca desde el análisis exploratorio de datos hasta el despliegue de modelos mediante una API REST con Flask.


## 📋 Descripción del Proyecto

El objetivo es clasificar pingüinos en tres especies (**Adelie**, **Chinstrap**, **Gentoo**) utilizando el dataset **Palmer Archipelago (Antarctica) penguin data**.

El proyecto incluye:

- ✅ **Preparación de datos**: eliminación de filas con `NA`, codificación *one-hot* con `DictVectorizer` y normalización con `StandardScaler`.
- ✅ **Entrenamiento y evaluación** de 4 modelos: **Regresión Logística**, **SVM**, **Árbol de Decisión**, **KNN**.
- ✅ **Serialización** de los modelos (`.pck`) para reutilizarlos en despliegue.
- ✅ **API REST con Flask** para realizar predicciones.
- ✅ **Cliente** para enviar al menos 2 peticiones a cada modelo y mostrar las respuestas.
---

## 📂 Estructura del Repositorio

```plaintext
penguins-classification-flask/
│
├── dataset/
│   └── penguins_size.csv       # Dataset original (requerido)
│
├── models/                     # Modelos entrenados (.pck)
│   ├── decision_tree.pck
│   ├── knn.pck
│   ├── logistic_regression.pck
│   └── svm.pck
│
├── notebooks/
│   ├── train_model.ipynb       # Notebook de limpieza, entrenamiento y serialización
│   └── client.ipynb            # Notebook para testear el cliente contra la API
│
├── predict_app.py              # Script del servidor Flask
├── environment.yml             # Dependencias del proyecto (Conda)
└── README.md                   # Documentación del proyecto

```

---

## 🚀 Instalación y Requisitos

Este proyecto utiliza **Python 3.9+**. Para asegurar la compatibilidad y gestionar las dependencias correctamente, se utiliza **Conda** mediante un archivo de configuración `environment.yml`.

### 1. Configuración del entorno (`environment.yml`)
El archivo llamado `environment.yml` en la carpeta raíz del proyecto con el siguiente contenido:

```yaml
name: penguins_env
channels:
  - defaults
dependencies:
  - python=3.9
  - pandas
  - numpy
  - scikit-learn
  - flask
  - requests
  - seaborn
  - matplotlib
  - jupyter
  - pip
```

### Instalación y Activación

Puedes crear el entorno virtual e instalar todas las dependencias automáticamente ejecutando los siguientes comandos en tu terminal:

```bash
# Crear el entorno a partir del archivo YAML
conda env create -f environment.yml

# Activar el entorno creado
conda activate penguins_env
```

---

## 📦 Dataset

El proyecto requiere el archivo de datos en la siguiente ruta: `dataset/penguins_size.csv`


---

## 🧪 Entrenamiento y serialización de modelos

Antes de iniciar el servidor, es necesario entrenar los modelos. Ejecuta paso a paso el Jupyter Notebook: `📂 notebooks/train_model.ipynb`

```bash
notebooks/train_model.ipynb
```

Este proceso realiza lo siguiente:

1) Carga el dataset y elimina filas con valores nulos.
2) Divide los datos **80% train / 20% test**  
3) Escala variables numéricas con `StandardScaler`
4) Aplica one-hot encoding a categóricas con `DictVectorizer`  
5) Entrena 4 modelos y los guarda en la carpeta `models/`:

- `models/logistic_regression.pck`
- `models/svm.pck`
- `models/decision_tree.pck`
- `models/knn.pck`

---

## 🌐 Ejecutar la API (Flask)

Una vez generados los modelos, arranca el servidor desde la terminal (estando en la raíz del proyecto):

```bash
python predict_app.py
```

El servidor corre en:

- `http://127.0.0.1:9696`

### Endpoints

La API expone un endpoint por modelo:

- `POST /predict/lr` (Regresión Logística)
- `POST /predict/svm` (Support Vector Machine)
- `POST /predict/dt` (Árbol de Decisión)
- `POST /predict/knn` (K-Nearest Neighbors)


### Ejemplo de petición (JSON)

```json
{
  "island": "Torgersen",
  "culmen_length_mm": 39.1,
  "culmen_depth_mm": 18.7,
  "flipper_length_mm": 181.0,
  "body_mass_g": 3750.0,
  "sex": "MALE"
}
```

### Ejemplo con `curl`

```bash
curl -X POST "http://127.0.0.1:9696/predict/lr"   -H "Content-Type: application/json"   -d '{
    "island":"Torgersen",
    "culmen_length_mm":39.1,
    "culmen_depth_mm":18.7,
    "flipper_length_mm":181.0,
    "body_mass_g":3750.0,
    "sex":"MALE"
  }'
```

---

## 🧑‍💻 Cliente de prueba

Con el servidor encendido, ejecutamos paso por paso el Jupyter Notebook::

```bash
notebooks/client.ipynb
```

El cliente enviará automáticamente peticiones a cada uno de los 4 modelos y mostrará la predicción en pantalla.

---

## 🧠 Modelos implementados

- **Regresión logística**: baseline lineal
- **SVM**: hiperplano separador (en el ejemplo con `probability=True`)
- **Árbol de decisión**: reglas con profundidad acotada para evitar sobreajuste
- **KNN**: clasificación por vecinos más cercanos

---

## 📊 Preprocesamiento aplicado

- **Limpieza**: eliminación de filas con valores nulos (`dropna`).
- **Escalado**: `StandardScaler` sobre variables numéricas (media 0, desviación 1).  
  - Se ajusta **solo con train** y se aplica a **train y test**.
- **Codificación**: `DictVectorizer` para variables categóricas (`island`, `sex`) mediante one-hot.

---

## ✅ Checklist de entrega (rúbrica)

- [x] Entorno y dependencias (Conda / pip) documentadas
- [x] Preparación de datos (NA, split 80/20, escalado, one-hot)
- [x] Entrenamiento de 4 modelos (LogReg, SVM, DT, KNN)
- [x] Serialización de 4 modelos
- [x] API Flask para servir predicciones
- [x] Cliente con mínimo 2 peticiones por modelo
- [x] Repositorio público en GitHub con README

---

## 📌 Notas

- Ejecuta `notebooks/train_model.ipynb` **antes** de levantar `predict_app.py` para que existan los `.pck` en `models/`.
