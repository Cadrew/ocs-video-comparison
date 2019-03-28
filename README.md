# OCS-Video-Comparison

This is a video comparison project using FFMPEG developped by Onii-ChanSub.

# How it Works

The script is only compatible with Windows.
The goal is to compare two videos using PSNR and MSE estimator.

It can compare videos in the following formats :
- MKV
- MP4
- MOV
- AVI
- MXF
- MPEG

Videos do not have to be in the same format to be compared. However, they must have the same resolution and the same aspect ratio.

## Prerequisites

You'll need Python 3.5 or higher to make this work.
You can download the latest Python version [here](https://www.python.org/downloads/windows/).

## Compare two videos

Open the project folder and use the following command in your CLI (Command Line Interface) :
```CLI
python ocs_comparison.py <input_video_1> <input_video_2>
```

By default, the *extract* argument is *no*, but if you want to extract all the images from the videos in the *images* folder just add *--extract=yes* :
```CLI
python ocs_comparison.py <input_video_1> <input_video_2> --extract=yes
```

Moreover, if you only want to extract images without run a PSNR comparison :
```CLI
python ocs_comparison.py <input_video_1> <input_video_2> --extract=yes --psnr=no
```

# TODO

- Add possibility to chose which report we want
- Add differents video comparison analysis (SSIM, VMAF...)
- Add Linux compatibility
- Add possibility to extract only wanted images from video
- Add GUI
- Add possibility to run on GPU to improve performance
- Test many video formats
- Test which python versions are compatible

