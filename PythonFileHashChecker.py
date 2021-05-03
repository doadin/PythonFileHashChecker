import argparse
import hashlib
import os
import sys

parser = argparse.ArgumentParser(description='Python Program to check hash or'
                                             ' file checksum.')
parser.add_argument("--file", help="File you want the hash for.")
parser.add_argument("--hashtype", help="Type of hash you want.MD5 SHA etc etc")
parser.add_argument("--list", help="Path to a Text file containing file name + hash to"
                                   " check against.")
parser.add_argument("--save", help="Path to save filename.hashtype to file")
parser.add_argument("-v", action="store_true", dest="verbose")
parser.add_argument("-q", action="store_false", dest="verbose")
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

if args.file:
    filename = os.path.basename(args.file)

if args.hashtype:
    if sys.version_info >= (3, 0):
        if args.hashtype not in hashlib.algorithms_available:
            print('The algorithm you specified is not supported')
            sys.exit(1)
    else:
        if args.hashtype not in hashlib.algorithms:
            print('The algorithm you specified is not supported')
            sys.exit(1)
else:
    # If hashtype wasnt supplied try and find it in our hash list text file
    if args.file and args.list:
        try:
            print("Got file and list searching for hashtype in list...")
            for line in open(args.list, 'r'):
                if filename in line:
                    txtline = line
                    #print(txtline)
                    fileplushash = txtline.split()
                    filenameinlist, correcthash, hashtype = fileplushash[0], fileplushash[1], fileplushash[2]
                    args.hashtype = hashtype
                    print("Found hashtype:  ", args.hashtype)
            if sys.version_info >= (3, 0):
                if args.hashtype not in hashlib.algorithms_available:
                    print('The algorithm found is not supported')
                    raise ValueError('The algorithm you specified is not supported')
            else:
                if args.hashtype not in hashlib.algorithms:
                    print('The algorithm found is not supported')
                    raise ValueError('The algorithm you specified is not supported')
        except ValueError as err:
            #print(err)
            sys.exit(1)
        except:
            print("Error Reading Hash From Hashlist")
    if args.file and not args.hashtype:
        print("--hashtype not supplied defaulting to md5")
        args.hashtype = "MD5"

if args.file:
    # Generate the selected files hash
    filehash = hashlib.new(args.hashtype)
    with open(args.file, "rb") as f:
        while True:
            buf = f.read(4096)
            if not buf:
                break
            filehash.update(buf)
    filehash = filehash.hexdigest()

# If user selected a list
# Search text file for file name + hash
if args.list:
    # If filename is in the list
    for line in open(args.list, 'r'):
        if filename in line:
            txtline = line
else:
    filenameplushashname = args.file + "." + args.hashtype
    if os.path.isfile(filenameplushashname):
        args.list = filenameplushashname
        for line in open(args.list, 'r'):
            if filename in line:
                txtline = line

# If a file and hash list where given compaire
if args.file and args.list and filehash and txtline:
    try:
        fileplushash = txtline.split()
        filenameinlist, correcthash = fileplushash[0], fileplushash[1]
        print("Filename:        ", filename)
        print("File Hash:       ", filehash)
        print("Correct Hash:    ", correcthash)
        # Compare Hashes
        if filehash == correcthash:
            print("Hashes match file is safe!")
        else:
            print("Hashes DO NOT match file is corrupt!")
    except NameError:
        print("File Not Found In List!")
        print("File:        ", filename)
        print("Has the Hash:", filehash)
else:
    if args.file and filehash:
        print("Your File:    ", filename)
        print("Has a Hash of:", filehash)
    if args.save:
        print("Saving Hash File: ", filename + "." + args.hashtype)
        if sys.version_info >= (3, 0):
            f = open(args.save + "\\" + filename + "." + args.hashtype, "w+")
            f.write(filename + " " + filehash + " " + args.hashtype)
        else:
            f = open(args.save + "\\" + filename + "." + args.hashtype, "wb+")
            f.write(filename + " " + filehash + " " + args.hashtype)            
        #print(f)
