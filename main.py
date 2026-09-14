import os, sys 
import numpy as np 
import tensorflow as tf 
import matplotlib.pyplot as plt 
import keras
from keras import layers, models 
 
TRAIN_DIR = "data/train" 
TEST_DIR = "data/test" 
MODEL_FILE = "Blood_Sweat_Tears.h5" 
IMG_SIZE = (1024, 1024) 
BATCH_SIZE = int(input("Batch Size -> "))
EPOCHS = int(input("No. of Epochs -> ")) 
 
mode = input("What want to do -> [train/test] ").lower()   
 
if mode == "train": 
    train_data = keras.utils.image_dataset_from_directory( 
        TRAIN_DIR, image_size=IMG_SIZE, batch_size=BATCH_SIZE 
    ) 
    class_names = train_data.class_names 
    print("Classes:", class_names) 
 
    print("Model be training rn.") 
    model = models.Sequential([ 
        layers.Rescaling(1./255, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)), 
        layers.Conv2D(16, (3,3), activation='relu'), 
        layers.MaxPooling2D(), 
        layers.Conv2D(32, (3,3), activation='relu'), 
        layers.MaxPooling2D(), 
        layers.Flatten(), 
        layers.Dense(64, activation='relu'), 
        layers.Dense(len(class_names), activation='softmax') 
    ]) 
 
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy']) 
 
    model.fit(train_data, epochs=EPOCHS) 
    model.save(MODEL_FILE) 
    print("Model save file", MODEL_FILE) 
 
elif mode == "test": 
    if not os.path.exists(MODEL_FILE): 
        print("No model. You kill me.") 
        sys.exit(1) 
 
    print("Model be testing rn.") 
    test_data = tf.keras.utils.image_dataset_from_directory( 
        TEST_DIR, image_size=IMG_SIZE, batch_size=BATCH_SIZE 
    ) 
    class_names = test_data.class_names 
 
    model = tf.keras.models.load_model(MODEL_FILE) 
 
    loss, acc = model.evaluate(test_data) 
    print(f"Test Accuracy: {acc*100:.2f}%") 
 
    for images, labels in test_data.take(1): 
        predictions = model.predict(images) 
        for i in range(min(5, len(images))): 
            plt.imshow(images[i].numpy().astype("uint8")) 
            plt.title(f"Pred: {class_names[np.argmax(predictions[i])]} | True: {class_names[labels[i]]}") 
            plt.show() 
 
else: 
    print("error")