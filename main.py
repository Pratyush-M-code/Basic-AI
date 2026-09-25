import os, sys 
import csv
import numpy as np 
import tensorflow as tf 
import matplotlib.pyplot as plt 
import keras
from keras import layers, models 
import sklearn
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay


DIR = "Interstellar Objects" 
File =  str(input("Model File Name -> "))
MODEL_FILE = File + ".keras"

IMG_SIZE = (256, 256) 
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
    class_names = train_data.class_names
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

    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    print("Classes:", class_names) 
 
    print("Model be training rn.") 
    model = models.Sequential([
        layers.InputLayer(input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)), 
        layers.Rescaling(1./255),
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.2, fill_mode='nearest'),
        tf.keras.layers.RandomTranslation(0.2,0.2, fill_mode='nearest'),
        tf.keras.layers.RandomZoom(0.2, fill_mode='nearest'),
         
        layers.Conv2D(16, (3,3), activation='relu'), 
        layers.MaxPooling2D(),

        layers.Conv2D(32, (3,3), activation='relu'), 
        layers.MaxPooling2D(),

        layers.Conv2D(64, (3,3), activation='relu'), 
        layers.MaxPooling2D(),

        layers.Conv2D(64, (3,3), activation='relu'), 
        layers.MaxPooling2D(),  

        layers.GlobalAveragePooling2D(), 
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        
        layers.Dense(len(class_names), activation='softmax') ]) 
 
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy']) 
 
    history = model.fit(train_data,validation_data = validation_data, epochs=EPOCHS, callbacks=[early_stopping], verbose=1) 
    model.save(MODEL_FILE) 
    print("Model save file", MODEL_FILE) 

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    plt.plot(range(1, len(acc) + 1), acc, label='Training Accuracy')
    plt.plot(range(1, len(val_acc) + 1), val_acc, label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()
    plt.show()

    plt.plot(range(1, len(loss) + 1), loss, label='Training Loss')
    plt.plot(range(1, len(val_loss) + 1), val_loss, label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.show()

    csv_file = File + "_training_history.csv"

    with open(csv_file, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['Epoch', 'Training Accuracy', 'Validation Accuracy', 'Training Loss', 'Validation Loss'])
        for i in range(EPOCHS):
            writer.writerow([
                i + 1,
                acc[i], 
                val_acc[i], 
                loss[i], 
                val_loss[i]
            ])


 
elif mode == "test": 
    if not os.path.exists(MODEL_FILE): 
        print("No model.") 
        sys.exit(1) 
 
    print("Model be testing rn.") 
    test_data = tf.keras.utils.image_dataset_from_directory( 
        "Interstellar Objects Test", image_size=IMG_SIZE, batch_size=BATCH_SIZE, shuffle=False
    ) 
    class_names = test_data.class_names 
    model = tf.keras.models.load_model(MODEL_FILE) 
 
    loss, acc = model.evaluate(test_data) 
    print(f"Test Accuracy: {acc*100:.2f}%") 

    y_true,y_pred=[],[]
    for images,labels in test_data:
        predictions = model.predict(images, verbose=1)
        y_true.extend(labels.numpy())
        y_pred.extend(np.argmax(predictions, axis=1)) 
    y_true,y_pred=np.array(y_true),np.array(y_pred)

    print("Classification report")
    report = classification_report(y_true,y_pred,target_names=class_names)
    print(report)

    csv_file = File + "_testing_history.csv"

    report_dict = classification_report(y_true,y_pred,target_names=class_names,output_dict=True )
    with open(csv_file, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow/(["class", "precision", "recall", "f1-score", "support"])
        for label,metrics in report_dict.items():
            if isinstance(metrics,dict):
                writer.writerow([label, metrics["precision"], metrics["recall"], metrics["f1-score"], metrics["support"]])

    for images, labels in test_data.take(1): 
        predictions = model.predict(images) 
        for i in range(min(5, len(images))): 
            plt.imshow(images[i].numpy().astype("uint8")) 
            plt.title(f"Pred: {class_names[np.argmax(predictions[i])]} | True: {class_names[labels[i]]}") 
            plt.show() 
 
else: 
    print("error")