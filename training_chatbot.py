import spacy
import json
import pickle
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from keras.optimizers.schedules import ExponentialDecay
import random

# Carga el modelo de español de SpaCy
print("Cargando modelo SpaCy...")
nlp = spacy.load('es_core_news_sm')

# Carga el archivo JSON de intenciones
print("Cargando archivo de intenciones...")
with open('intents_spanish.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)

words = []
classes = []
documents = []
ignore_words = ['?', '!', '.', ',']

# Procesa cada intención y sus patrones
print("Procesando intenciones y patrones...")
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokeniza y lematiza las palabras en cada patrón usando SpaCy
        doc = nlp(pattern)
        w = [token.lemma_.lower() for token in doc if token.text not in ignore_words]
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

print("Lematización y tokenización completada.")
print(f"Palabras: {words}")
print(f"Clases: {classes}")

words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Guarda las listas de palabras y clases en archivos pickle
print("Guardando listas en archivos pickle...")
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

print("Creando conjunto de entrenamiento...")
for doc in documents:
    bag = []
    pattern_words = doc[0]
    for word in words:
        bag.append(1) if word in pattern_words else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

print("Mezclando conjunto de entrenamiento...")
random.shuffle(training)

train_x = [row[0] for row in training]
train_y = [row[1] for row in training]

train_x = np.array(train_x)
train_y = np.array(train_y)

print("Creando modelo de red neuronal...")
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

lr_schedule = ExponentialDecay(
    initial_learning_rate=0.01,
    decay_steps=10000,
    decay_rate=0.9
)

sgd = SGD(learning_rate=lr_schedule, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

print("Entrenando modelo...")
hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

print("Guardando modelo...")
model.save('chatbot_model.h5', hist)

print("Modelo creado")