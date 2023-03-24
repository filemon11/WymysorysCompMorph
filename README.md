# A finite-state morphological grammar of Wymysorys
Wymysorys Computational Morphology Package Version 0.2
22.09.2020
Author: Lukas Mielczarek

More information available at: https://lukasmielczarek.de/index.php/computerlinguistik/

Includes:
1. Wymysorys Test Suit Version 0.2 - Automated Tool for Morphological Analysis: testsuit.py, TestData, WordTypes
2. Custom Python library for morphological analysis using xfst: xfstlib.py
3. xfst-compliant Wymysorys grammar: Main.fst, Grammar.txt, Rules
4. Project description

IMPORTANT:
You need to place a xfst program file into the Wymysorys parent folder. Due to licencing issues we cannot include the program with the package.

Instructions:
1. 
    Run the Test Suit using python 3.7; for Linux: Open terminal, navigate to the Wymysorys directory, run testsuit.py with python3.
    For more information on commands see project description
2.
    Python library usable with no prerequesites.
    You might need to re-assign the following variables currenctly set to these values:
    
    working_dir = os.getcwd()
    script_dir = "Main.fst"
    test_dir = "TestData/"
    wordtypes_dir = "WordTypes/Types.txt"

3.
    The grammar is importable in xfst using the command:
    
    source < Main.fst
    
