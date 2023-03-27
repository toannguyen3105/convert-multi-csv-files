import glob, os
import csv
from datetime import datetime
from os import path

# Getting the current date and time
dt = datetime.now()
ts = datetime.timestamp(dt)
ts_int = int(ts)
KEY_RENAME = 'Commander'


def getfiles(dirpath):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a


def check_file(filePath):
    if path.exists(filePath):
        numb = 1
        while True:
            newPath = "{0}_{2}{1}".format(*path.splitext(filePath) + (numb,))
            if path.exists(newPath):
                numb += 1
            else:
                return newPath
    return filePath


def list_to_string(s):
    str1 = "+".join(s)
    str1 = str1.replace('//', '')
    return str1


def rename_file(new_name, folder, filename):
    dst = f"{new_name}.csv"
    dst = f"destination/{dst}"
    dst = check_file(dst)
    src = f"{folder}/{filename}"
    os.rename(src, dst)


def main():
    folder = "source"

    lst_files = glob.glob("*.csv")
    lst_files.sort(key=os.path.getmtime)

    for count, filename in enumerate(os.listdir(folder)):
        with open(f"{folder}/{filename}") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            count_commander = 0
            commander_name = []
            for row in csv_reader:
                if row[2] == KEY_RENAME:
                    count_commander += 1
                    commander_name.append(row[1])

        if count_commander == 1:
            rename_file(list_to_string(commander_name), folder, filename)
            print(f"Deck {filename} has 1 commander")
        elif count_commander == 0:
            print(f"Deck {filename} has no commander")
        else:
            rename_file(list_to_string(commander_name), folder, filename)
            print(f"Deck {filename} has more than 1 commander")

    print('All Files Renamed')
    print('New Names are')
    # verify the result
    res = os.listdir("destination")
    print(res)


if __name__ == '__main__':
    main()
