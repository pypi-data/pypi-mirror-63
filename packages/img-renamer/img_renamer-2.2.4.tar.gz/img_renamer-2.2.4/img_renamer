#!/usr/bin/env python
from os import path
from os import listdir
from os import rename as osrename
from sys import argv
from getopt import getopt
from getopt import GetoptError
from re import search

"""
Renamer is a command line interface for renaming images in numberic order.
"""

# Variables
yes = False
log = False
nro = 0
zeroes = 7
nro_total = 0
nro_to_skip = []
folder = ''
images = []
images_to_rename = []


def main():
    get_args(argv[1:])
    get_images()
    get_images_to_rename()
    rename_images()


def get_args(args):
    # If no args given, show usage
    if len(args) < 1:
        usage_text()
        exit(0)
    # check if --help is written
    if args[0] == '--help':
            help_text()
    # Parse arguments
    try:
        opts, args = getopt(args, 'hyln:dz:d')
    except GetoptError as e:
        print(e)
        help_text()
        exit(0)
    # Get options
    for opt, arg in opts:
        if opt == '-h':
            help_text()
        elif opt == '-y':
            global yes
            yes = True
        elif opt == '-n':
            global nro
            nro = int(arg) - 1
        elif opt == '-z':
            if int(arg) < 0:
                print('You can\'t have negative number of zeroes')
                exit(0)
            global zeroes
            zeroes = int(arg)
        elif opt == '-l':
            global log
            log = True
            print('log is true')
    # Get folder
    try:
        if path.exists(str(args[0])):
            global folder
            if search(r'/$', str(args[0])):
                folder = str(args[0])
            else:
                folder = str(args[0]) + '/'
        else:
            print('Folder doesn\'t exist')
            exit(0)
    except IndexError:
        print('Please define folder location')
        exit(0)


def get_images():
    imgs = listdir(folder)
    global images
    for image in imgs:
        if search(r'\.[pngj]+$', image):
            images.append(image)
    global nro_total
    nro_total = len(images)


def get_images_to_rename():
    nmax = nro_total
    global images_to_rename
    global nro_to_skip
    for image in images:
        try:
            i = search(r'(^\d+)\.[pngj]+$', image).group(1)
        except Exception:
            images_to_rename.append(image)
            continue
        if int(i) > nmax + nro or int(i) <= nro:
            # the range needs to be the range of numbers to use in renaming
            images_to_rename.append(image)
        elif not len(i) == zeroes:
            images_to_rename.append(image)
        else:
            nro_to_skip.append(int(i))
    if len(images_to_rename) == 0:
        print('Nothing to rename')
        exit(0)


def rename_images():
    n = nro + 1
    rename = []
    rename_total = 0
    # Create list of images to rename with name to rename to
    for i in range(n, nro_total + n):
        # the range needs to be the range of numbers to use in renaming
        if not i in nro_to_skip:
            ext = search(r'\.[pngj]+$', images_to_rename[0]).group()
            rename.append([images_to_rename[0], generate_name(i) + ext])
            images_to_rename.remove(images_to_rename[0])
            rename_total += 1
        if len(images_to_rename) == 0:
            break
    # Ask about renaming
    if not yes:
        print('These will be renamed:')
        n = -1
        for i in rename:
            n += 1
            print(rename[n][0] + ' -> ' + rename[n][1])
        print('_'*20)
        print('Renaming ' + str(rename_total) + ' of ' + str(nro_total))
        y = input('Are you sure you want to rename (y/n): ')
        if y.lower() == 'n':
            print('Aborting')
            exit(0)
        if not log:
            y = input('Do you want to save a log file (y/n): ')
            if y.lower() == 'y':
                create_log(rename)
    elif log:
        create_log(rename)
    if yes:
        print('Renaming:')
        n = -1
        for i in rename:
            n += 1
            print(rename[n][0] + ' -> ' + rename[n][1])
        print('_'*20)
        print('Renaming ' + str(rename_total) + ' of ' + str(nro_total))
    # Rename images with xxx prefix
    n = -1
    for i in rename:
        n += 1
        osrename(folder + rename[n][0], folder + 'x'*3 + rename[n][1])
    # Rename images to correct name
    n = -1
    for i in rename:
        n += 1
        osrename(folder + 'x'*3 + rename[n][1], folder + rename[n][1])


def generate_name(number):
    n = zeroes - len(str(number))
    return('0'*n + str(number))


def create_log(rename_list):
    text = ''
    n = -1
    for i in rename_list:
        n += 1
        text += rename_list[n][0] + ' -> ' + rename_list[n][1] + '\n'
    with open('rename.log', 'w') as f:
        f.write(text)


def help_text():
    # Print help text and exit
    usage_text()
    print('\n'
          'img_renamer is a command line interface for renaming images in'
          'numberic order.\n\n'
          '-l\t\tSave logfile [rename.log].\n'
          '-y\t\tAutomatic yes to prompts; assume "yes" as answer to all'
          'prompts and run non-interactively.\n'
          '-n NRO\t\tDefine custom number to start counting from.\n'
          '-z NRO\t\tDefine custom number of zeroes before number.\n'
          '-h, --help\tPrint this help text and exit.\n\n'
          'Programmed by @Miicat_47')
    exit(0)


def usage_text():
    # Print usage (also part of help_text)
    print('Usage: renamer [OPTIONS] [FOLDER]')


if __name__ == '__main__':
    main()
