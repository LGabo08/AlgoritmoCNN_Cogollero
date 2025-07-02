import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Preparar datos
data_gen = ImageDataGenerator(validation_split=0.2, rescale=1./255)

train = data_gen.flow_from_directory(
    'CornPhases',
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val = data_gen.flow_from_directory(
    'CornPhases',
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Mostrar clases
print("Clases:", train.class_indices)

# Construir modelo CNN
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(4, activation='softmax')  # ← 4 clases
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar modelo
model.fit(train, epochs=10, validation_data=val)

# Guardar modelo
model.save('modelo/cnn_model_fases.h5')
