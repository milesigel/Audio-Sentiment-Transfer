# Music-Sentiment-Transfer
University of Rochester 2021 Summer REU focusing on music sentiment transfer using CycleGAN

Poster: [Music Sentiment Transfer poster.pdf](https://github.com/milesigel/Audio-Sentiment-Transfer/files/7240114/Music.Sentiment.Transfer.poster.pdf)

Paper: [Music Sentiment Transfer.pdf](https://github.com/milesigel/Audio-Sentiment-Transfer/files/7240116/Music.Sentiment.Transfer.pdf)

Slides: [Music Sentiment Transfer.pptx](https://github.com/milesigel/Audio-Sentiment-Transfer/files/7240117/Music.Sentiment.Transfer.pptx)

For this project, we based our network on the CycleGAN framework for symbolic music created by Brunner et al. in thier paper [Symbolic Music Genre Transfer with CycleGAN](https://arxiv.org/pdf/1809.07575.pdf).

<img width="755" alt="Screen Shot 2021-07-28 at 11 04 29 AM" src="https://user-images.githubusercontent.com/64766743/127357063-3927e768-1eb4-4f91-80db-af7a1fb3b199.png">

The network we used was a [Pytorch implementation](https://github.com/Asthestarsfalll/Symbolic-Music-Genre-Transfer-with-CycleGAN-for-pytorch) written in 2021. After getting the code working, the results indicated that the GAN network was not able to generate the correct format neccessary for MIDI interpreters. On the other hand, the data processing pipeline we created, midi_to_npy.py was a valid mechansim for creating datasets that were fit for the network. The data format created by the file turns MIDI files into binary piano rolls such that the format is Time x MIDI notes. As for the results of the network, the npy files not run through the network were able to be successfuly convert back into midi files using utils from the Pytorch implementation we refrenced above. 

Other tools we created include the wav_splitter folder which is able to split wav files, possibly of long musical performences, into smaller segments. Additionally, the functions also include mechansims for transforming wav files into spectrograms using torchaudio and librosa.



