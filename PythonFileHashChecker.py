import hashlib
import argparse
import os

parser = argparse.ArgumentParser(description='Check ISO MD5.')
parser.add_argument("--file", help="File you want the hash for.")
parser.add_argument("--hashtype", help="Type of hash you want.(MD5 SHA etc etc..")
parser.add_argument("--list", help="Text file containing file name + hash to check against.")
args = parser.parse_args()

selectedfile = args.file
filename = os.path.basename(args.file)

if args.hashtype:
    if args.hashtype not in hashlib.algorithms:
            raise NameError('The algorithm you specified is not supported')
else:
    print "--hashtype not supplied defaulting to md5"
    args.hashtype = "MD5"

# Generate the selected files hash
filehash = hashlib.new(args.hashtype)
with open( args.file , "rb" ) as f:
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

# If a file and hash list where given compaire
if args.file and args.list:
    fileplushash = txtline.split()
    filenameinlist, correcthash = fileplushash[0],fileplushash[1]
    # Debug
    # print list[1]
    print "the file"
    print filename 
    print "has the hash:"
    print filehash
    print "correct hash is:"
    print correcthash
    # Compair Hashes
    if filehash == correcthash:
        print "Hashes match file is safe!"
    else:
        print " Hashes DO NOT match file is corrupt!"
else:
    print "your file:"
    print filename
    print "has a hash of:"
    print filehash

