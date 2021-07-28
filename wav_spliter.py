import os
import csv
import argparse
import sys
from pydub import AudioSegment


parser = argparse.ArgumentParser()
parser.add_argument('-sf', '--sound_file', type=str, required=False, help="path to soundfile")
parser.add_argument('-sd', "--save_dir", type=str, required=False, help="path to save dir")
parser.add_argument('-ss', '--sample_size', type=int, required=False, help="the size of each sample")
parser.add_argument('-cv', '--csv_save', type=bool, required=False, help="True if metadata")
parser.add_argument('-head', '--head', type=str, required=False, help="header to wav files")
parser.add_argument('-class', '--class_id', type=int, required=False, help="classID -- will default to 1")
parser.add_argument('-name', '--dataset_name', type=str, required=False, help="name of the dataset")
args = parser.parse_args()


def slice(sound_file, save_dir, sample_size=10, csv_save=True, head="sample", class_id=1, dataset_name=None,
          max_num=1000):
    """
    This funciton splits a sound file into a save directory where each new sound file is "sample_size" seconds long.
    If you want a csv_file that has that split file as well as its annotation based on class
    :param sound_file: location of sound file wanting to be split
    :param save_dir: location of save_dir for new sound files. Will be created if not there.
    :param sample_size: sample size of sound chunck
    :param csv_save: True if you want a CSV file
    :param head: the save name header for each file
    :param class_id: annotation for this sound file
    :param dataset_name: name of the dataset you want to create with that sound file
    :param max_num: max num of created chunks
    :return:
    """
    sound = AudioSegment.from_file(sound_file, format="wav")
    if not (dataset_name == None):
        folder = os.path.join(save_dir, dataset_name)
    else:
        folder = save_dir

    csv_save_dir = os.path.join(folder, "metadata")
    audio_save_dir = os.path.join(folder, "audio")

    # convert to seconds
    jump = sample_size * 1000
    start = 0
    end = jump
    num_samples = (len(sound) // jump)
    csv_file = []

    print("Creating folders...")

    if not os.path.isdir(folder):
        os.makedirs(folder)
        os.makedirs(audio_save_dir)
        if csv_save:
            os.makedirs(csv_save_dir)
    else:
        if not os.path.isdir(audio_save_dir):
            os.makedirs(audio_save_dir)
            if csv_save:
                os.makedirs(csv_save_dir)

    print("Splitting into samples...")

    for sample in range(num_samples - 1):
        if max_num == sample:
            break
        segment = sound[start:end]
        if len(segment) != jump:
            continue
        file_name = f"{head}_{sample}.wav"
        segment.export(os.path.join(audio_save_dir, file_name), format='wav')
        length = str(len(segment))
        row = [file_name, length, class_id]
        csv_file.append(row)
        start += jump
        end += jump
    if csv_save:
        print("Saving CSV...")
        with open(os.path.join(csv_save_dir, 'meta.csv'), 'w') as file:
            writer = csv.writer(file)
            writer.writerows(csv_file)
    print("Finished.")


class Audio_Dataset_Creator:
    """
    Class that makes the object that splits and saves the files.
    """

    def __init__(self, sound_path, data_path, csv_save=True, class_id=1, dataset_name=None, max_num=1000):
        self.sound_file = sound_path
        self.data_path = data_path
        self.sample_size = None
        self.csv_save = csv_save
        self.label = class_id
        self.dataset_name = dataset_name
        self.max_num = max_num

    def split_and_save(self, sample_size=10, head="sample"):
        slice(self.sound_file, self.data_path, sample_size=sample_size, csv_save=self.csv_save, head=head,
              class_id=self.label,
              dataset_name=self.dataset_name, max_num=self.max_num)


if __name__ == "__main__":
    # name of the data set
    dataset_name = "sad_set"
    # path to original sound file
    sound_file = "/Users/milessigel/Desktop/PycharmProjects/audio_dataset_creator/sad.wav"
    # where are the top level datasets saved
    save_dir = "/Users/milessigel/Desktop/Datasets"
    # class_id
    class_id = 1
    # header for the sample files
    head = "sample"
    # do you want CSV?
    csv_save = True
    # number of seconds of sample
    sample_size = 5

    max_num = 1000

    if len(sys.argv) > 1:
        splitter_w_args = Audio_Dataset_Creator(args.sound_file, args.save_dir,
                                        csv_save=args.csv_save if args.csv_save is not None else csv_save,
                                        class_id=args.class_id if args.class_id is not 1 else class_id,
                                        dataset_name=args.dataset_name if args.dataset_name is not None else dataset_name)
        splitter_w_args.split_and_save(sample_size=args.sample_size if args.sample_size is not 10 else sample_size,
                               head=args.head if args.head is not None else head)
        exit()
    else:
        splitter = Audio_Dataset_Creator(sound_file,
                                        save_dir,
                                        csv_save=csv_save,
                                        class_id=class_id,
                                        dataset_name=dataset_name,
                                        max_num=max_num)

        splitter.split_and_save(sample_size=sample_size,
                               head=head)
        exit()


