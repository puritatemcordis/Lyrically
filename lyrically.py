import pytesseract
import os
import sys
from tqdm import tqdm
from pdf2image import convert_from_path

# removes hidden directories in Songs directory
def remove_hidden(directories):
    for directory in directories:
        name = str(directory)
        if name[0] == '.':
            directories.remove(directory)

# converts pdf to img and stores img to same directory
def convert_to_img(path):
    i = 0
    pages = convert_from_path(str(path))

    path = path.split('/')
    path.pop()
    path = '/'.join(path) + '/'

    for page in pages:
        page.save(path + 'img' + str(i) + '.jpg', 'JPEG')
        i += 1

# converts the lyrics from the img and appends to a .txt file
def convert_to_txt(path, first, language):
    result = pytesseract.image_to_string(str(path), lang=language)

    path = path.split('/')
    path.pop()
    path = '/'.join(path) + '/'

    # appends the result string to a file
    if first:
        f = open(path + "output.txt", "w+")
        f.write(str(result))
        f.close()
        first = False
    else:
        f = open(path + "output.txt", "a+")
        f.write(str(result))
        f.close()

# cleans .txt file from new lines and unordered words
def clean_txt(path):
    path = path.split('/')
    path.pop()
    path = '/'.join(path) + '/' + 'output.txt'

    # remove new lines and chords in list
    with open(path, 'r') as f:
        lines = []
        for line in f:
            # removes chords and 0 word lines
            i = 0
            word_count = 0
            for word in line.split():
                if not word.islower():
                    i += 1
                elif word == "":
                    continue
                word_count += 1
            # print(str(i))
            # print(str(word_count))
            if i == word_count:
                continue
            else:
                lines.append(line)

    line_num = 0  # var to determine new line based on number of stanzas in song
    is_num = True   # var to determine when appearance of numbers in stanza ends
    length = 0  # var to statically contain the number of stanzas
    i = 0   # var to determine index in line array
    misc = []

    # removes any lines with only one letter/word and appends them to misc
    for line in lines:
        word_arr = line.split()
        if len(word_arr) == 1:
            misc.append(line)
            lines.remove(line)

    # removes any misc lines
    for line in lines:
        if is_num and any(char.isdigit() for char in line):
            line_num += 1
        else:
            if is_num:
                length = line_num
            is_num = False

            word_arr = line.split()
            if len(word_arr[0]) == 1:
                misc.append(line)
                lines.remove(line)
                i += 1
                continue

            if line_num == length:
                lines[i] = '\r\n' + line
                line_num = 0
            else:
                line_num += 1
        i += 1

    # writes for the first line, appends for the rest of the lines
    first = True
    for line in lines:
        if first:
            f = open(path, 'w+')
            f.write(line)
            f.close()
            first = False
        else:
            f = open(path, 'a+')
            f.write(line)
            f.close()

    # appends misc lines at the end of the .txt file
    f = open(path, 'a+')
    f.write("\r\n\n" + "Misc lines:")
    for line in misc:
        f.write("\r\n" + line)
    f.close()

# main algorithm: traverses through subfolders to change the pdf --> jpg --> txt
def traverse_subf(directories, language):
    for directory in directories:
        # enters data set folder
        for folder in os.listdir(directory):
            # starts progress bar for folders in song directory -- will always be songs + 1 (.DSTORE)
            for counter in tqdm(range(len(os.listdir(directory)))):
                counter = 0
                # skips hidden directories
                name = str(folder)
                if name[0] == '.':
                    counter += 1
                    continue

                first = True  # var to determine whether to write or append

                # enters each song folder
                for file in os.listdir(directory + '/' + folder):
                    # skips hidden directories
                    name = str(file)
                    if name[0] == '.':
                        continue

                    path = directory + '/' + folder + '/' + file  # var to store path

                    # converts pages of pdf to images
                    name = file.split('.')
                    if name[1] == 'pdf':
                        convert_to_img(path)
                        # creates output file
                        path = path.split('/')
                        path.pop()
                        path = '/'.join(path) + '/' + 'output.txt'
                        f = open(path, 'w+')
                        f.close()
                    # translates the text on the image to a string
                    elif name[1] == 'jpg':
                        convert_to_txt(path, first, language)

                clean_txt(path)

def main():
    directories = next(os.walk('.'))[1]
    remove_hidden(directories)
    traverse_subf(directories, str(sys.argv[1]))

if __name__ == "__main__":
    main()