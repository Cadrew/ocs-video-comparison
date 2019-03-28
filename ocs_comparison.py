import os
import sys
import subprocess

def usage():
    print("python " + sys.argv[0] + " <input_video_1> <input_video_2> [--psnr=yes/no][--extract=yes/no]")

def psnr_comparison(input_video_1, input_video_2, report):
    if not os.path.exists("output"):
        os.mkdir("output")
    print("PSNR Comparison in progress...")
    print("It may take some time.")
    result = subprocess.Popen('ffmpeg -i "' + input_video_1 + '" -i "' + input_video_2 + '" -lavfi  psnr="output/' + report + '" -f null -', stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    result.communicate()
    print("Done.")

def get_psnr_report(filename):
    try:
        with open("output\\" + filename, "r") as file:
            input = ""
            input += file.read().replace(" ",";")
            input = input.replace("n:","")
            input = input.replace("mse_avg:","")
            input = input.replace("mse_y:","")
            input = input.replace("mse_u:","")
            input = input.replace("mse_v:","")
            input = input.replace("psnr_avg:","")
            input = input.replace("psnr_y:","")
            input = input.replace("psnr_u:","")
            input = input.replace("psnr_v:","")
            input = input.replace(";\n","\n")
            input = csv_to_array(input.split("\n"))    
            file.close()
            return input
    except IOError:
        print("PSNR Comparison failed!")
        print("Exiting...")
        sys.exit()

def extract_images(input_video):
    video_name = input_video.split("\\")[len(input_video.split("\\")) - 1]
    if not os.path.exists("images"):
        os.mkdir("images")
    if not os.path.exists("images\\" + video_name.split(".")[0]):
        os.mkdir("images\\" + video_name.split(".")[0])
    print("Extracting all images from " + video_name + "...")
    print("It may take a long time. Go get some coffee.")
    result = subprocess.Popen('ffmpeg -i "' + input_video + '" "images\\' + video_name.split(".")[0] + '\\%d.png"', stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    result.communicate()
    print("Done.")

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
    return int(str(output).split("frame=")[len(str(output).split("frame=")) - 1].split(" ")[0])

def csv_to_array(lines):
    output = []
    for line in lines:
        if line != "":
            cols = line.split(";")
            output.append(cols)
    return output

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

def is_relevant(array, input):
    if(average(array, input) >= 70):
        return True
    return False

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

def get_string_time(total_frames, current_frame, duration, timelaps=0):
    hours, minutes, seconds = 0, 0, 0
    time = duration * current_frame / total_frames + timelaps
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
    file = open("output\\" + name,"w")
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
    file = open("output\\" + name,"w")
    duration = get_video_duration(input_video)
    total_frames = get_video_number_of_frames(input_video)
    file.write("[Events]\n")
    for o in range(0, len(output)):
        file.write("Comment: 0," \
            + get_string_time(total_frames, output[o][0], duration)[0] + ":" + get_string_time(total_frames, output[o][0], duration)[1] + ":" + get_string_time(total_frames, output[o][0], duration)[2] + ".00," \
            + get_string_time(total_frames, output[o][len(output[o]) - 1], duration, 1)[0] + ":" + get_string_time(total_frames, output[o][len(output[o]) - 1], duration, 1)[1] + ":" + get_string_time(total_frames, output[o][len(output[o]) - 1], duration, 1)[2] + ".00," \
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
    file = open("output\\" + name,"w")
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
    video_one, video_two = argv[0], argv[1]
    psnr, extract = True, False
    for opt in argv:
        if "--extract" in opt:
            extract = (True if len(argv) > 2 \
                and opt.split("--extract=")[len(opt.split("--extract=")) - 1] == "yes" \
                else False)
        elif "--psnr" in opt:
            psnr = (True if len(argv) > 2 \
                and opt.split("--psnr=")[len(opt.split("--psnr=")) - 1] == "yes" \
                else False)
    
    if(psnr):
        psnr_comparison(video_one, video_two, "psnr.log")
        input = get_psnr_report("psnr.log")
        output, comp = [], []
        psnr_standard = 70
        for i in range(0, len(input)):
            if(average_on_ten(input, i) > psnr_standard):
                comp.append(i + 1)
            elif(comp and is_relevant(comp, input)):
                output.append(comp)
                comp = []
            else:
                comp = []

        print("Number of differences: " + str(len(output)))
        generate_output_average(input, output, "output_average.txt")
        generate_output_ass(input, output, video_one, "output_ass.ass")
        generate_output_psnr(input, output, "output_psnr.log")

    if(extract):
        extract_images(video_one)
        extract_images(video_two)

if __name__ == "__main__":
    main(sys.argv[1:])
