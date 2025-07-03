# 1. Base oficial de Python
FROM python:3.10-slim

# 2. Instala dependencias APT y Git LFS
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
     ca-certificates \
     curl \
     git \
     apt-transport-https \
 && \
 # Instala Git LFS siguiendo las instrucciones oficiales
 curl -fsSL https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh \
   | bash \
 && apt-get install -y --no-install-recommends git-lfs \
 && git lfs install \
 && rm -rf /var/lib/apt/lists/*

# 3. Copia tu código
WORKDIR /app
COPY . .



# 5. Crea un venv y instala deps
RUN python -m venv /opt/venv \
 && . /opt/venv/bin/activate \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

# 6. Asegúrate de usar ese venv
ENV PATH="/opt/venv/bin:$PATH"

# 7. Exponer el puerto y lanzar tu app
EXPOSE 5000
CMD ["python", "api/app.py"]
