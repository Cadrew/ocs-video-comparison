# OCS-Video-Comparison

This is a video comparison project using FFMPEG developped by Onii-ChanSub.

# How it works

The script is only compatible with Windows.
The goal is to compare two videos using PSNR and MSE estimator.

It can compares videos in the following formats:
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

Open the project folder and use the following command in your CLI (Command Line Interface):
```CLI
python ocs_comparison.py <input_video_1> <input_video_2>
```

By default, the *extract* argument is *no*, but if you want to extract all the images from the videos in the *images* folder just add *--extract=yes*:
```CLI
python ocs_comparison.py <input_video_1> <input_video_2> --extract=yes
```

Moreover, if you only want to extract images without run a PSNR comparison:
```CLI
python ocs_comparison.py <input_video_1> <input_video_2> --extract=yes --psnr=no
```

## Output reports

Once the videos have been compared, you'll have four differents reports in your *output* folder.
- *psnr.log* : This is the original PSNR report. It might be difficult to read for uninitiated people.
- *output_psnr.log* : This is the same report but all irrelevant lines have been removed.
- *output_average.txt* : This is a summary of *output_psnr.log* report. It regroups all the relevant lines by average.
- *output_ass.ass* : This is a friendly report. Basically, it's the same that *output_average.txt* but in an ASS file in order to compare video directly with your own eyes where the script tells you there are differences.

## Read results

The most interesting value in the PSNR report is *mse_avg*. The more it's high, the more there is differences between the two videos.
The coefficent indicates the difference value frame by frame.
In the *output_average.txt* and *output_ass.ass* reports, you'll see results as following:
```
<first frame> -> <last frame> = <average mse_avg value> (min: <lower mse_avg value> at <frame with lower mse_avg value> - max: <higher mse_avg value> at <frame with higher mse_avg value>)
```
Each line represents a difference identified by the script. You can see details of this difference in the *output_psnr.log* report.

# TODO

There is more things to do in order to improve this project:
- Add possibility to chose which report we want
- Add differents video comparison analysis (SSIM, VMAF...)
- Add Linux compatibility
- Add possibility to extract only wanted images from video
- Add GUI
- Add possibility to run on GPU to improve performance
- Test many video formats
- Test which python versions are compatible

