# OCS-Video-Comparison

This is a video comparison project using FFMPEG developped by Onii-ChanSub.
It needs Python 3.5 or higher.

# How it Works

The script is only compatible with Windows.
The goal is to compare two videos using PSNR and MSE estimator.

It can compare video in the following formats :
- MKV
- MP4
- MOV
- AVI
- MXF
- MPEG

Videos do not have to be in the same format to be compared. However, they must have the same resolution and the same aspect ratio.

## Compare two videos

Open the project folder and use the following command in you CLI (Command Line Interface) :
```CLI
python ocs_comparison.py <input_video_1> <input_video_2>
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

