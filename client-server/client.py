import socket
from threading import Thread, Lock
import pandas as pd
import pickle

class Client:
    def __init__(self, HOST, PORT, route_csv, output_csv):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))            

        self.df = pd.read_csv(route_csv)
        self.df = self.df.drop(columns=['class1'])
        self.output_csv = output_csv
        self.classification_results = []

        # Lock para controlar flujo de mensajes
        self.lock = Lock()

        self.talk_to_server()

    def talk_to_server(self):
        # Iniciar hilo receptor
        Thread(target=self.receive_message, daemon=True).start()
        # Enviar filas al servidor
        self.send_message()

    def send_message(self):
        for _, row in self.df.iterrows():
            self.lock.acquire()
            # Serializar fila y enviar
            data = pickle.dumps(row.to_dict())
            self.socket.send(data)

    def receive_message(self):
        i = 0
        while True:
            # Recibir resultado del servidor
            data = self.socket.recv(4096)
            if not data:
                break

            classification_result = pickle.loads(data)
            self.classification_results.append(classification_result)

            print(f'Received: {i+1} / {len(self.df)}')
            i += 1

            self.lock.release()

    def save_results(self):
        results_df = pd.DataFrame(self.classification_results, columns=['classification_result'])
        results_df.to_csv(self.output_csv, index=False)
        print(f'Results saved to {self.output_csv}')

# Example usage for client (in a separate script or thread)
ruta_csv = '/home/javb/vscode_folder/X-IIoTID dataset/client - server/E1.3__results.pkl_class1_test.csv'
output_csv = '/home/javb/vscode_folder/X-IIoTID dataset/client - server/classification_results.csv'
Client('127.0.0.1', 7632, ruta_csv, output_csv)
Client.save_results()