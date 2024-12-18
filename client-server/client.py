import socket
from threading import Thread, Lock
import pandas as pd
import pickle
import time
import numpy as np
import os

class Client:
    def __init__(self, HOST, PORT, test_directory):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))

        self.test_directory = test_directory  # Directorio con archivos .npy

        # Lock para controlar flujo de mensajes
        self.lock = Lock()
        self.process_files()

    def process_files(self):
        test_files = [file for file in os.listdir(self.test_directory) if file.endswith('.npy')]
        for file in test_files:
            file_name = file.split('/')[-1]

            # Notificar al servidor sobre el nombre del archivo actual
            self.send_file_name(file_name)

            # Cargar datos del archivo actual
            data = np.load(os.path.join(self.test_directory, file), allow_pickle=True)

            real_labels = data[:, -2]
            other_predictions = data[:, -1]
            data = data[:, :-2]  # Eliminar las dos últimas columnas

            # Iniciar recolección de tiempos y predicciones
            self.time_deltas = []
            self.predictions = []

            Thread(target=self.receive_predictions, daemon=True).start()
            self.send_data(data)

            # Calcular métricas al finalizar archivo
            self.calculate_metrics(real_labels, other_predictions)

    def send_file_name(self, file_name):
        self.lock.acquire()
        self.socket.send(pickle.dumps({"file_name": file_name}))
        self.lock.release()

    def send_data(self, data):
        for row in data:
            self.lock.acquire()
            start_time = time.time()
            row_dict = {f"col_{i}": val for i, val in enumerate(row)}
            serialized_data = pickle.dumps(row_dict)
            self.socket.send(serialized_data)
            self.time_deltas.append((start_time, None))

    def receive_predictions(self):
        i = 0
        while True:
            data = self.socket.recv(4096)
            if not data:
                break

            prediction = pickle.loads(data)
            end_time = time.time()

            # Registrar tiempo de respuesta y predicción
            self.time_deltas[i] = (self.time_deltas[i][0], end_time)
            self.predictions.append(prediction)

            i += 1
            self.lock.release()

    def calculate_metrics(self, real_labels, other_predictions):
        # Calcular tiempo promedio
        times = [end - start for start, end in self.time_deltas if end is not None]
        avg_time = sum(times) / len(times) if times else 0

        # Calcular accuracy
        prediction_accuracy = sum(1 for p, r in zip(self.predictions, real_labels) if p == r) / len(real_labels)
        other_accuracy = sum(1 for p, o in zip(self.predictions, other_predictions) if p == o) / len(other_predictions)

        print(f"Average response time: {avg_time:.4f} seconds")
        print(f"Prediction accuracy: {prediction_accuracy * 100:.2f}%")
        print(f"Other system accuracy: {other_accuracy * 100:.2f}%")

# Cliente
# listar todos los archivos de test
# def list_npy_files(directory):
#     return [file for file in os.listdir(directory) if file.endswith('.npy')]

directory_path = '/home/ubuntu2202/Desktop/datasets/X-IIoTID dataset/test_splits'
# test_files = list_npy_files(directory_path)

Client('127.0.0.1', 7632, directory_path)