# Lightweight_IDS

Code and archives associated to the development of a lightweight IDS (Intrusion Detection System) for ICPS (Industrial Cyber Physical System).

The content of folders is the following:

- **models:** Modelos entrenados para usar en Jetson, y Jupyter Notebook. Contiene modelos entrenados siguiendo la descripcion de los experimentos haciendo un split de 80/20 para train/test. En los modelos con feature selection se usan las m features que mas se repitieron en los folds del experimento, siendo m el entero superior de la cantidad de features media eseleccionadas. Son 3 modelos por cada experimento, correspondiente al tipo de clasificacion. Se guardan tambien los splits de train/test para las pruebas en Jetson.

Detalles del nombre de los archivos:
- E1.x: Clasificador Decission Tree
- E2.x: Clasificador DNN
- E3.x: Clasificador CNN
- ---
- Ex.1: Usar todas las features
- Ex.2: Eliminar features correlacionadas
- Ex.3: Seleccionar features con RFECV (Recursive Feature Elimination with Cross-Validation)
- Ex.4: Seleccionar features con GA (Genetic Algorithm)

**Nota:** Los archivos grandes no se cargaron en este github.
- dataset limpio: https://drive.google.com/file/d/1kORPJxDHyV9wI_9HTpBnUC4Ozpz6FigP/view?usp=sharing
- dataset completo: https://drive.google.com/file/d/1EiDJ4LFZDFv_eX86dh821jkx_02_FaRI/view?usp=sharing
