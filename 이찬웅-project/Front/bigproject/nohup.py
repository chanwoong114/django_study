import sys
import os
import sqlite3
import time

from os import listdir
from os.path import isfile, join, exists
import librosa
import librosa.display
import matplotlib.pyplot as plt
from IPython.display import Audio
import random
import numpy as np
import pandas as pd
import math
import pickle
import pathlib
import shutil

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *

from midiutil.MidiFile import MIDIFile
from music21.tempo import MetronomeMark
from music21.note import Note, Rest
from music21.stream import Stream
from music21 import metadata
from music21 import instrument
from music21 import midi 
from music21.key import Key
import music21



path = './'
sr = 22050
frameSize = 2406
randomRange = 4 # 노트 랜덤 생성시 최대 몇 노트를 이용해서 생성(너무 크면 음이 깨짐)
trimRight = int(round(3003 * pow(2, randomRange / 12) + 3))
minNoteNumber = 1 # 음 번호의 최솟값
maxNoteNumber = 88 # 음 번호의 최댓값
hop_length = 512

# only returns int
def getHalfFrequency(pitch:int) -> int:
    return int(round(11025 / (440 * pow(2, (pitch - 49) / 12))))
def getFrequency(pitch:int) -> int:
    return int(round(22050 / (440 * pow(2, (pitch - 49) / 12))))
