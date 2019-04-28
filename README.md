# OCS Video Comparison

This is a video comparison project using FFMPEG.

# How it works

The script works on Windows and Linux.
The goal is to compare two videos using PSNR and MSE estimator.

It can compare videos in the following formats:
- MKV
- MP4
- MOV
- AVI
- MXF
- MPEG

Videos do not have to be in the same format to be compared. However, they must have the same resolution and the same aspect ratio. It's better that both videos have the same framerate to avoid potential image shifts in the comparison.

## Prerequisites

You'll need Python 3.5 or higher to make this work.
You can download the latest Python version [here](https://www.python.org/downloads/windows/).

On Linux, you'll need to install ffmpeg:
```CLI
sudo apt-get install ffmpeg
```

## Compare two videos

Open the project folder and use the following command in your CLI (Command Line Interface):
```CLI
python ocs_comparison.py <input_video_1> <input_video_2>
```

To run a more precise comparison:
```CLI
python ocs_comparison.py <input_video_1> <input_video_2> --mode=accurate
```
It will be longer than a basic comparison.
You can determine a sample with:
```CLI
python ocs_comparison.py <input_video_1> <input_video_2> --mode=accurate -ss 00:10:02.000 -to 00:10:05.000
```

Moreover, if you want to extract images without running a PSNR comparison:
```CLI
python ocs_comparison.py <input_video_1> <input_video_2> --mode=extract
```
You can extract only a sample:
```CLI
python ocs_comparison.py <input_video_1> <input_video_2> --mode=extract -ss 00:10:02.000 -to 00:10:05.000
```

You can generate new reports with new tolerance value if you have an original psnr report without runing a comparison:
```CLI
python ocs_comparison.py <input_video_1> <input_video_2> <input_report> --mode=report --standard=<value>
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

## Build

Install pyinstaller:
```CLI
pip install pyinstaller
```
If you're working on Windows, you'll need to install [PyWin32](https://github.com/mhammond/pywin32/releases)

Then run:
```CLI
pyinstaller --onefile ocs_comparison.py
```

# TODO

There is more things to do in order to improve this project:
- Add possibility to chose which report we want
- Add a detailed description of the possible results
- Add a friendlier report with only appreciations and not values
- Add differents video comparison analysis (SSIM, VMAF...)
- Test many video formats
- Test which python versions are compatible

