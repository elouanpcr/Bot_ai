from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

# Cargar el modelo una sola vez
MODEL = load_model("keras_model.h5", compile=False)

# Cargar etiquetas una sola vez
with open("labels.txt", "r", encoding="utf-8") as file:
    CLASS_NAMES = file.readlines()


def get_class(image_path):

    np.set_printoptions(suppress=True)

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open(image_path).convert("RGB")

    image = ImageOps.fit(
        image,
        (224, 224),
        Image.Resampling.LANCZOS
    )

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    data[0] = normalized_image_array

    prediction = MODEL.predict(data)

    index = np.argmax(prediction)

    class_name = CLASS_NAMES[index].strip()

    # Eliminar el número inicial de labels.txt
    class_name = class_name.split(" ", 1)[1]

    confidence_score = float(prediction[0][index])

    return class_name, confidence_score