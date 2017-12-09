
# coding: utf-8

# In[1]:

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda
from keras.layers import Conv2D, MaxPool2D
from keras.layers import Cropping2D
from keras.layers import Dropout, BatchNormalization
from keras.callbacks import EarlyStopping
from keras import regularizers

import keras.backend as K
import matplotlib.pyplot as plt

import csv
import cv2
import numpy as np


# In[2]:

# data1: driving in the center of the lane
# data2: recovery laps
# data3: driving counter-clockwise

dirs = ['data1', 'data2', 'data3']

images = []
measurements = []

# Correction factor
correction = 0.2

def load_driving_log(dir_name):
    lines = []
    
    logfile = str(dir_name) + '/driving_log.csv'
    print(logfile)
    with open(logfile) as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            lines.append(line)
            
    for line in lines:
        steering_center = float(line[3])

        for i in range(3):
            source_path = line[i]
            filename = source_path.split('/')[-1]
#             print('filename:', filename)

            current_path = dir_name + '/IMG/' + filename
#             print(current_path)
            image = cv2.imread(current_path)
            images.append(image)
#     print(measurement)
            if i == 0:
                measurements.append(steering_center)
            elif i == 1:
                measurements.append(steering_center + correction)  # streering_left
            elif i == 2:
                measurements.append(steering_center - correction) # steering_right

for dirname in dirs:
    print(dirname)
    load_driving_log(dirname)


# In[3]:

len(images)


# In[4]:

# plt.figure(figsize=(15,5))
# plt.subplot(1, 3, 1)
# plt.imshow(images[1])
# plt.title('left')

# plt.subplot(1, 3, 2)
# plt.imshow(images[0])
# plt.title('center')

# plt.subplot(1, 3, 3)
# plt.imshow(images[2])
# plt.title('right')


# In[5]:

# cropImage = images[0].copy()


# In[6]:

# cropImage = cropImage[70:135,:]


# In[7]:

# plt.imshow(cropImage)


# In[8]:

# Data Augmentation - flip the images
augmented_images, augmented_measurements = [], []
for image, measurement in zip(images, measurements):
    augmented_images.append(image)
    augmented_measurements.append(measurement)
    # Flip the images
    augmented_images.append(cv2.flip(image, 1))
    # change the direction of the measurement
    augmented_measurements.append(measurement*-1.0)


# In[9]:

X_train = np.array(augmented_images)
y_train = np.array(augmented_measurements)


# In[10]:

X_train.shape


# In[11]:

y_train.shape


# In[12]:

# Reset the network
K.clear_session()

model = Sequential()
# normalize the input data

model.add(Lambda(lambda x: x / 255.0 - 0.5, input_shape=(160, 320, 3)))

# Cropping the top 70 top pixels and 25 bottom pixels.
model.add(Cropping2D(cropping=((70, 25), (0, 0))))

model.add(Conv2D(24, (5, 5), strides=(2, 2), activation='relu'))
model.add(Conv2D(36, (5, 5), strides=(2, 2), activation='relu'))
model.add(Conv2D(48, (5, 5), strides=(2, 2), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))


# In[13]:

model.summary()


# In[14]:

early_stop = EarlyStopping(monitor='loss', patience=1, verbose=1)
model.compile(loss='mse', optimizer='adam')
history_object = model.fit(X_train, y_train, validation_split=0.2, shuffle=True, epochs=30, callbacks=[early_stop])

model.save('model.h5')
print('Done.')


# In[15]:

# ### print the keys contained in the history object
# print(history_object.history.keys())


# # In[16]:

# ### plot the training and validation loss for each epoch
# plt.plot(history_object.history['loss'])
# plt.plot(history_object.history['val_loss'])
# plt.title('model mean squared error loss (Strides=(2,2), No Pooling, No Dropout)')
# plt.ylabel('mean squared error loss')
# plt.xlabel('epoch')
# plt.legend(['training set', 'validation set'], loc='lower left')
# plt.show()


# # In[17]:

# K.clear_session()

# model = Sequential()

# model.add(Lambda(lambda x: x / 255.0 - 0.5, input_shape=(160, 320, 3)))

# model.add(Cropping2D(cropping=((70, 25), (0, 0))))

# model.add(Conv2D(24, (5, 5), strides=(2, 2), activation='relu'))
# model.add(Dropout(0.3))

# model.add(Conv2D(36, (5, 5), strides=(2, 2), activation='relu'))
# # model.add(Dropout(0.3))

# model.add(Conv2D(48, (5, 5), strides=(2, 2), activation='relu'))
# model.add(Dropout(0.3))

# model.add(Conv2D(64, (3, 3), activation='relu'))
# # model.add(Dropout(0.3))

# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(Dropout(0.3))

# model.add(Flatten())

# model.add(Dense(100))
# model.add(Dropout(0.5))

# model.add(Dense(50))
# model.add(Dropout(0.5))

# model.add(Dense(10))
# model.add(Dense(1))


# # In[18]:

# model.summary()


# # In[19]:

# model.compile(loss='mse', optimizer='adam')
# history_object = model.fit(X_train, y_train, validation_split=0.2, shuffle=True, epochs=30)

# model.save('model-dropout.h5')
# print('Done.')


# # In[20]:

# ### plot the training and validation loss for each epoch
# plt.plot(history_object.history['loss'])
# plt.plot(history_object.history['val_loss'])
# plt.title('model mean squared error loss (with Dropout)')
# plt.ylabel('mean squared error loss')
# plt.xlabel('epoch')
# plt.legend(['training set', 'validation set'], loc='lower left')
# plt.show()


# # In[12]:

# # Reset the network
# K.clear_session()

# model = Sequential()
# # normalize the input data

# model.add(Lambda(lambda x: x / 255.0 - 0.5, input_shape=(160, 320, 3)))

# # Cropping the top 70 top pixels and 25 bottom pixels.
# model.add(Cropping2D(cropping=((70, 25), (0, 0))))

# # Color space
# model.add(Conv2D(3, (1, 1), activation='relu'))

# model.add(Conv2D(16, (3, 3), activation='relu'))
# # model.add(MaxPool2D(pool_size=(2,2)))
# model.add(Dropout(0.5))

# model.add(Conv2D(32, (5, 5), strides=(2, 2), activation='relu'))
# model.add(MaxPool2D(pool_size=(2,2)))
# model.add(Dropout(0.5))

# model.add(Conv2D(48, (3, 3), strides=(2, 2), activation='relu'))
# model.add(MaxPool2D(pool_size=(2,2)))
# model.add(Dropout(0.5))

# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(Dropout(0.5))


# model.add(Flatten())

# model.add(Dense(256))
# model.add(Dropout(0.5))

# model.add(Dense(128))
# model.add(Dropout(0.5))

# model.add(Dense(64))
# model.add(Dropout(0.5))

# model.add(Dense(8))

# model.add(Dense(1))


# # In[13]:

# model.summary()


# # In[14]:


# model.compile(loss='mse', optimizer='adam')
# history_object = model.fit(X_train, y_train, validation_split=0.2, shuffle=True, epochs=50)

# model.save('model-dropout-pooling.h5')
# print('Done.')


# # In[15]:

# ### plot the training and validation loss for each epoch
# plt.plot(history_object.history['loss'])
# plt.plot(history_object.history['val_loss'])
# plt.title('model mean squared error loss (with Dropout and Pooling)')
# plt.ylabel('mean squared error loss')
# plt.xlabel('epoch')
# plt.legend(['training set', 'validation set'], loc='lower left')
# plt.show()


# In[16]:

exit()


# In[ ]:



