import os
import re
import sys
import shutil
import subprocess
import platform

def usage():
    print("python " + sys.argv[0] + " <input_video_1> <input_video_2> [--psnr=yes/no][--mode=basic/accurate/report/extract/extract-report][--standard=<value>][--quality=<value>][--keep=yes/no]")

def psnr_comparison(input_video_1, input_video_2, report):
    if not os.path.exists("output"):
        os.mkdir("output")
    result = subprocess.Popen('ffmpeg -i "' + input_video_1 + '" -i "' + input_video_2 + '" -lavfi  psnr="output/' + report + '" -f null -', stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    result.communicate()

def get_psnr_report(filepath):
    try:
        with open(filepath, "r") as file:
            input = ""
            input += file.read().replace(" ",";")
            input = input.replace("n:","")
            input = input.replace("mse_avg:","")
            input = input.replace("mse_r:","")
            input = input.replace("mse_g:","")
            input = input.replace("mse_b:","")
            input = input.replace("mse_y:","")
            input = input.replace("mse_u:","")
            input = input.replace("mse_v:","")
            input = input.replace("psnr_avg:","")
            input = input.replace("psnr_y:","")
            input = input.replace("psnr_u:","")
            input = input.replace("psnr_v:","")
            input = input.replace("psnr_r:","")
            input = input.replace("psnr_g:","")
            input = input.replace("psnr_b:","")
            input = input.replace(";\n","\n")
            input = csv_to_array(input.split("\n"))    
            file.close()
            return input
    except IOError:
        print("Analysis failed!")
        print("Exiting...")
        sys.exit()

def extract_images(input_video, temp = False, time_ss = "", time_to = "", extract_path = ""):
    video_name = input_video.split(OS_SEPARATOR)[len(input_video.split(OS_SEPARATOR)) - 1]
    if not os.path.exists("images"):
        os.mkdir("images")
    if(temp):
        if not os.path.exists("images" + OS_SEPARATOR + "temp"):
            os.mkdir("images" + OS_SEPARATOR + "temp")
        if not os.path.exists("images" + OS_SEPARATOR + "temp" + OS_SEPARATOR + video_name.split(".")[0]):
            os.mkdir("images" + OS_SEPARATOR + "temp" + OS_SEPARATOR + video_name.split(".")[0])
        result = subprocess.Popen('ffmpeg -ss ' + time_ss + ' -to ' + time_to  + ' -i "' + input_video + '" "images' + OS_SEPARATOR + 'temp' + OS_SEPARATOR + video_name.split(".")[0] + OS_SEPARATOR + '%d.png"', stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        result.communicate()
    else:
        path = ""
        if not os.path.exists("images" + OS_SEPARATOR + video_name.split(".")[0]):
            os.mkdir("images" + OS_SEPARATOR + video_name.split(".")[0])
        if extract_path != "":
            for folder in extract_path.split(OS_SEPARATOR):
                path = path + OS_SEPARATOR + folder
                if not os.path.exists("images" + OS_SEPARATOR + video_name.split(".")[0] + path):
                    os.mkdir("images" + OS_SEPARATOR + video_name.split(".")[0] + path)
        print("Extracting images from " + video_name + "...")
        if(time_ss != "" and time_to != ""):
            result = subprocess.Popen('ffmpeg -ss ' + time_ss + ' -to ' + time_to  + ' -i "' + input_video + '" "images' + OS_SEPARATOR + video_name.split(".")[0] + path + OS_SEPARATOR + '%d.png"', stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
            result.communicate()
        else:
            result = subprocess.Popen('ffmpeg -i "' + input_video + '" "images' + OS_SEPARATOR + video_name.split(".")[0] + path + OS_SEPARATOR + '%d.png"', stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
            result.communicate()
        print("Done.")

def reduce_images(input_video, quality, keep = True, reduce_path = ""):
    video_name = input_video.split(OS_SEPARATOR)[len(input_video.split(OS_SEPARATOR)) - 1]
    processed = ""
    if(reduce_path != ""):
        reduce_path = reduce_path + OS_SEPARATOR
    if(not os.path.exists("images" + OS_SEPARATOR + video_name.split(".")[0] + OS_SEPARATOR + reduce_path + "processed") and keep):
        os.mkdir("images" + OS_SEPARATOR + video_name.split(".")[0] + OS_SEPARATOR + reduce_path + "processed")
    if(keep):
        processed = "processed"
    print("Reducing images quality from " + video_name + "...")
    result = subprocess.Popen('ffmpeg -i "images' + OS_SEPARATOR + video_name.split(".")[0] + OS_SEPARATOR + reduce_path + '%d.png" -q:v ' + str(quality) + ' "images' + OS_SEPARATOR + video_name.split(".")[0] + OS_SEPARATOR + reduce_path + processed + OS_SEPARATOR + '%d.jpg"', stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    result.communicate()
    if(not keep):
        result = subprocess.Popen('del "images' + OS_SEPARATOR + video_name.split(".")[0] + OS_SEPARATOR + reduce_path + '*.png"', stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        result.communicate()
    print("Done.")

def video_cut(input_video, value):
    video_name = input_video.split(OS_SEPARATOR)[len(input_video.split(OS_SEPARATOR)) - 1]
    if not os.path.exists("output"):
        os.mkdir("output")
    result = subprocess.Popen('ffmpeg -ss ' + str(value) + ' -i "' + input_video + '" -c:v libx264 -c:a aac "output' + OS_SEPARATOR + video_name.split(".")[0] + ' (adjusted).' + video_name.split(".")[len(video_name.split(".")) - 1] + '"', stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    result.communicate()
    return "output" + OS_SEPARATOR + video_name.split(".")[0] + " (adjusted)." + video_name.split(".")[len(video_name.split(".")) - 1]


def get_video_duration(input_video):
    cmd = 'ffprobe -i "{}" -show_entries format=duration -v quiet -of csv="p=0"'.format(input_video)
    output = subprocess.check_output(
        cmd,
        shell=True,
        stderr=subprocess.STDOUT
    )
    return float(output)

def get_video_number_of_frames(input_video):
    cmd = 'ffmpeg -i "{}" -map 0:v:0 -c copy -f null -'.format(input_video)
    output = subprocess.check_output(
        cmd,
        shell=True,
        stderr=subprocess.STDOUT
    )
    try:
        return int(str(output).split("frame=")[len(str(output).split("frame=")) - 1].split(" ")[0])
    except ValueError:
        return int(str(output).split("frame= ")[len(str(output).split("frame= ")) - 1].split(" ")[0])

def get_video_fps(input_video):
    cmd = 'ffprobe -v 0 -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate "{}"'.format(input_video)
    output = subprocess.check_output(
        cmd,
        shell=True,
        stderr=subprocess.STDOUT
    )
    return float(re.findall(r'\d+', str(output))[0]) / float(re.findall(r'\d+', str(output))[1])

def csv_to_array(lines):
    output = []
    for line in lines:
        if line != "":
            cols = line.split(";")
            output.append(cols)
    return output

def input_average(input):
    average = 0.0
    for x in range(0, len(input)):
        average += float(input[x][1])
    return average / len(input)

def average(array, input):
    average = 0.0
    for x in range(array[0] - 1, array[len(array) - 1] - 1):
        average += float(input[x][1])
    return average / len(array)

def average_on_ten(array, index):
    average, end = 0.0, index + 10
    if(len(array) - index <= 10):
        end = len(array)
    for j in range(index, end):
        average += float(array[j][1])
    return average / 10

def is_relevant(array, input, standard):
    if(average(array, input) >= standard):
        return True
    return False

def sort_number_string(a):
    a = a.split(OS_SEPARATOR)[len(a.split(OS_SEPARATOR)) - 1]
    return int(re.findall(r'\d+', a)[0])

def range_min(array, input):
    sub_input = input[array[0] - 1:array[len(array) - 1]]
    values = []
    for x in range(0, len(sub_input)):
        values.append(float(sub_input[x][1]))
    return [min(values), array[values.index(min(values))]]

def range_max(array, input):
    sub_input, values = input[array[0] - 1:array[len(array) - 1]], []
    for x in range(0, len(sub_input)):
        values.append(float(sub_input[x][1]))
    return [max(values), array[values.index(max(values))]]

def get_string_time_duration(total_frames, current_frame, duration, timelaps=0):
    hours, minutes, seconds = 0, 0, 0
    time = duration * current_frame / total_frames + timelaps
    hours = int(time / 3600)
    minutes = int((time / 3600 - hours) * 60)
    seconds = int(((time / 3600 - hours) * 60 - minutes) * 60)
    hours = ("0" + str(hours) if hours < 10 else str(hours))
    minutes = ("0" + str(minutes) if minutes < 10 else str(minutes))
    seconds = ("0" + str(seconds) if seconds < 10 else str(seconds))
    return [hours, minutes, seconds]

def get_string_time_fps(current_frame, fps, timelaps=0):
    hours, minutes, seconds = 0, 0, 0
    time = current_frame / fps + timelaps
    hours = int(time / 3600)
    minutes = int((time / 3600 - hours) * 60)
    seconds = int(((time / 3600 - hours) * 60 - minutes) * 60)
    hours = ("0" + str(hours) if hours < 10 else str(hours))
    minutes = ("0" + str(minutes) if minutes < 10 else str(minutes))
    seconds = ("0" + str(seconds) if seconds < 10 else str(seconds))
    return [hours, minutes, seconds]

def generate_output_average(input, output, name):
    if not os.path.exists("output"):
        os.mkdir("output")
    file = open("output" + OS_SEPARATOR + name,"w")
    for o in range(0, len(output)):
        file.write(str(output[o][0]) + " -> " \
            + str(output[o][len(output[o]) - 1]) \
            + " = " + str(average(output[o], input)) \
            + " (min: " + str(range_min(output[o], input)[0]) \
            + " at " + str(range_min(output[o], input)[1]) \
            + " - max: " + str(range_max(output[o], input)[0]) \
            + " at " + str(range_max(output[o], input)[1]) + ")\n")
    file.close()

def generate_output_ass(input, output, input_video, name):
    if not os.path.exists("output"):
        os.mkdir("output")
    file = open("output" + OS_SEPARATOR + name,"w")
    #duration = get_video_duration(input_video)
    #total_frames = get_video_number_of_frames(input_video)
    fps = get_video_fps(input_video)
    file.write("[Events]\n")
    for o in range(0, len(output)):
        file.write("Comment: 0," \
            + get_string_time_fps(output[o][0], fps)[0] + ":" + get_string_time_fps(output[o][0], fps)[1] + ":" + get_string_time_fps(output[o][0], fps)[2] + ".00," \
            + get_string_time_fps(output[o][len(output[o]) - 1], fps, 1)[0] + ":" + get_string_time_fps(output[o][len(output[o]) - 1], fps, 1)[1] + ":" + get_string_time_fps(output[o][len(output[o]) - 1], fps, 1)[2] + ".00," \
            + "Default,,0,0,0,," \
            + str(output[o][0]) + " -> " \
            + str(output[o][len(output[o]) - 1]) \
            + " = " + str(average(output[o], input)) \
            + " (min: " + str(range_min(output[o], input)[0]) \
            + " at " + str(range_min(output[o], input)[1]) \
            + " - max: " + str(range_max(output[o], input)[0]) \
            + " at " + str(range_max(output[o], input)[1]) + ")" \
            + "\n")
    file.close()

def generate_output_psnr(input, output, name):
    if not os.path.exists("output"):
        os.mkdir("output")
    file = open("output" + OS_SEPARATOR + name,"w")
    for o in range(0, len(output)):
        file.write("--" + str(o + 1) + "--\n")
        for p in range(output[o][0] - 1, output[o][len(output[o]) - 1]):            
            file.write("n:" + str(input[p][0]) \
                + " mse_avg:" + str(input[p][1]) \
                + " mse_y:" + str(input[p][2]) \
                + " mse_u:" + str(input[p][3]) \
                + " mse_v:" + str(input[p][4]) \
                + " psnr_avg:" + str(input[p][5]) \
                + " psnr_y:" + str(input[p][6]) \
                + " psnr_u:" + str(input[p][7]) \
                + " psnr_v:" + str(input[p][8]) \
                + "\n")
        file.write("\n")
    file.close()

def main(argv):
    if(len(argv) < 2):
        usage()
        sys.exit()
    video_one, video_two, arg_report = argv[0], argv[1], argv[2]
    psnr, mode = True, "basic"
    set_time_ss, set_time_to, time_set = "00:00:03.000", "00:00:05.000", False
    accepted_modes = ["basic", "accurate", "report", "extract", "extract-report"]
    quality, keep = 0, True
    psnr_standard = 70
    for opt in argv:
        if "--psnr" in opt:
            psnr = (True if len(argv) > 2 \
                and opt.split("--psnr=")[len(opt.split("--psnr=")) - 1] == "yes" \
                else False)
        elif "--mode" in opt:
            mode = opt.split("--mode=")[len(opt.split("--mode=")) - 1]
        elif "-ss" in opt:
            set_time_ss = argv[argv.index(opt) - len(argv) + 1]
            time_set = True
        elif "-to" in opt:
            set_time_to = argv[argv.index(opt) - len(argv) + 1]
        elif "--standard" in opt:
            psnr_standard = float(opt.split("--standard=")[len(opt.split("--standard=")) - 1])
        elif "--quality" in opt:
            quality = float(opt.split("--quality=")[len(opt.split("--quality=")) - 1])
        elif "--keep" in opt:
            keep = (True if len(argv) > 2 \
                and opt.split("--keep=")[len(opt.split("--keep=")) - 1] == "yes" \
                else False)
    
    if(mode not in accepted_modes):
        print("Indicated mode incorrect.")
        usage()
        sys.exit()

    if(mode == "extract"):
        psnr = False
        if(time_set):
            extract_images(video_one, False, set_time_ss, set_time_to)
            extract_images(video_two, False, set_time_ss, set_time_to)
        else:
            extract_images(video_one)
            extract_images(video_two)
        if(quality > 0):
            reduce_images(video_one, quality, keep)
            reduce_images(video_two, quality, keep)

    if(mode == "extract-report"):
        print("Extract Report Mode")
        psnr = False
        report_ss, report_to, report = "", "", ""
        try:
            with open(arg_report, "r") as file:
                report = file.read().split("\n")
        except IOError:
            print("Unable to open report!")
            print("Exiting...")
            sys.exit()
        differences = 0
        for line in report:
            if(len(line.split(",")) < 3):
                continue
            differences+=1
            report_ss = line.split(",")[1]
            report_to = line.split(",")[2]
            extract_images(video_one, False, report_ss, report_to, "diff" + str(differences))
            extract_images(video_two, False, report_ss, report_to, "diff" + str(differences))
            if(quality > 0):
                reduce_images(video_one, quality, keep, "diff" + str(differences))
                reduce_images(video_two, quality, keep, "diff" + str(differences))

    if(psnr):
        if(mode == "accurate"):
            print("Extracting sample...")
            extract_images(video_one, True, set_time_ss, set_time_to)
            extract_images(video_two, True, set_time_ss, set_time_to)
            print("Done.")
            
            video_one_name = video_one.split(OS_SEPARATOR)[len(video_one.split(OS_SEPARATOR)) - 1]
            video_two_name = video_two.split(OS_SEPARATOR)[len(video_two.split(OS_SEPARATOR)) - 1]
            path1 = "images" + OS_SEPARATOR + "temp" + OS_SEPARATOR + video_one_name.split(".")[0] + OS_SEPARATOR
            path2 = "images" + OS_SEPARATOR + "temp" + OS_SEPARATOR + video_two_name.split(".")[0] + OS_SEPARATOR
            if not os.path.exists(path1) or not os.path.exists(path2):
                print("Extracting failed.")
                sys.exit()

            files1, files2 = [], []
            for r, d, f in os.walk(path1):
                for file in f:
                    if '.png' in file:
                        files1.append(os.path.join(r, file))
                    
            for r, d, f in os.walk(path2):
                for file in f:
                    if '.png' in file:
                        files2.append(os.path.join(r, file))
            
            files1 = sorted(files1, key = sort_number_string)
            files2 = sorted(files2, key = sort_number_string)
            
            psnr_reports1, psnr_reports2, standard_range = [], [], (20 if 20 <= len(files1) else len(files1))
            print("Adjusting videos...")
            print("It may take some time.")
            for i in range(0, standard_range):
                input_psnr = []
                for j in range(0, standard_range):
                    if j+i >= len(files1) or not os.path.exists(files1[j+i]):
                        break
                    psnr_comparison(files1[j+i], files2[j], "psnr.log")
                    input_psnr.append(get_psnr_report("output" + OS_SEPARATOR + "psnr.log")[0])
                psnr_reports1.append(input_average(input_psnr))
            
            for i in range(0, standard_range):
                input_psnr = []
                for j in range(0, standard_range):
                    if j+i >= len(files2) or not os.path.exists(files2[j+i]):
                        break
                    psnr_comparison(files1[j], files2[j+i], "psnr.log")
                    input_psnr.append(get_psnr_report("output" + OS_SEPARATOR + "psnr.log")[0])
                psnr_reports2.append(input_average(input_psnr))
            print("Done.")

            if(float(min(psnr_reports1)) < float(min(psnr_reports2))):
                print("Cutting " + video_one_name + "...")
                fps = get_video_fps(video_one)
                video_one = video_cut(video_one, float((psnr_reports1.index(min(psnr_reports1))) / fps))
                print("Done.")
            elif(float(min(psnr_reports1)) > float(min(psnr_reports2))):
                print("Cutting " + video_two_name + "...")
                fps = get_video_fps(video_two)
                video_two = video_cut(video_two, float((psnr_reports2.index(min(psnr_reports2))) / fps))
                print("Done.")
            shutil.rmtree('images' + OS_SEPARATOR + 'temp', ignore_errors=True)

        if(mode == "report"):
            input_psnr = get_psnr_report(arg_report)
        else:
            print("PSNR Comparison in progress...")
            psnr_comparison(video_one, video_two, "psnr.log")
            print("Done.")
            input_psnr = get_psnr_report("output" + OS_SEPARATOR + "psnr.log")

        output, comp = [], []
        for i in range(0, len(input_psnr)):
            if(average_on_ten(input_psnr, i) > psnr_standard):
                comp.append(i + 1)
            elif(comp and is_relevant(comp, input_psnr, psnr_standard)):
                output.append(comp)
                comp = []
            else:
                comp = []

        print("Number of differences: " + str(len(output)))
        generate_output_average(input_psnr, output, "output_average_" + str(psnr_standard) + ".txt")
        generate_output_ass(input_psnr, output, video_one, "output_ass_" + str(psnr_standard) + ".ass")
        generate_output_psnr(input_psnr, output, "output_psnr_" + str(psnr_standard) + ".log")

OS_SEPARATOR = "\\"
if(platform.system() == "Linux"):
    OS_SEPARATOR = "/"
if __name__ == "__main__":
    main(sys.argv[1:])
