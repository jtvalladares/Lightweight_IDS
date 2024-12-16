# Content

Code for model and test dataset generation: "generar_modelos.ipynb"

Resulting test_splits are located in the folder "test_splits"

Resulting models are located in the folder "models"

Models are meant to be run in the Jetson (client) to classify each record in the corresponding test_split file. Each record will be send by server, wich will also receive the inference result.

Code for main feature selection and feature variation experiment: clasificacion_ataques_it.ipynb
