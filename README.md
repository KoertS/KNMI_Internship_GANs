# Nowcasting Precipitation using GANs

## GANs on MNIST
In [this folder](https://github.com/KoertS/KNMI_Internship_GANs/tree/main/dcgan_MNIST) I apply a conditional GAN to a hand written number dataset in order to gain some more experience with GANs and cGANs.

## GANs on Precipitation Data

[Here](https://github.com/KoertS/KNMI_Internship_GANs/tree/main/precipitation_forecasting) I work with the precipitation radar data. The real time (rtcor) data is matched with the Overreem data to create input output pairs. This is done in the [batchcreator](https://github.com/KoertS/KNMI_Internship_GANs/blob/main/precipitation_forecasting/batchcreator.py) module. 
The [model_builder](https://github.com/KoertS/KNMI_Internship_GANs/blob/main/precipitation_forecasting/model_builder.py) is used to create a model. Currently I implemented a GAN model that is based the paper from [Tian et al.](https://ieeexplore.ieee.org/abstract/document/8777193) on precipitation nowcasting. 
In [this](https://github.com/KoertS/KNMI_Internship_GANs/blob/main/precipitation_forecasting/testrun.ipynb) notebook I perform a test run to get an idea of the training time.

### Clutter

The find locations where clutter tends to happen, I looked at the probability that pixels exceed certain rain intensity thresholds.
#### rtcor dataset:
Prob > 0.3mm             |  Prob > 3.0mm  |        Prob > 30.0mm                
:-------------------------:|:-------------------------:|:---------------:|
![image](https://github.com/KoertS/KNMI_Internship_GANs/blob/main/precipitation_forecasting/figures/freq_above_03mm.png)  |  ![image](https://github.com/KoertS/KNMI_Internship_GANs/blob/main/precipitation_forecasting/figures/freq_above_3mm.png) |![image](https://github.com/KoertS/KNMI_Internship_GANs/blob/main/precipitation_forecasting/figures/freq_above_30mm.png)


#### Aart dataset:
Prob > 0.3mm             |  Prob > 3.0mm  |        Prob > 30.0mm                
:-------------------------:|:-------------------------:|:---------------:|
![image](https://github.com/KoertS/KNMI_Internship_GANs/blob/main/precipitation_forecasting/figures/aart_freq_above_03mm.png)  |  ![image](https://github.com/KoertS/KNMI_Internship_GANs/blob/main/precipitation_forecasting/figures/aart_freq_above_3mm.png) |![image](https://github.com/KoertS/KNMI_Internship_GANs/blob/main/precipitation_forecasting/figures/aart_freq_above_30mm.png)

An other way to detect clutter is by looking at the gradient of the radar image. Rainfall tends to gradually increase from low to high precipitation values, while clutter can lead to sudden increases and decreases in radar reflectively. However removing these spikes is not a straightforward procedure, as clouds can move through areas that contain clutter and occasionally clouds also contain high gradients. This makes it difficult to discard pixels based on the magnitude of their gradient. Below you can see an example of abnormal pixel detection. Pixels are seen as abnormal if their gradient magnitude is bigger than 500. The radar image shows all rainy pixels (>.3mm) in color.

Input (rainy pixels in color)  |  Detecting abnormal pixels  |             
:-------------------------:|:-------------------------:|
![image](https://github.com/KoertS/KNMI_Internship_GANs/blob/main/precipitation_forecasting/gif/july7.gif)  |  ![image](https://github.com/KoertS/KNMI_Internship_GANs/blob/main/precipitation_forecasting/gif/july7clutter.gif) |



## Paper
Work in progress of the paper I'm writing can be found in [overleaf](https://www.overleaf.com/read/nqbdxkjnnqyv).
