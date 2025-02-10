import tensorflow as tf
import numpy as np
from PIL import Image

# Параметры
img_height = 28
img_width = 28

# Загрузка модели
model = tf.keras.models.load_model('my_model.keras')

# Функции для загрузки и предсказания изображения
def load_image(filepath):
    img = Image.open(filepath).convert('L')
    img = img.resize((img_height, img_width))
    img = np.array(img)
    img = img / 255.0
    img = img.reshape(-1, img_height, img_width, 1)
    return img

def predict_digit(test_img):
    img = load_image(test_img)
    prediction = model.predict(img)
    # Определить класс (цифру) с наибольшей вероятностью. Вернуть наиболее вероятную цифру, предсказанную моделью
    return np.argmax(prediction)

# Пример использования
test_image = '4_2.png'
predicted_digit = predict_digit(test_image)

print(f'Цифра на изображении: {predicted_digit}')