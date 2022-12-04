import glob
import os

import joblib
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.base import TransformerMixin

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pickle import load

import convert_csv
import warnings

warnings.filterwarnings('ignore')

'''

MoWA deep에서 학습시킨 Tensorflow model, scaler, encoding 등에 대해서 Load
새로운 CSI 데이터가 들어올 경우 model을 통해서 현재의 상태를 에측

'''

np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', '{:.4f}'.format)
np.seterr(divide='ignore')


class Standard_Scaler(TransformerMixin):
    def __init__(self, **kwargs):
        self._scaler = StandardScaler(copy=True, **kwargs)
        self._orig_shape = None

    def fit(self, X, **kwargs):
        X = np.array(X)
        # Save the original shape to reshape the flattened X later
        # back to its original shape
        if len(X.shape) > 1:
            self._orig_shape = X.shape[1:]
        X = self._flatten(X)
        self._scaler.fit(X, **kwargs)
        return self

    def transform(self, X, **kwargs):
        X = np.array(X)
        X = self._flatten(X)
        X = self._scaler.transform(X, **kwargs)
        X = self._reshape(X)
        return X

    def _flatten(self, X):
        # Reshape X to <= 2 dimensions
        if len(X.shape) > 2:
            n_dims = np.prod(self._orig_shape)
            X = X.reshape(-1, n_dims)
        return X

    def _reshape(self, X):
        # Reshape X back to it's original shape
        if len(X.shape) >= 2:
            X = X.reshape(-1, *self._orig_shape)
        return X


def reading_file(activity_csv):
    results = []
    for i in range(len(activity_csv)):
        df = pd.read_csv(activity_csv[i])
        results.append(df.values)
    return results


def print_value(prediction):
    if prediction == 0:
        return "Empty"
    elif prediction == 1:
        return "Lying"
    elif prediction == 2:
        return "Sitting"
    elif prediction == 3:
        return "Standing"
    elif prediction == 4:
        return "Walking"


print("---------------------------")
print("[Load Scaler and Encoding]")
print("---------------------------\n")

sc = joblib.load('./model/scaling_model/model_pickle3.pkl')
en = joblib.load('./model/encoding_model/model_pickle3.pkl')

# with open('./model/scaling_model/model_pickle2.pkl', 'rb') as f:
#     sc = load(f)
#
# with open('./model/encoding_model/model_pickle2.pkl', 'rb') as f:
#     en = load(f)

print("-----------------------------------")
print("[Load Scaler and Encoding complete]")
print("-----------------------------------\n")

print("------------")
print("[Load model]")
print("------------\n")

model = tf.keras.models.load_model(
    # "C:\\Users\\HOME\\Desktop\\Experiment-3\\Experiment-3\\Data\\model\\model_2022_09_21_18_14_23_97.09")
    "./model/model_2022_11_30_23_42_33_97.67")

print("---------------------")
print("[Load model complete]")
print("---------------------\n")


class Target:
    # watchDir = "D:\\MoWA\\data\\input\\pcap"
    watchDir = "../data/input/pcap"

    # watchDir에 감시하려는 디렉토리를 명시한다.
    def __init__(self):
        self.observer = Observer()  # observer객체를 만듦

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()


class Handler(FileSystemEventHandler):
    # FileSystemEventHandler 클래스를 상속받음.
    # 아래 핸들러들을 오버라이드 함

    def on_created(self, event):  # 파일, 디렉터리가 생성되면 실행
        Fname, Extension = os.path.splitext(os.path.basename(event.src_path))

        print("---------------------------------------")
        print("[Convert %s.csv]" % Fname)
        print("---------------------------------------\n")

        if os.path.getsize(event.src_path) >= 1:
            time.sleep(10)
        else:
            time.sleep(5)

        # convert_csv.generate_csv(  # Fname + ".pcap",
        #     "D:\\MoWA\\data\\input\\pcap\\" + Fname + ".pcap", "D:\\MoWA\\data\\input\\csv\\" + Fname + ".csv",
        #     'amplitude')
        convert_csv.generate_csv("../data/input/pcap/" + Fname + ".pcap",
                                 "../data/input/csv/" + Fname + ".csv",
                                 'amplitude')

        print("----------------------")
        print("[Convert csv complete]")
        print("----------------------\n")

        print("---------------------------------------")
        print("[Load %s.csv]" % Fname)
        print("---------------------------------------\n")

        # path = "D:\\MoWA\\data\\input\\csv"
        path = "../data/input/csv"
        os.chdir(path)
        list_file = glob.glob("*.csv")
        input_csv = [i for i in list_file]
        input = reading_file(input_csv)
        input = sc.transform(input)

        predictions = model.predict(input)
        print(predictions[0])

        print("Result : " + print_value(np.argmax(predictions[0])))

        print("-----------------------------------")
        print("[Delete prediction completion file]")
        print("-----------------------------------\n")

        os.system("del . /Q")


if __name__ == '__main__':  # 본 파일에서 실행될 때만 실행되도록 함

    w = Target()
    w.run()
