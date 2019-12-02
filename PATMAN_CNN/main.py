# -*- coding: utf-8 -*-
# @Author: Ben
# @Date:   2017-09-09 21:31:42
# @Last Modified by:   Ben
# @Last Modified time: 2017-09-11 20:41:12

import numpy as np
from tools.COLLECT_DATA import CollectData
from tools.TRAIN_MODEL import TrainModel
from tools.TEST_MODEL import TestModel

WINDOW_SIZE = (420, 420)
WIDTH = 80
HEIGHT = 80
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'inception3-1M-grey'
DATA_FOLDER = 'data/'

def main():
    print("#############################")
    print(" # PATMAN AI - Neural Network")
    print("#############################")
    print()

    running = True

    while running:
        choice = get_choice()

        if choice == "1":
            collect_data = CollectData(WINDOW_SIZE, DATA_FOLDER)
            collect_data.start()

        elif choice == "2":
            train_model = TrainModel(DATA_FOLDER, WIDTH, HEIGHT, LR, EPOCHS, MODEL_NAME)
            train_model.start()

        elif choice == "3":
            test_model = TestModel(WINDOW_SIZE, DATA_FOLDER, WIDTH, HEIGHT, LR, EPOCHS, MODEL_NAME)
            test_model.start()

        elif choice == "4":
            running = False

        else:
            continue

def get_choice():
    print("-----------------------------")
    print(" 1. Collect training data")
    print(" 2. Train model using existing data")
    print(" 3. Test trained model")
    print(" 4. Quit")
    print()
    choice = input("    Enter option: ")
    return choice

main()
# training_data = list(np.load('data/training_data_6.npy'))
# print(len(training_data))
# np.save('data/training_data_6.npy', training_data[:50000])
