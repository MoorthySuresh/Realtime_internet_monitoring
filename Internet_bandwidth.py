import psutil
from matplotlib import pyplot as plt
import datetime
import time
from urllib.request import urlopen
import sys
from multiprocessing import Process


def plotting():
    fig = plt.figure()
    x, y, y1 = [], [], []
    fig.show()
    plt.plot(x, y, color="r", label="upload")
    plt.plot(x, y1, color="b", label="download")
    plt.xlabel("Time (HH:MM:SS)")
    plt.ylabel("data downloaded/data uploaded per second")
    plt.legend(loc="upper right")

    while True:
        # monitoing uploaded/downloaded data in 1 second interval
        i = datetime.datetime.now()
        upload_0 = (psutil.net_io_counters().bytes_sent / 10 ** 6)
        download_0 = (psutil.net_io_counters().bytes_recv / 10 ** 6)
        time.sleep(1)  #
        upload_1 = (psutil.net_io_counters().bytes_sent / 10 ** 6)
        download_1 = (psutil.net_io_counters().bytes_recv / 10 ** 6)
        diff_upload = (upload_1 - upload_0)
        diff_download = (download_1 - download_0)
        x.append(i)
        y.append(diff_upload)
        y1.append(diff_download)
        plt.plot(x, y, color="r", label="upload")
        plt.plot(x, y1, color="b", label="download")
        fig.canvas.draw()
        fig.savefig('2line plot.jpg', bbox_inches='tight', dpi=150)


def is_available():
    try:
        urlopen("https://www.google.com/", timeout=1)
        return True
    except:
        return False
        # print("Internet Connection unavailable at:", datetime.now())


# print(is_available())

Time1 = datetime.datetime.now()
Prog_Start_Time = str(Time1).split(".")[0]
initial_upload = psutil.net_io_counters().bytes_sent / (10 ** 6)
initial_download = psutil.net_io_counters().bytes_recv / (10 ** 6)


def check():
    Time1 = datetime.datetime.now()
    Prog_Start_Time = str(Time1).split(".")[0]
    print("Prog_Start_Time :", Prog_Start_Time)
    initial_upload = psutil.net_io_counters().bytes_sent / (10 ** 6)
    initial_download = psutil.net_io_counters().bytes_recv / (10 ** 6)
    with open("i_mon.txt", "w") as f:
        f.write("Programe started at : " + Prog_Start_Time)
        f.write("\n")
    while True:
        if is_available():
            # print("avaialble")
            pass

        else:
            # Record observed time when internet connectivity fails.
            Fail_Time = datetime.datetime.now()
            status = "----Internet Connection unavailable at : " + str(Fail_Time).split(".")[0]
            print(status)
            with open("i_mon.txt", "a") as f:
                f.write(status)
                f.write("\n")

            counter = 0
            while not is_available():
                time.sleep(1)
                counter += 1
                # if internet is not alive more than 1 hour, you can exit the program manually if you wish
                if counter >= 60:
                    counter = 0
                    now = datetime.datetime.now()
                    status = "------------------------Internet Connection still unavailable at : " + \
                             str(now).split(".")[0]
                    print(status)
                    with open("i_mon.txt", "a") as f:
                        f.write(status)
                        f.write("\n")
                    # print('Do you want to kill the program? ')
                    # print("press :", 'n- to continue', 'y- to Stop')
                    # choice = input("enter your n or y")
                    # if choice == 'n':
                    # pass
                    # elif choice == 'y':
                    # sys.exit()
            reconnect_time = datetime.datetime.now()
            reconnect_msg = "-------Internet Connection reconnected at    : " + str(reconnect_time).split(".")[0]
            print(reconnect_msg)
            with open("i_mon.txt", "a") as f:
                f.write(reconnect_msg)
                f.write("\n")


def data():
    i = 0
    Time1 = datetime.datetime.now()
    Prog_Start_Time = str(Time1).split(".")[0]
    # print("Prog_Start_Time :", Prog_Start_Time)
    while True:
        time.sleep(1)
        final_upload = (psutil.net_io_counters().bytes_sent / 10 ** 6)
        final_download = (psutil.net_io_counters().bytes_recv / 10 ** 6)
        Time2 = datetime.datetime.now()
        Prog_end_Time = str(Time2).split(".")[0]
        # print(Prog_end_Time)
        Time_duration = str(Time2 - Time1).split(".")[0]
        total_download = str(final_download - initial_download)
        total_upload = str(final_upload - initial_upload)
        with open("i_data.txt", "w") as f:
            f.write("Prog_Start_Time: ")
            f.write(Prog_Start_Time)
            f.write("\n")
            f.write("[total_download] = ")
            f.write(total_download)
            f.write("MB; [Time_duration] = ")
            f.write(Time_duration)
            f.write("\n")
            f.write("[total_upload] = ")
            f.write(total_upload)
            f.write("MB; [Time_duration] = ")
            f.write(Time_duration)
            f.write("\n")
            f.write("Prog_end_Time: ")
            f.write(Prog_end_Time)
        i += 1
    Time2 = datetime.datetime.now()
    Prog_end_Time = str(Time2).split(".")[0]
    # print(Prog_end_Time)


if __name__ == '__main__':
    Process(target=plotting).start()
    Process(target=check).start()
    Process(target=data).start()