def generateDatasetFor(x, target, y=None):
    freq = getHalfFrequency(target)
    retx = []
    rety = []
    for xi in x:
        a = []
        i = 0
        while i + freq <= len(xi):
            a.append(xi[i:i+freq])
            i += freq
        retx.append(np.array(a).reshape((len(xi) // freq, freq, 1)))
    if y == None:
        return retx
    for yi in y:
        rety.append(yi[target - 1])
    return retx, rety

def hop_to_duration(hop):
    global tempo
    sec = hop * hop_length / sr # duration 몇초인가
    quarter_per_sec = tempo / 60 # 초당 1/4이 몇번있는가
    return round(sec * quarter_per_sec * 4)

print('loading models...')
ma_piano = [None] * 128
files = [f for f in listdir(path + "model") if isfile(join(path + "model", f))]
for f in files:
    dot = f.find('.')
    if dot >= 0 and f[dot+1:] == 'h5':
        num = int(f[1:dot])
        ma_piano[num] = tf.keras.models.load_model(path + "model/" + f)
        
ma_guitar = [None] * 128
files = [f for f in listdir(path + "model_guitar") if isfile(join(path + "model_guitar", f))]
for f in files:
    dot = f.find('.')
    if dot >= 0 and f[dot+1:] == 'h5':
        num = int(f[1:dot])
        ma_guitar[num] = tf.keras.models.load_model(path + "model_guitar/" + f)

ma_violin = [None] * 128
files = [f for f in listdir(path + "model_violin") if isfile(join(path + "model_violin", f))]
for f in files:
    dot = f.find('.')
    if dot >= 0 and f[dot+1:] == 'h5':
        num = int(f[1:dot])
        ma_violin[num] = tf.keras.models.load_model(path + "model_violin/" + f)

print('loading models... end')

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
while True:
    time.sleep(12)
    e = cur.execute('select * from result_result where status=1 or status=2')
    f = cur.fetchall()
    
    if len(f) == 0:
        continue

    col = [column[0] for column in e.description].index('file')
    fileName = f[0][col]

    col = [column[0] for column in e.description].index('instrument')
    instrument = f[0][col]

    if instrument == 1:
        ma = ma_piano
    elif instrument == 2:
        ma = ma_guitar
    elif instrument == 3:
        ma = ma_violin

    # 진행중인 파일 status = 2
    cur.execute('update result_result set status=2 where file="' + fileName + '"')
    conn.commit()
    
    print(fileName + ' reading...')

    try:
        y, sr = librosa.load('media/' + fileName)
        y = librosa.resample(y, orig_sr=sr, target_sr=22050)
    except:
        cur.execute('update result_result set status=4 where file="' + fileName + '"')
        conn.commit()
        continue
    sr = 22050

    od = librosa.onset.onset_detect(y=y, sr=sr, hop_length=512)
    odp = 6
    # Estimate Tempo
    tempo, beats=librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
    tempo=int(2*round(tempo/2))
    mm = MetronomeMark(referent='quarter', number=tempo)

    # Estimate Tempo
    tempo, beats=librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
    mm = MetronomeMark(referent='quarter', number=tempo)
    #print(tempo)

    raw = []
    rawPrev = []
    for o in od:
        if o*512+2406 < len(y):
            ty = y[o*512-1:o*512+2406] # 2407개
            if len(ty) < 2407:
                ty += [0] * (2407 - len(ty))
            
            # 표준화 스케일링 비스무리
            if min(ty) != max(ty):
                s = 1 / np.std(ty)
                for i in range(len(ty)):
                    ty[i] *= s * 0.9
        
            i = len(ty) - 1
            while i >= 1:
                ty[i] -= ty[i-1]
                i -= 1
        
            raw.append(ty[1:])
        
            ty = y[(o - odp) * 512 - 1:(o - odp) * 512 + 2406]
            if len(ty) == 0:
                ty = [0] * 2407
            elif len(ty) < 2407:
                ty += [0] * (2407 - len(ty))
            
            if min(ty) != max(ty):
                for i in range(len(ty)):
                    ty[i] *= s
                
            i = len(ty) - 1
            while i >= 1:
                ty[i] -= ty[i-1]
                i -= 1
        
            rawPrev.append(ty[1:])

    print('predicting...')
    result = [[]]
    resultPrev = [[]]
    for i in range(1, 89):
        if ma[i] != None:
            x = generateDatasetFor(raw, i)
            pred = ma[i].predict(np.array(x), verbose=0)
            result.append(np.array(pred).reshape((-1)))
            x = generateDatasetFor(rawPrev, i)
            pred = ma[i].predict(np.array(x), verbose=0)
            resultPrev.append(np.array(pred).reshape((-1)))
        else:
            result.append([])
            resultPrev.append([])
    
    resultStream = []
    for oi in range(len(od)):
        a = []
        for i in range(1, 89):
            if ma[i] == None:
                continue
            if result[i][oi] > 0.9 and resultPrev[i][oi] < result[i][oi]:
                a.append(i)
        resultStream.append(a)

    leftHands = []
    rightHands = []

    od = np.append(od, np.array([od[-1] + 4]), axis=0)
    for ri in range(len(resultStream)):
        duration = hop_to_duration(od[ri+1] - od[ri])
        left = []
        right = []
        for rj in range(len(resultStream[ri])):
            if resultStream[ri][rj] < 40 and instrument == 1:
                left.append(resultStream[ri][rj])
            else:
                right.append(resultStream[ri][rj])
        leftHands.append([left, duration])
        rightHands.append([right, duration])
        
    # create your MIDI object
    mf = MIDIFile(2)     # only 2 track
    track = 0   # the only track

    firstFrame = od[0]
    ntime = 0
    mf.addTrackName(track, ntime, "Sample Track")
    mf.addTempo(track, ntime, tempo)

    # add some notes
    channel = 0
    volume = 100
    
    ntime = 0
    for i in range(len(leftHands)):
        for j in leftHands[i][0]:
            mf.addNote(1, 0, j + 20, ntime / 4, leftHands[i][1] / 4, volume)
        ntime += leftHands[i][1]

    ntime = 0
    for i in range(len(rightHands)):
        for j in rightHands[i][0]:
            mf.addNote(0, 0, j + 20, ntime / 4, rightHands[i][1] / 4, volume)
        ntime += rightHands[i][1]

    od = od[:-1]

    # write it to disk
    try:
        with open("media/" + fileName + ".mid", 'wb') as outf:
            mf.writeFile(outf)
    except:
        cur.execute('update result_result set status=4 where file="' + fileName + '"')
        conn.commit()
        continue
    print('writing to file...')
    '''
    synthesis = []
    for oi in range(len(od)):
        for rj in resultStream[oi]:
            if od[oi] * hop_length + len(notes[rj]) >= len(synthesis):
                synthesis += [0] * (od[oi] * hop_length + len(notes[rj]) - len(synthesis) + 1000)
            i = 0
            while i < len(notes[rj]):
                synthesis[od[oi] * hop_length + i] += notes[rj][i]
                i += 1
    display(Audio(synthesis, rate=sr))
    plt.plot(synthesis)
    plt.show()
    '''


    # 이거 반드시 설정 필요
    #us = music21.environment.UserSettings()
    #us['debug'] = 0
    #us['musescoreDirectPNGPath'] = 'C:\\Users\\clrmt\\Desktop\\bigproject\\big-project\\Front\\bigproject\\bin\\MuseScore3.exe'
    #us['musicxmlPath'] = 'C:\\Users\\clrmt\\Desktop\\bigproject\\big-project\\Front\\bigproject\\bin\\MuseScore3.exe'
    #us['musicxmlPath'] = 'C:/Program Files/MuseScore 3/bin' # '내가 설치한 MuseScore 3.exe path ( 대부분 programfiles -> MuseScore3 -> bin 안에 있음 )'
    #us['musescoreDirectPNGPath'] = 'C:/Program Files/MuseScore 3/bin' # '내가 설치한 MuseScore 3.exe path ( 대부분 programfiles -> MuseScore3 -> bin 안에 있음 )'
    #us['midiPath'] = 'C:\\Users\\clrmt\\Desktop\\bigproject\\big-project\\Front\\bigproject'
    #us['graphicsPath'] = 'C:\\Users\\clrmt\\Desktop\\bigproject\\big-project\\Front\\bigproject'
    #us['pdfPath'] = 'C:\\Users\\clrmt\\Desktop\\bigproject\\big-project\\Front\\bigproject'
    #us['vectorPath'] = 'C:\\Users\\clrmt\\Desktop\\bigproject\\big-project\\Front\\bigproject'
    #us['braillePath'] = 'C:\\Users\\clrmt\\Desktop\\bigproject\\big-project\\Front\\bigproject'
    #

    score = music21.converter.parse('media/' + fileName + '.mid')
    pngFilePath = str(score.write('musicxml.png'))
    shutil.copy(pngFilePath, "media/" + fileName + '-1.png')

    dot = pngFilePath.find('.')
    for i in range(2, 16):
        nextFile = pngFilePath[:dot - 1] + str(i) + '.png'
        #print(nextFile)
        if exists(nextFile):
            shutil.copy(nextFile, "media/" + fileName + "-" + str(i) + '.png')
            #print("media/" + fileName + "-" + str(i) + '.png')
    
    #print(pngFilePath)

    # 진행완료 파일 status = 3
    cur.execute('update result_result set status=3 where file="' + fileName + '"')
    conn.commit()
