# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 20:33:08 2020

@author: André Desktop
"""

from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plt
import wave

samplerate = 44100
permisibleCharacter=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']
noteWaveCounter=0
ChordWaveCounter=0
def get_piano_notes():
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    base_freq = 261.63 #Frequency of Note C4
    
    note_freqs = {octave[i]: base_freq * pow(2,(i/12)) for i in range(len(octave))}        
    note_freqs[''] = 0.0
    
    return note_freqs
    
def get_wave(freq, duration=0.5):
    global noteWaveCounter
    noteWaveCounter+=1
    amplitude = 4096
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    
    plt.plot(wave[0:800])
    plt.xlabel("Tiempo[ms]")
    plt.ylabel("Amplitud")
    plt.title("Frecuencia: "+str(freq))
    plt.savefig('GraficaDeNotas/note#'+str(noteWaveCounter))
    plt.show()
    return wave
    
    
def get_song_data(music_notes):
    note_freqs = get_piano_notes()
    song = [get_wave(note_freqs[note]) for note in music_notes.split('-')]
    song = np.concatenate(song)
    return song.astype(np.int16)
    
def get_chord_data(chords):
    global ChordWaveCounter
    chords = chords.split('-')
    note_freqs = get_piano_notes()
    chord_data = []
    for chord in chords:
        ChordWaveCounter+=1
        data = sum([get_wave(note_freqs[note]) for note in list(chord)])
        chord_data.append(data)
        plt.plot(data[0:2000])
        plt.xlabel("Tiempo[ms]")
        plt.ylabel("Amplitud")
        plt.title("Acorde: "+str(chord))
        plt.savefig('GraficaAcordes/Acorde'+str(noteWaveCounter))
        plt.show()
    chord_data = np.concatenate(chord_data, axis=0)    
    return chord_data.astype(np.int16)

def get_note_assigner(character):
    switcher={
        'A':'a',
        'B':'A',
        'C':'B',
        'D':'c',
        'E':'C',
        'F':'d',
        'G':'D',
        'H':'E',
        'I':'F',
        'J':'f',
        'K':'G',
        'L':'g',
        'M':'a',
        'N':'A',
        'Ñ':'B',
        'O':'c',
        'P':'C',
        'Q':'d',
        'R':'D',
        'S':'E',
        'T':'F',
        'U':'f',
        'V':'G',
        'W':'g',
        'X':'a',
        'Y':'A',
        'Z':'B'
        }
    return switcher.get(character,"")
f=open("texto.txt","r")
string=f.read()
notes=[]
exportingNotes=""
exportingChords=""
f.close()
print(string)
string=string.upper()
print(string)
chordCounter=0
chords=[]
for character in range(len(string)):
    for letras in range(len(permisibleCharacter)):
        if string[character]==permisibleCharacter[letras]:
            notes.append(get_note_assigner(string[character]))
            chords.append(get_note_assigner(string[character]))
            chordCounter+=1
            if (character!=len(string)-1):
                notes.append("-")
                if chordCounter==3:
                    chords.append("-")
                    chordCounter=0
print(notes)
exportingNotes=exportingNotes.join(notes)
exportingChords=exportingChords.join(chords)
print(exportingNotes)   
print(exportingChords)
data = get_song_data(exportingNotes)
data = data * (16300/np.max(data))
write('notasIndividuales.wav', samplerate, data.astype(np.int16))
data = get_chord_data(exportingChords)
data = data * (16300/np.max(data))
data = np.resize(data, (len(data)*5,))
write('acordificado.wav', samplerate, data.astype(np.int16))

wav_file = wave.open("acordificado.wav",'r')

signal = wav_file.readframes(-1)
if wav_file.getsampwidth() == 1:
    signal = np.array(np.frombuffer(signal, dtype='UInt8')-128, dtype='Int8')
elif wav_file.getsampwidth() == 2:
    signal = np.frombuffer(signal, dtype='Int16')
else:
    raise RuntimeError("Unsupported sample width")


deinterleaved = [signal[idx::wav_file.getnchannels()] for idx in range(wav_file.getnchannels())]


fs = wav_file.getframerate()
Time=np.linspace(0, len(signal)/wav_file.getnchannels()/fs, num=int (len(signal)/wav_file.getnchannels()))
plt.figure(figsize=(50,3))

plt.figure(1)

plt.title('Señal')
for channel in deinterleaved:
    plt.plot(Time,channel, linewidth=.125)
#don't need to show, just save
#plt.show()
plt.savefig('acordificado', dpi=150)

plt.clf()

wav_file2 = wave.open("notasIndividuales.wav",'r')

signal = wav_file2.readframes(-1)
if wav_file2.getsampwidth() == 1:
    signal = np.array(np.frombuffer(signal, dtype='UInt8')-128, dtype='Int8')
elif wav_file2.getsampwidth() == 2:
    signal = np.frombuffer(signal, dtype='Int16')
else:
    raise RuntimeError("Unsupported sample width")


deinterleaved = [signal[idx::wav_file2.getnchannels()] for idx in range(wav_file2.getnchannels())]


fs = wav_file2.getframerate()
Time=np.linspace(0, len(signal)/wav_file2.getnchannels()/fs, num=int (len(signal)/wav_file2.getnchannels()))
plt.figure(figsize=(50,3))

plt.figure(1)

plt.title('Señal')
for channel in deinterleaved:
    plt.plot(Time,channel, linewidth=.125)
#don't need to show, just save
#plt.show()
plt.savefig('notasIndividuales', dpi=150)




