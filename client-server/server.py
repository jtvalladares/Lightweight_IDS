import socket
from threading import Thread, Lock
import pandas as pd
import numpy as np
import pickle
import re
import time
from tensorflow.keras.models import load_model

class Server:
    def __init__(self, HOST, PORT, model_folder):
        self.model_folder = model_folder
        self.model_name = None
        self.current_model = None
        self.times = []

        self.socket = socket.socket()
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        print("Server is listening...")

        self.client_socket, self.client_address = self.socket.accept()
        print(f"Connection established with {self.client_address}")

        self.handle_client()

    def handle_client(self):
        while True:
            data = self.client_socket.recv(4096)
            if not data:
                break

            # Determinar si se recibió un nombre de archivo o datos
            message = pickle.loads(data)

            if isinstance(message, dict) and "file_name" in message:
                file_name = message["file_name"]
                self.load_model(file_name)
                if not self.times:
                    print("First file")
                else:
                    media = sum(self.times) / len(self.times)
                    print(f"Mean time in previous file: {media}")
                    self.times = []
            else:
                row = message
                start_time = time.time()
                classification_result = self.classify_attack(row)
                end_time = time.time()
                self.times.append(end_time - start_time)
                self.client_socket.send(pickle.dumps(classification_result))

    def load_model(self, file_name):
        patron = r"(E[1-3]\.[1-4])__results.pkl_(class[1-3])"
        coincidencia = re.search(patron, file_name)
        
        if coincidencia:
            e_version = coincidencia.group(1)  # Ejemplo: E1.1
            class_version = coincidencia.group(2)  # Ejemplo: class1
            if e_version.startswith("E1"):
                self.model_name = f"model_{e_version}__results.pkl_{class_version}.pkl"
                model_path = self.model_folder + '/' + self.model_name
                with open(model_path, 'rb') as archivo:
                    self.current_model = pickle.load(archivo)
            else:
                self.model_name = f"model_{e_version}__results.pkl_{class_version}.h5"
                model_path = self.model_folder + '/' + self.model_name
                self.current_model = load_model(model_path)
        else:
            raise ValueError("No se encontró un patrón válido en el nombre del archivo")

    def classify_attack(self, row):
        # Convertir fila a DataFrame
        df_row = pd.DataFrame([row])
        np_row = df_row.to_numpy()

        if re.search(r'E[23]', self.model_name):
            if 'class3' in self.model_name:
                prediction = (self.current_model.predict(np_row, verbose=0) > 0.5).astype(int).flatten()
            else:
                prediction = np.argmax(self.current_model.predict(np_row, verbose=0), axis=-1)
        else:
            prediction = self.current_model.predict(np_row, verbose=0)

        return prediction[0]

# Uso del cliente y servidor

# Servidor
model_folder = '/home/ubuntu2202/Desktop/datasets/X-IIoTID dataset/models'
Server('127.0.0.1', 7632, model_folder)    
