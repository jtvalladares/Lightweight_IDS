import socket
from threading import Thread, Lock
import pandas as pd
import pickle


class Server:
    def __init__(self, HOST, PORT, model_route):
        self.model_route = model_route

        with open(self.model_route, 'rb') as archivo:
            self.modelo = pickle.load(archivo)

        self.socket = socket.socket()
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        print("Server is listening...")

        self.client_socket, self.client_address = self.socket.accept()
        print(f"Connection established with {self.client_address}")

        self.handle_client()

    def handle_client(self):
        while True:
            # Recibir datos serializados
            data = self.client_socket.recv(4096)
            if not data:
                break

            # Deserializar los datos (fila del DataFrame)
            row = pickle.loads(data)

            # Convertir el diccionario a un DataFrame (o numpy array)
            df_row = pd.DataFrame([row])  # Assuming row is a dict
            np_row = df_row.to_numpy()
            classification_result = self.classify_attack(np_row)
            
            # Enviar el resultado de la clasificación
            self.client_socket.send(pickle.dumps(classification_result))

    def classify_attack(self, data):
        # Convertir el DataFrame a un numpy array para la predicción
        prediction = self.modelo.predict(data)  # Modelo espera una estructura 2D (DataFrame o numpy array)
        return prediction[0]  # Retorna el resultado de la predicción

    
ruta_modelo = '/home/javb/vscode_folder/X-IIoTID dataset/client - server/model_E1.3__results.pkl_class1.pkl'
Server('127.0.0.1', 7632, ruta_modelo)
