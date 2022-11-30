import glob
import os

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


print("----------------")
print("[Load Scaler and Encoding]")
print("----------------\n")

with open('model/sc_model.pkl', 'rb') as f:
    sc = load(f)

with open('model/en_model.pkl', 'rb') as f:
    en = load(f)

print("-------------------------")
print("[Load Scaler and Encoding complete]")
print("-------------------------\n")

print("------------")
print("[Load model]")
print("------------\n")

model = tf.keras.models.load_model(
    # "C:\\Users\\HOME\\Desktop\\Experiment-3\\Experiment-3\\Data\\model\\model_2022_09_21_18_14_23_97.09")
    "../model_2022_09_21_18_14_23_97.09")

print("---------------------")
print("[Load model complete]")
print("---------------------\n")


class Target:
    # watchDir = "D:\\MoWA\\data\\input\\pcap"
    watchDir = "ftp://blue-sun.kro.kr:9002/data/input/pcap"

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
        convert_csv.generate_csv("ftp://blue-sun.kro.kr:9002/data/input/pcap/" + Fname + ".pcap",
                                 "ftp://blue-sun.kro.kr:9002/data/input/csv/" + Fname + ".csv",
                                 'amplitude')

        print("----------------------")
        print("[Convert csv complete]")
        print("----------------------\n")

        print("---------------------------------------")
        print("[Load %s.csv]" % Fname)
        print("---------------------------------------\n")

        path = "D:\\MoWA\\data\\input\\csv"
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
