import os
import tempfile
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf

# 1) Carga variables de entorno desde .env (en local) o desde configuración de Railway
load_dotenv()
MODEL_PATH = os.environ.get('MODEL_PATH', './modelo/cnn_model_fases.h5')
PORT       = int(os.environ.get('PORT', 5000))
DEBUG      = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

# 2) Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

# 3) Carga el modelo desde la ruta configurada
logger.info(f'Loading model from: {MODEL_PATH}')
model = tf.keras.models.load_model(MODEL_PATH)

# Mapear índices a etiquetas
CLASS_LABELS = {
    0: "sana",
    1: "incipiente",
    2: "moderada",
    3: "avanzada",
    4: "crítica"
}

# 4) Inicializa Flask
app = Flask(__name__)
CORS(app)

@app.route('/ping', methods=['GET'])
def ping():
    return "API modelo de fases activa", 200

@app.route('/predict', methods=['POST'])
def predict():
    logger.info('Petición /predict recibida')
    # Validar carga de archivo
    if 'file' not in request.files:
        logger.warning('No se recibió archivo')
        return jsonify({"error": "No has subido ningún archivo"}), 400

    file = request.files['file']
    if not file.filename:
        logger.warning('Nombre de archivo vacío')
        return jsonify({"error": "El nombre del archivo está vacío"}), 400

    # Guardar imagen en un temporal
    suffix = os.path.splitext(file.filename)[1]
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    img_path = tmp.name
    file.save(img_path)
    tmp.close()

    try:
        # Preprocesar imagen
        img = image.load_img(img_path, target_size=(150, 150))
        arr = image.img_to_array(img)
        arr = np.expand_dims(arr, axis=0) / 255.0

        # Hacer predicción
        preds = model.predict(arr)[0]
        idx = int(np.argmax(preds))
        confidence = float(np.max(preds))
        logger.info(f'Predicción: clase={idx}, confianza={confidence:.3f}')

    except Exception as e:
        logger.exception('Error al procesar /predict:')
        return jsonify({"error": str(e)}), 500

    finally:
        # Limpieza del archivo temporal
        try:
            os.remove(img_path)
        except OSError:
            pass

    nivel = CLASS_LABELS.get(idx, "desconocido")
    tiene_plaga = (idx != 0)
    estado = "tiene plaga" if tiene_plaga else "sana"

    # Respuesta JSON
    return jsonify({
        "class_index": idx,
        "nivel_infeccion": nivel,
        "tiene_plaga": tiene_plaga,
        "estado": estado,
        "confidence": confidence
    })

if __name__ == '__main__':
    # 5) Arranca el servidor con las vars de entorno
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
