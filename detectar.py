import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import sys

# Etiquetas (en orden alfabético por carpeta)
labels = ['Blight', 'Common_Rust', 'Gray_Leaf_Spot', 'Healthy_corn']

# Cargar modelo
model = tf.keras.models.load_model('modelo/cnn_model_fases.h5')

# Cargar imagen
img_path = sys.argv[1]
img = image.load_img(img_path, target_size=(150, 150))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0

# Predecir
prediction = model.predict(img_array)[0]
resultado = np.argmax(prediction)
print("Fase detectada:", labels[resultado])
