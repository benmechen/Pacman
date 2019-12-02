# -*- coding: utf-8 -*-
# @Author: Ben
# @Date:   2017-10-30 12:18:57
# @Last Modified by:   Ben
# @Last Modified time: 2017-12-20 22:42:50

import numpy as np
import subprocess
import pickle
import os
import atexit
from PIL import Image
import cv2
import keyboard
import tensorflow as tf
import tflearn


class DQN:
    def __init__(self):
        pass



def exit(file, pipe, proc):
    proc.kill()
    pipe.close
    os.remove(file)

def preprocess(screen):
    screen = np.array(screen, dtype='uint8').reshape((screen.size[1],screen.size[0],4))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 80))
    screen = screen.astype(np.float).ravel()
    return screen

def checkIfPipeOpen(lastiter):
    pipe = open("PAT.pipe", "rb")
    try:
        pipeval = pickle.loads(pipe.read())
    except:
        pipe.close()
        return False
    if not pipeval[0] > lastiter:
        pipe.close()
        return False
    pipe.close()
    return True

def environment(lastiter, action):
    pipe = open("PAT.pipe", "rb")
    try:
        pipeval = pickle.loads(pipe.read())
    except:
        pipe.close()
        return False
    if pipeval[0] > lastiter:
        keyboard.release('up')
        keyboard.release('down')
        keyboard.release('left')
        keyboard.release('right')
        if action == 0:
            keyboard.press('up')
        elif action == 1:
            keyboard.press('down')
        elif action == 2:
            keyboard.press('left')
        elif action == 3:
            keyboard.press('right')

        done = pipeval[2]
        reward = pipeval[1]
        lastiter = pipeval[0]
        print("PIPE:", pipeval)
    else:
        pipe.close()
        return False
    pipe.close()

    os.system("screencapture -R0,45,420,420 temp.png")
    screen = Image.open("temp.png")
    os.unlink('temp.png')
    
    return screen, done, reward, lastiter


proc = subprocess.Popen("exec python3 PATMAN.py", stdout=subprocess.PIPE, shell=True)

open("PAT.pipe", "w").write('')

exists = False
while not exists:
    if os.path.isfile("PAT.pipe"):
        exists = True


H = 200
BATCH_SIZE = 10
LR = 1e-4
GAMMA = 0.99
DECAY = 0.99
D = 80 * 80
# args = argparse.ArgumentParser("Reinforcement AI Pacman learning agent")
# args.add_argument("-r", help="Restore from saved model (True or False)", type=bool, default=False)
RESUME = True

os.system("screencapture -R0,45,420,420 temp.png")
screen = Image.open("temp.png")
os.unlink('temp.png')

if RESUME:
    print(" >> Restoring model from saved file")
    model = pickle.load(open('save.p', 'rb'))
else:
    model = {}
    model['W1'] = np.random.randn(H,D) / np.sqrt(D)
    model['W2'] = np.random.randn(H) / np.sqrt(H)

grad_buffer = { k : np.zeros_like(v, dtype='float64') for k,v in model.items() }
rmsprop_cache = { k : np.zeros_like(v) for k,v in model.items() }

prev_x = None
xs, hs, dlogps, drs = [], [] ,[], []
running_reward = None
reward_sum = 0
episode_number = 0

lastiter = -1
i = 0
nextiter = True
while True:
    if checkIfPipeOpen(lastiter):
        cur_x = preprocess(screen)
        if not prev_x is None:
            x = cur_x - prev_x
        else:
            x = np.zeros(D)

        prev_x = cur_x
        aprob, h = policy_forward(x)
        if np.random.uniform() < aprob:
            if np.random.uniform() < aprob:
                action = 1
            else:
                action = 2
        else:
            if np.random.uniform() < aprob:
                action = 3
            else:
                action = 4

        xs.append(x)
        hs.append(h)
        if action == 1:
            y = 1
        elif action == 2:
            y = 0.75
        elif action == 3:
            y = 0.5
        elif action == 4:
            y = 0.25
        else:
            y = 0

        dlogps.append(y - aprob)

        env = environment(lastiter, action)
        if not env == False:
            screen, done, reward, lastiter = env
            nextiter = True
        else:
            nextiter = False
            continue

        reward_sum += reward
        drs.append(reward)

        if i > 1 and done:
            try:
                episode_number += 1

                epx = np.vstack(xs)
                eph = np.vstack(hs)
                epdlogp = np.vstack(dlogps)
                epr = np.vstack(drs)
                xs, hs, dlogps, drs = [], [], [], []

                discounted_epr = discount_rewards(epr)
                discounted_epr -= np.mean(discounted_epr)
                discounted_epr /= np.std(discounted_epr)

                if not epdlogp.shape == discounted_epr.shape:
                    if epdlogp.shape > discounted_epr.shape:
                        diff = epdlogp.shape[0] - discounted_epr.shape[0]
                        for n in range(diff):
                            epdlogp = np.delete(epdlogp, n)
                    else:
                        diff = discounted_epr.shape[0] - epdlogp.shape[0]
                        discounted_epr = discounted_epr.reshape(epdlogp.shape)
                        for n in range(diff):
                            discounted_epr = np.delete(discounted_epr, n+1)

                epdlogp = np.multiply(epdlogp, discounted_epr)
                grad = policy_backward(eph, epdlogp)
                for k in model:
                    grad_buffer[k] = np.add(grad_buffer[k], grad[k])

                if episode_number % BATCH_SIZE == 0:
                    for k, v in model.items():
                        g = grad_buffer[k]
                        rmsprop_cache[k] = DECAY * rmsprop_cache[k] + (1 - DECAY) * g**2
                        model[k] += LR * g / (np.sqrt(rmsprop_cache[k]) + 1e-5)
                        grad_buffer[k] = np.zeros_like(v)

                if running_reward is None:
                    running_reward = reward_sum
                else:
                    running_reward = running_reward * 0.99 + reward_sum * 0.01

                print(" >> Episode reward total:", reward_sum, "running mean:", running_reward, "iteration:", i)
                
                reward_sum = 0
                prev_x = 0

                pickle.dump(model, open('save.p', 'wb'))
            except Exception as e:
                print(" >> Backprob error:", e)
                pass
        i += 1


atexit.register(exit, "PAT.pipe", pipe, proc)
