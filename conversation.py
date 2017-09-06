import csv
import urllib
import json
from subprocess import Popen, os, PIPE
from random import randint
import os.path


class MyOpener(urllib.FancyURLopener):
	version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'


def check_process(PROCESS_NAME):
    cmd = "ps -ef | grep " + PROCESS_NAME
    process_list = Popen( cmd, stdout=PIPE, shell=True )
    out, err = process_list.communicate()

    fields = ['UID', 'PID', 'PPID', 'C', 'STIME', 'TTY', 'TIME', 'CMD']
    reader = csv.DictReader(out.decode('ascii').splitlines(),
                            delimiter=' ', skipinitialspace=True,
                            fieldnames=fields)
    for row in reader:
        if row['CMD'] == PROCESS_NAME:
            return True;
        else:
            continue
    return False;


def check_lockfile():
	result = os.path.exists('/tmp/conversation.lock')
	return result;


def mkLockfile():
	cmd = ['touch', '/tmp/conversation.lock']
	macTerm(cmd)


def rmLockfile():
	cmd = ['rm', '/tmp/conversation.lock']
	macTerm(cmd)


def baconipsum(LENGTH):
    url = 'https://baconipsum.com/api/?type=all-meat&sentences=' + str(LENGTH)
    agent = MyOpener()
    page = agent.open(url)
    jsonurl = page.read()
    data = json.loads(jsonurl)
    return data[0]


def speak_it(VOICE, WORDS):
    Popen(['say', '-v', VOICE, WORDS])


def main ():
	mkLockfile()
    voices = ["Samantha", "Daniel", "Milena", "Lee"]
    number_of_voices = randint(1,3)
    print("Number of Speakers: \t" + str(number_of_voices + 1))
    while check_lockfile():
        speaker = voices[randint(0,number_of_voices)]
        words = baconipsum(randint(1,2))

        speak_it(speaker, words)
        while (check_process('say') == True):
            continue


if __name__ == "__main__":
	main()
