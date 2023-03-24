import subprocess
import os
import json

working_dir = "'{}'".format(os.getcwd())
script_dir = "Main.fst"
test_dir = "TestData/"
wordtypes_dir = "WordTypes/Types.txt"

#Utilies
#is iterable?
def iterable(obj):
    return (True if type(obj) in (list, tuple) else False)

#Compare two lists of words for set equality
def compare(x, y):
    return set(x) == set(y)

#perform list operation
def listperf(get_input, function):
    return [function(row) for row in get_input]

def xfstout_to_list(string):
    return string.split("\n")[:-1]

#converts analysis to list
def analysis_to_list(analysis):
    return analysis.split("+")

def categoryconcat(cat1, cat2):
    if cat1 == "":
        return cat2
    if cat2 == "":
        return cat1
    else:
        return cat1+"+"+cat2

#get inflection categories data
def wordinfo():
    with open(wordtypes_dir, 'r') as type_data:
        type_dict = json.loads(type_data.read())
        return type_dict

def inflectinfo(category):
    return wordinfo()[category]

#Classes

class Lexeme:
    def __init__(self, stem, category):
        self.stem = stem
        self.category = category
        self.tup = (self.stem, self.category)
    def __str__(self):
        return str(self.tup)
    def __repr__(self):
        return self.__str__()
    def inflectinfo(self):
        return inflectinfo(self.category)
    def analysisform(self):
        return categoryconcat(self.stem, self.category)

class Analysisverbund:
    def __init__(self, analysis):
        self.analysis = analysis
        self.wordlist = [Word(form, analysis) for form in down(analysis)]
    def __str__(self):
        return str(self.wordlist)
    def __repr__(self):
        return self.__str__()
    def __iter__(self):
        return self.wordlist

class Word:
    def __init__(self, form, analysis):
        self.form = form
        self.analysis = analysis
        self.listanalysis = analysis_to_list(analysis)
        self.stem = self.listanalysis[0]
        self.category = self.listanalysis[1]
        self.tup = (self.form, self.analysis)
    def __str__(self):
        return str(self.tup)
    def __repr__(self):
        return self.__str__()
    def isempty(self):
        return self.form == "???"

class Wordform:
    def __init__(self, form):
        self.form = form

        analysis = up(form)
        self.analysis = [] if analysis == ["???"] else analysis

        self.listanalysis = [analysis_to_list(analysis) for analysis in self.analysis]

        self.wordlist = [Word(form, wordanalysis) for wordanalysis in self.analysis]

        lexeme_tuple_list = [(word.stem, word.category) for word in self.wordlist]
        lexeme_tuple_list = list(set(lexeme_tuple_list))

        self.lexeme = [Lexeme(*tup) for tup in lexeme_tuple_list]

        self.category = list(set([tup[1] for tup in lexeme_tuple_list]))

        self.stem = list(set([tup[0] for tup in lexeme_tuple_list]))

#Help class
class Decltable:
    def __init__(self, inflectindex, before_variant):
        self.before_variant = before_variant
        if len(inflectindex) == 0:
            return None
        self.category = list(inflectindex)[0]
        self.variants = inflectindex[self.category]

        self.decltables = []
        for v in self.variants:
            if type(v) == dict:
                self.decltables.append((list(v.keys())[0], Decltable(v[list(v.keys())[0]], before_variant)))
            elif len(inflectindex) > 1:
                self.decltables.append((v, Decltable({i:inflectindex[i] for i in inflectindex if i != self.category}, categoryconcat(before_variant, v))))
            else:
                self.decltables.append((v))
        #self.decltables = [(((v, Decltable({i:inflectindex[i] for i in inflectindex if i != self.category}, categoryconcat(before_variant, v))) if len(inflectindex) > 1 else (v)) if type(v) != dict else (list(v.keys)[0], Decltable(v[list(v.keys)[0]], before_variant, v))) for v in self.variants]
        #self.decltables = [((v, Decltable({i:inflectindex[i] for i in inflectindex if i != self.category}, categoryconcat(before_variant, v))) if len(inflectindex) > 1 else (v)) for v in self.variants]
    def __str__(self):
        return self.category + ": " + str([(table[0], str(table[1])) if len(table) == 2 else (table) for table in self.decltables])
    def __repr__(self):
        return self.__str__()
    def __iter__(self):
        return self.decltables
    def inflect(self, lexeme, variant):
        if self.before_variant == "":
            return [(declt[1].inflect(lexeme,declt[0]) if len(declt) == 2 else (declt, Analysisverbund(categoryconcat(categoryconcat(lexeme.analysisform(), self.before_variant),declt)))) for declt in self.decltables]
        else:
            return (variant, [(declt[1].inflect(lexeme,declt[0]) if len(declt) == 2 else (declt, Analysisverbund(categoryconcat(categoryconcat(lexeme.analysisform(), self.before_variant),declt)))) for declt in self.decltables])

