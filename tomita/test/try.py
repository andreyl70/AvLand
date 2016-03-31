import sys
import json
import subprocess

text = """\
cat <<EOF
{0} {1} {2}\nEOF"""

TOMITA_BIN = "../bin/tomita-linux64"
TOMITA_CONFIG = "./config.proto"

def ppp(tomita, config, line):
    p = subprocess.Popen(text.format(tomita, config, line.encode('utf8')), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    ttt = p.stdout.read()
    retcode = p.wait()
    return " ".join(ttt.split()[2: ])

if __name__ == "__main__":
    for line in open(sys.argv[1]):
        if line.startswith('{'):
            js = json.loads(line)
            print ppp(TOMITA_BIN, TOMITA_CONFIG, js['about'])

