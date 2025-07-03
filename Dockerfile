# 1. Base oficial de Python
FROM python:3.10-slim

# 2. Instala dependencias APT mínimas
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
     ca-certificates \
     curl \
 && rm -rf /var/lib/apt/lists/*

# 3. Establece directorio de trabajo y copia el código
WORKDIR /app
COPY . .

# 4. Descarga el modelo HDF5 desde tu Release en GitHub
#    Reemplaza esta URL por la tuya tal como la ves en "Assets" de tu release
ARG MODEL_URL=https://github.com/LGabo08/AlgoritmoCNN_Cogollero/releases/download/v1.0/cnn_model_fases.h5
RUN mkdir -p ./modelo \
 && echo "=> Descargando modelo desde $MODEL_URL" \
 && curl -L "$MODEL_URL" -o ./modelo/cnn_model_fases.h5

# 5. Crea y activa un venv, luego instala dependencias Python
RUN python -m venv /opt/venv \
 && . /opt/venv/bin/activate \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

# 6. Asegúrate de usar el venv para ejecutar los comandos siguientes
ENV PATH="/opt/venv/bin:$PATH"

# 7. Expone el puerto que usas en Railway y lanza la app con Gunicorn
#    Fíjate que ahora usamos gunicorn, más robusto en producción
RUN pip install gunicorn
EXPOSE 5000
CMD ["gunicorn", "api.app:app", "--bind", "0.0.0.0:5000"]