class Lexemedeclension:
    def __init__(self, lexeme):
        self.decltable = Decltable(inflectinfo(lexeme.category), "")
        self.lexeme = lexeme
        self.table = []
    def inflect(self):
        self.table = self.decltable.inflect(self.lexeme, "")
        return self.table
    def perform_on_words(self, func, limit_to_existing = ""):
        return [[func(word.form) for word in verbund.__iter__()] for verbund in self.traverse(self.table) if limit_to_existing == "" or verbund.__iter__()[0].form != '???']
    def perform_on_verbund(self, func, limit_to_existing = ""):
        return [func(verbund) for verbund in self.traverse(self.table) if limit_to_existing == "" or verbund.__iter__()[0].form != '???']
    def give_as_dict(self,limit_to_existing):
        return {analysis:[word.form for word in wordlist] for analysis, wordlist in self.perform_on_verbund((lambda x : (x.analysis, x.wordlist)), "yes" if limit_to_existing != "" else "")}
    #gives list of Analysisverbunds
    def traverse(self, table):
        outlist = []
        if type(table) == Analysisverbund:
            outlist = [table]
        elif type(table) == list:
            for entry in table:
                outlist += self.traverse(entry)
        elif type(table) == tuple:
            outlist += self.traverse(table[1])
        return outlist
    def __iter__(self):
        return self.traverse(self.table)

#Functions

#Input: analysis String, Output: category as String
def getcat(analysis):
    if analysis == "":
        return ""
    else:
        return analysis.split("+")[1]

def getstem(analysis):
    if analysis == "":
        return ""
    else:
        return analysis.split("+")[0]

#split with checking last entry for emptyness ('') and removing if empty
def xsplit(glist, seperator):
    output = glist.split(seperator)
    if output[-1] == '':
        return output[:-1]
    else:
        return output

#Returns String or List
#direction: 'up' or 'down'
def apply(direction, source, from_file=False, to_list=False, seperator="\n", secondary_seperator=""):
    if from_file:
        source = "< " + source
    output = subprocess.check_output([working_dir + '/xfst -q -e "source < '+script_dir+'" -e "apply ' + direction + ' ' + source + '" -stop'], shell=True, stderr=subprocess.STDOUT).decode("utf-8")
    if to_list:
        output = xsplit(output, seperator)
    return output if secondary_seperator == "" else [xsplit(entry, secondary_seperator) for entry in output]

#Returns a list of words
def up(word):
    if iterable(word):
        return listperf(word, up)
    else:
        output = apply("up", word, to_list=True)
        return output

#Returns a list of words
def down(word):
    if iterable(word):
        return listperf(word, down)
    else:
        output = apply("down", word, to_list=True)
        return output

#Returns Tuple of:
# 1. List containing a list for each entry to test. Each list contains a tuple for each form predicted: (form, True if correct, False if not)
# 2. List containing a list for each entry to test. Each list contains a tuple for each form that should be predicted: (form, True if predicted, False if not)
# 3. List containing True if entries predictions and correct entries equal; False if not
# category: 'Nouns', 'Adjectives', 'Prepositions' or 'Articles'
def test(category, direction, to_test_file = "", correct_file = ""):
    file_direction = "l" if direction == "up" else "u"
    if to_test_file == "":
        to_test_file = test_dir+category+"_"+file_direction+".txt"
    if correct_file == "":
        correct_file = test_dir+category+"_"+file_direction+"_correct.txt"

    predicted_list = apply(direction, to_test_file, from_file=True, to_list=True, seperator="\n???\n", secondary_seperator="\n")
    equal_index = [False for i in predicted_list]

    with open(correct_file, 'r') as correct_data:
        correct_list = correct_data.read().split("\n\n")
        correct_list = [ xsplit(word,"\n") for word in correct_list ]

        counter = 0
        for correct, predicted in zip(correct_list, predicted_list):
            if compare(correct, predicted):
                equal_index[counter]=True
            for i in range(0, len(predicted)):
                if predicted[i] in correct:
                    predicted[i] = (predicted[i], True)
                else:
                    predicted[i] = (predicted[i], False)

            for i in range(0, len(correct)):
                if (correct[i], True) in predicted:
                    correct[i] = (correct[i], True)
                else:
                    correct[i] = (correct[i], False)
            counter += 1
    return (predicted_list, correct_list, equal_index)

# Tests all word types up and down
def testall():
    wordTypes = wordinfo()
    return {wordType:[test(wordType, "up"),test(wordType, "down")] for wordType in wordTypes.keys()}

# Returns dictionary; Keys: analyses; entries: lists of word forms
def inflect(word, gtype, limit_to_existing=""):
    decl = Lexemedeclension(Lexeme(word,gtype))
    decl.inflect()
    return decl.give_as_dict(limit_to_existing)
