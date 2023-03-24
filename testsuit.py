import subprocess
import os
from subprocess import PIPE
import json
from datetime import datetime
import xfstlib as lib

working_dir = "'{}'".format(os.getcwd())
test_dir = "TestData/"
script_dir = "Main.fst"

text_output = True

past_user_input = ["#"]

#def add_word(cat, word, flex):
#    file_obj = open(files[cat],"a")
#    entry = word + " " + flex + " ;"
#    file_obj.write(entry + "\n")
#    file_obj.close()
#    return entry

#def combine_data():
#    os.remove("Grammar.txt")
#    with open('Grammar.txt', 'w') as outfile:
#        for fname in filenames:
#            with open(fname) as infile:
#                for line in infile:
#                    outfile.write(line)

def clearlog():
    with open("log.txt", 'w') as log_file:
        log_file.write("Wymysorys Test Suit Version 0.1\nNew log "+str(datetime.now())+"\n")

def logdata(logstring):
    with open("log.txt", 'a') as log_file:
        log_file.write(logstring)

class Cprint:
    def __init__(self, outprint=True):
        self.outprint = outprint
        self.text = ""
    def print(self, s):
        if type(s) is list:
            for entry in s:
                self.print(entry)
        else:
            if self.outprint and text_output:
                logdata(s+"\n")
                print(s)
            self.text = self.text + s + "\n"


print("---------------------------------------------")
print("Wymysorys Test Suit Version 0.2")
print("Automated Tool for Morphological Analysis")
print("---------------------------------------------")
print("---------------------------------------------")
print("-- Loading Grammar -- ")
print("---------------------------------------------")
print("---------------------------------------------")
print("-- Done! --")

continue_program = True
debug_mode = False

def command(c, arguments=[]):
    options = {
                "xfst" : [xfst, True],
                "quit" : [end_program, False],
                "stop" : [end_program, False],
                "halt" : [end_program, False],
                "up" : [up, True],
                "down" : [down, True],
                "test" : [test, True],
                "l" : [last, False],
                "debug" : [debug, False],
                "uplist" : [uplist, True],
                "downlist" : [downlist, True],
                "inflect" : [inflect, True],
                "testall" : [testall, True]
            }

    if debug_mode:
        print("Calling >" + c + "< with argument(s) >" + str(arguments) + "<.")

    #Unknown command error
    if not c in options:
        print("FAIL: Command unknown.")
        return False

    #known command
    cprint = Cprint()
    options[c][0](Cprint(),*arguments)
    return(options[c][1])

def xfst(cprint):
    p1 = subprocess.Popen([os.getcwd() + "/xfst"])
    cprint.print("-------------- connected!")
    return cprint.text

def end_program(cprint):
    cprint.print("goodbye!")
    exit()

def up(cprint, word):
    cprint.print(lib.up(word))
    return cprint.text

def down(cprint, word):
    cprint.print(lib.down(word))
    return cprint.text

def uplist(cprint, *wordlist):
    for word in lib.up(wordlist):
        cprint.print(word)
        cprint.print("")
    return cprint.text

def downlist(cprint, *wordlist):
    for word in lib.down(wordlist):
        cprint.print(word)
        cprint.print("")
    return cprint.text

# Utility function for test-outprint
def printtest(cprint, predicted_list, correct_list, equal_index):
    counter = 0
    for correct, predicted in zip(correct_list, predicted_list):
        counter += 1
        for word in correct:
            if not word[1]:
                cprint.print("Not predicted: " + word[0] + " at entry " + str(counter))
        for word in predicted:
            if not word[1]:
                cprint.print("Falsely predicted: " + word[0] + " at entry " + str(counter))
    correct_num = sum(equal_index)
    cprint.print("END OF TEST, predicted " + str(correct_num) + " entries correctly")
    cprint.print("predicted " + str(len(correct_list) - correct_num) + " falsely")

    return cprint.text

def test(cprint, category, direction):
    return printtest(cprint, *lib.test(category, direction))

def testall(cprint):
    result = lib.testall()
    for wordType in result:
        cprint.print(wordType+":")
        cprint.print("- up:")
        printtest(cprint, *result[wordType][0])
        cprint.print("- down:")
        printtest(cprint, *result[wordType][1])
    return None

def inflect(cprint, word, gtype, limit_to_existing=""):
    dictionary = lib.inflect(word, gtype, limit_to_existing)
    for key in dictionary:
        cprint.print(key)
        cprint.print(dictionary[key])
        cprint.print("")
    return cprint.text

def last(cprint, index=""):
    if(index == "s"):
        cprint.print(str(past_user_input[1:]))
    elif(index==""):
        past_input_split = past_user_input[-1].split()
        if(past_input_split[0] != "#"):
            command(past_input_split[0], make_args(past_input_split))
        else:
            cprint.print("No command has been called.")
    else:
        past_input_split = past_user_input[-int(index)].split()
        if(past_input_split[0] != "#"):
            command(past_input_split[0], make_args(past_input_split))
        else:
            cprint.print("No command has been called.")
    return cprint.text

def debug(cprint, state=""):
    global debug_mode

    debug_mode = (True if state == "true" or (state == "" and debug_mode == False) else False)
    return cprint.text

######
def make_args(i_input_split):
    if len(i_input_split) > 1:
        return(i_input_split[1:])
    return([])
######

clearlog()

while(continue_program):
    promt_text = "/DEBUG/ (WymysorysL): " if debug_mode else "(WymysorysL): "
    user_input = input(promt_text)
    logdata(promt_text + user_input + "\n")

    input_split = user_input.split()

    if debug_mode:
        print(past_user_input)

    #process
    
    to_be_appended = command(input_split[0], make_args(input_split))
    if(to_be_appended):
        past_user_input.append(user_input)
