import os, sys 
import numpy as np 
import tensorflow as tf 
import matplotlib.pyplot as plt 
import keras
from keras import layers, models 
 
DIR = "Interstellar Objects" 
MODEL_FILE = "Blood_Sweat_Tears.h5" 

IMG_SIZE = (512, 512) 
BATCH_SIZE = int(input("Batch Size -> "))
EPOCHS = int(input("No. of Epochs -> ")) 
 
mode = input("What want to do -> [train/test] ").lower()   
 
if mode == "train": 

    train_data = keras.utils.image_dataset_from_directory( 
        DIR,
        validation_split=0.2,
        subset="training",
        shuffle=True,
        seed=110, 
        image_size=IMG_SIZE, 
        batch_size=BATCH_SIZE 
    )
    train_data = (train_data.cache().prefetch(tf.data.AUTOTUNE))
    validation_data = keras.utils.image_dataset_from_directory( 
            DIR,
            validation_split=0.2,
            subset="validation",
            shuffle=True,
            seed=110, 
            image_size=IMG_SIZE, 
            batch_size=BATCH_SIZE 
        )  
    validation_data = (validation_data.cache().prefetch(tf.data.AUTOTUNE))

    class_names = train_data.class_names 
    print("Classes:", class_names) 
 
    print("Model be training rn.") 
    model = models.Sequential([ 
        layers.Rescaling(1./255, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
         
        layers.Conv2D(16, (3,3), activation='relu'), 
        layers.MaxPooling2D(),

        layers.Conv2D(32, (3,3), activation='relu'), 
        layers.MaxPooling2D(),

        layers.Conv2D(64, (3,3), activation='relu'), 
        layers.MaxPooling2D(),

        layers.Conv2D(64, (3,3), activation='relu'), 
        layers.MaxPooling2D(),  

        layers.Flatten(), 
        layers.Dense(64, activation='relu'), 
        layers.Dense(len(class_names), activation='softmax') 
    ]) 
 
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy']) 
 
    history = model.fit(train_data,validation_data = validation_data, epochs=EPOCHS, verbose=2) 
    model.save(MODEL_FILE) 
    print("Model save file", MODEL_FILE) 

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    plt.plot(range(1, EPOCHS + 1), acc, label='Training Accuracy')
    plt.plot(range(1, EPOCHS + 1), val_acc, label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()
    plt.show()
 
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