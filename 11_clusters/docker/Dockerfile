FROM python:3.12-slim

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "./diffusion_numpy_memory2.py"]
