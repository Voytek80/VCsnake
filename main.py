import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import librosa
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from keras import models
from keras import layers
from keras.utils import to_categorical
from concurrent.futures import ThreadPoolExecutor
import audioop
import pyaudio
import wave
import snake2class
from threading import Thread
import keras



mfcc_number = 11
epochs_number = 250
silence_threshold = 500
fs = 22050


class Dataset:
    def __init__(self):
        self.direction_classes = 'lewo prawo gora dol ignoruj'.split()
        self.exit_classes = 'koniec jeszcze_raz ignoruj'.split()
        self.directions_data = []
        self.directions_data_set = []
        self.exit_data = []
        self.exit_data_set = []

    @staticmethod
    def create_data(classes):
        data = []
        data_set = []
        for c in classes:
            for filename in os.listdir(f'/Users/Voytek/Desktop/Programming/Python/keras_mfcc/Audio11025/{c}'):
                if filename.endswith('.wav'):
                    file_path = f'/Users/Voytek/Desktop/Programming/Python/keras_mfcc/Audio11025/{c}/{filename}'
                    y, sr = librosa.load(file_path, mono=True, duration=1)
                    data_to_append = Features.feature_extraction(y)
                    data_set_to_append = data_to_append, c
                    data.append(data_to_append)
                    data_set.append(data_set_to_append)
        return data, data_set


class Features:
    @staticmethod
    def feature_extraction(y):
        all_features = []
        mfcc = librosa.feature.mfcc(y=y, sr=fs, n_mfcc=mfcc_number, n_fft=662, n_mels=64)
        all_features = np.append(all_features, mfcc.flatten())
        return all_features

    @staticmethod
    def normalizing(datax):
        scaler = StandardScaler()
        X_normalized = scaler.fit_transform(np.array(datax, dtype=float))
        return X_normalized


class NeuralNetwork:
    def __init__(self):
        self.model = 0
        self.model1 = 0
        self.model2 = 0
        self.test_acc = 0

    def teaching_model(self, data_set, data, epochs_number, exit_neurons):
        class_list = []
        for count, i in enumerate(data_set):
            class_list.append(data_set[count][-1])
        encoder = LabelEncoder()
        input_labels = encoder.fit_transform(class_list)
        one_hot_encoded = to_categorical(input_labels)

        X_train, X_test, y_train, y_test = train_test_split(Features.normalizing(data), one_hot_encoded, test_size=0.2)
        self.model = models.Sequential()
        self.model.add(layers.Dense(64, activation='sigmoid', input_shape=(X_train.shape[1],)))
        self.model.add(layers.Dense(32, activation='sigmoid'))
        self.model.add(layers.Dense(exit_neurons, activation='sigmoid'))
        self.model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics="accuracy")
        self.model.fit(X_train, y_train, verbose=0, epochs=epochs_number, batch_size=128)
        test_loss, self.test_acc = self.model.evaluate(X_test, y_test)
        print('test_acc: ', self.test_acc)
        return self.model


class SoundRecognition:
    @staticmethod
    def sound_detection(silence_threshold=silence_threshold, chunk=1225, rate=fs):
        licznik = 0
        while not waz.exit_game:
            CHANNELS = 1
            FORMAT = pyaudio.paInt16
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=rate,
                            input=True,
                            output=False,
                            frames_per_buffer=chunk)
            frames = []
            prev_audio = []
            rms = 0
            while rms < silence_threshold:
                if waz.exit_game:
                    quit()
                prev_audio = stream.read(chunk)
                rms = audioop.rms(prev_audio, 2)
            frames.append(prev_audio)
            for i in range(8):
                sound_chunks = stream.read(chunk)
                frames.append(sound_chunks)

            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open(f'output{licznik}.wav', 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            y, sr = librosa.load(f'./output{licznik}.wav', mono=True, duration=1)

            if developer_mode:
                print(licznik, ' ', end="")
                licznik += 1

            executor = ThreadPoolExecutor(max_workers=3)
            if waz.game_close == False:
                executor.submit(SoundRecognition.predict_direction, y)
            else:
                executor.submit(SoundRecognition.predict_exit, y)

    @staticmethod
    def predict_direction(y):
        dane.directions_data.append(Features.feature_extraction(y))
        X = Features.normalizing(dane.directions_data)
        predictions = network.model1.predict(X, verbose=0)
        dane.directions_data.pop()
        z = np.argmax(predictions[-1])
        if predictions[-1][z] > 0.6:
            waz.global_direction= np.argmax(predictions[-1])
        if developer_mode:
            for count, value in enumerate(predictions[-1]):
                dir = [ 'dół', 'góra','background noise', 'lewo', 'prawo']
                if value > 0.9:
                    print('\x1b[6;30;42m' + f'{dir[count]}:' + '\x1b[0m', "%.3f" % value, end='  ')
                elif value > 0.6:
                    print('\x1b[5;37;43m' + f'{dir[count]}:' + '\x1b[0m', "%.3f" % value, end='  ')
                else:
                    print(f'{dir[count]}:', "{:.00}".format(value), end='  ')
            print()



    @staticmethod
    def predict_exit(y):
        dane.exit_data.append(Features.feature_extraction(y))
        X = Features.normalizing(dane.exit_data)
        predictions = network.model2.predict(X, verbose=0)
        dane.exit_data.pop()
        if predictions[-1][1] > 0.6:
            waz.once_more = True
        elif predictions[-1][2] > 0.6:
            waz.exit_game = True


if __name__ == "__main__":

    developer_mode = False

    dane = Dataset()
    dane.directions_data, dane.directions_data_set = dane.create_data(dane.direction_classes)
    dane.exit_data, dane.exit_data_set = dane.create_data(dane.exit_classes)


    network = NeuralNetwork()



    #network.model1 = network.teaching_model(dane.directions_data_set, dane.directions_data, epochs_number, 5)
    #network.model2 = network.teaching_model(dane.exit_data_set, dane.exit_data, epochs_number, 3)
    network.model1 = keras.models.load_model('/Users/Voytek/Desktop/Programming/Python/keras_mfcc/250_epochs_model1')
    network.model2 = keras.models.load_model('/Users/Voytek/Desktop/Programming/Python/keras_mfcc/250_epochs_model2')
    #network.model1.save('250_epochs_model1')
    #network.model2.save('250_epochs_model2')


    #print("Ilość próbek: ", len(dane.directions_data_set))
    #print("Ilość próbek2: ", len(dane.exit_data_set))
    input("Press any key to continue...")
    waz = snake2class.Snejk()
    thread = Thread(target=SoundRecognition.sound_detection)
    thread.start()
    waz.gameLoop()












