# 1. Base oficial de Python
FROM python:3.10-slim

# 2. Instala dependencias APT mínimas
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
     ca-certificates \
     curl \
 && rm -rf /var/lib/apt/lists/*

# 3. Directorio de trabajo
WORKDIR /app

# 4. Copia el código fuente
COPY . .

# 5. Define argumentos de build:
#    - GH_TOKEN (tu PAT de GitHub, se inyecta desde Railway)
#    - MODEL_URL (la URL de tu release)
ARG GH_TOKEN
ARG MODEL_URL="https://github.com/LGabo08/AlgoritmoCNN_Cogollero/releases/download/v1.0/cnn_model_fases.h5"

# 6. Descarga el modelo HDF5 con autenticación
RUN mkdir -p ./modelo \
 && echo "=> Descargando modelo desde $MODEL_URL" \
 && curl -L \
     -H "Authorization: token ${GH_TOKEN}" \
     "$MODEL_URL" \
     -o ./modelo/cnn_model_fases.h5

# 7. Crea y activa un venv, luego instala deps Python
RUN python -m venv /opt/venv \
 && . /opt/venv/bin/activate \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

# 8. Asegúrate de usar ese venv para los siguientes comandos
ENV PATH="/opt/venv/bin:$PATH"

# 9. Instala Gunicorn para producción
RUN pip install gunicorn

# 10. Expone el puerto y lanza la app con Gunicorn
EXPOSE 5000
CMD ["gunicorn", "api.app:app", "--bind", "0.0.0.0:5000"]
