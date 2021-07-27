import glob
import os
import random
import pypianoroll
import numpy as np
from music21 import *
import pandas as pd
import shutil

"""
This program is able to take a MIDI dataset along with a csv file that cotains annotations and turn them into 
(64, 84, 1) npy arrays that represent a section of the midi file. The dataset used is the VGMIDI dataset that contains 
valence and arousal labels. This implementation splits the data into two binary classes based on valence.

dataset found here: https://github.com/lucasnfe/vgmidi
"""


class Midi_to_Npy():

    def __init__(self, midi_path, csv_path, new_dataset_path):
        """
        midi_path = the full path to the midi dataset
        csv_path = full path to the csv file
        new_dataset_path = path to new location of dataset npy files

        """
        self.midi_path = midi_path
        self.csv_path = csv_path
        self.new_dataset_path = new_dataset_path
        os.makedirs(self.new_dataset_path) if not os.path.isdir(self.new_dataset_path) else None
        self.song_data = None
        self.rolls = None
        self.splits = None

    def load_midi(self):
        """
        load midi files into array
        """
        song_array = glob.glob(os.path.join(self.midi_path, "**/*.mid"), recursive=True)
        self.song_data = song_array
        print("midi files have been loaded into array")

    def clean_midi(self):
        """
        clean midi by turning midi into single track midi files and making it binary (note on/note off) values
        """
        self.rolls = []
        for i, song in enumerate(self.song_data):
            # create music 21 object
            tracks = pypianoroll.read(song).set_resolution(16).binarize()
            single_track_roll = tracks.blend('sum')
            self.rolls.append([single_track_roll, song])
        print("rolls have been saved!")

    def split_roll(self):
        """
        split dataset into rolls
        """
        time = 64
        split = []
        print("splitting dataset into array of snips")
        for roll, name in self.rolls:
            song = {"song": name, "snips": []}
            for i in range(len(roll) // time):
                section = roll[i * time:(i + 1) * time, 24:108]
                section = np.expand_dims(section, axis=2)
                song["snips"].append(section)
            split.append(song)
        self.splits = split

    def save_rolls(self):
        """
        This function saves the npy arrays to directory

        prints out "Complete" if the files were saved
        """
        fields = ["id", "series", "console", "game", "piece", "midi", "valence", "arousal"]
        csv = pd.read_csv(self.csv_path, usecols=fields)
        pieces = (list(csv.midi))
        pieces = [word.split("/")[-1] for word in pieces]
        print(f"saving {len(self.splits)} into shorter sequences")
        print()
        os.makedirs(f"{self.new_dataset_path}/happy") if not os.path.isdir(f"{self.new_dataset_path}/happy") else None
        os.makedirs(f"{self.new_dataset_path}/sad") if not os.path.isdir(f"{self.new_dataset_path}/sad") else None
        for song in self.splits:
            name = song["song"]
            splits = name.split("/")
            name = splits[-1]
            clips = song["snips"]
            index = pieces.index(name)
            positive = True if csv.iloc[index][6] == 1 else False
            for i in range(len(clips)):
                if positive:
                    np.save(f"{self.new_dataset_path}/happy/{name}_{i}", clips[i])
                else:
                    np.save(f"{self.new_dataset_path}/sad/{name}_{i}", clips[i])

    def reduce(self, path, count, new_path="reduced"):
        """
        downsample a directory down into smaller number of npy files
        :param path: path to reduce files in
        :param count: num of files to downsample to
        :param new_path: new save path
        :return: no return
        """
        os.makedirs(os.path.join(self.new_dataset_path, new_path)) if not os.path.isdir(os.path.join(self.new_dataset_path, new_path)) else None
        files = glob.glob(path + "/*.*")
        print(f"turning {len(files)} into {count}")
        sample = random.sample(files, count)
        for s in sample:
            shutil.copyfile(s, os.path.join(os.path.join(self.new_dataset_path, new_path), s.split("/")[-1]))
        print("Finished downsample")

    def join(self, first, second, new_path="combined"):
        os.makedirs(os.path.join(self.new_dataset_path, new_path)) if not os.path.isdir(os.path.join(self.new_dataset_path, new_path)) else None
        first_files = glob.glob(os.path.join(first, "*.*"))
        second_files = glob.glob(os.path.join(second, "*.*"))
        assert len(first_files) == len(second_files)
        print(f"joining directories in {new_path}")
        for i in range(len(first_files)):
            shutil.copyfile(first_files[i], os.path.join(self.new_dataset_path, new_path, first_files[i].split("/")[-1]))
            shutil.copyfile(second_files[i], os.path.join(self.new_dataset_path, new_path, second_files[i].split("/")[-1]))
        print("Finished joining files")

    def save(self):
        """
        Will save the dataset in the wanted new_dataset location
        """
        self.load_midi()
        self.clean_midi()
        self.split_roll()
        self.save_rolls()
        print("finished save!")



if __name__ == '__main__':
    MIDI_PATH = "/Users/milessigel/Desktop/PycharmProjects/Audio-Sentiment-Transfer/phrases"
    CSV_PATH = "/Users/milessigel/Desktop/PycharmProjects/Audio-Sentiment-Transfer/vgmidi_labelled.csv"
    NEW_PATH = "/Users/milessigel/Desktop/PycharmProjects/Audio-Sentiment-Transfer/new"
    converter = Midi_to_Npy(midi_path=MIDI_PATH, csv_path=CSV_PATH, new_dataset_path=NEW_PATH)
    converter.save()


