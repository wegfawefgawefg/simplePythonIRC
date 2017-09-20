import sys

#   usage
if len( sys.argv ) != 1:
    sys.stdout.write( "Usage: python3 spamLine.py \"%s\"" )

while True:
    sys.stdout.write( sys.argv[1] + '\n' )
