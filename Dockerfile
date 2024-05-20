# Use the official Python 3.7 image from the Docker Hub
FROM python:3.7-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0


# Set the working directory in the container
WORKDIR /application

# Copy the requirements file into the container at /app
COPY requirements.txt /application/

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Copy the rest of your application into the container at /app
COPY . /application/
RUN mv /application/app/ai/darknet_lib/libdarknet.* /usr/local/lib
RUN echo -e "classes=35\nnames=/application/app/ai/weights/ocr/ocr-net.names" > /application/app/ai/weights/ocr/ocr-net.data
# Set environment variables for your application
ENV DETECTION_WEIGHT_PATH='/application/app/ai/weights/lp-detector/wpod-net_update1'
ENV OCR_DATASET='/application/app/ai/weights/ocr/ocr-net.data'
ENV OCR_NETCFG='/application/app/ai/weights/ocr/ocr-net.cfg'
ENV OCR_WEIGHT='/application/app/ai/weights/ocr/ocr-net.weights'
ENV FLASK_CONFIG='development'
ENV PYTHONPATH='/application'
# Expose the port that the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app/main.py"]