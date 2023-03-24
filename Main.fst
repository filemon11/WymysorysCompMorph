set char-encoding utf-8

clear ;

set obey-flags ON ;


source < Rules/PhonologicalRules.fst

regex PhonologicalRules ;

read lexc < Grammar.txt ;

set flag-is-epsilon ON

# Filter

regex [ 0 -> %/a || ?* _ ? ] ;

regex [ 0 -> %/u || ?* _ ? ] ;

regex [ 0 -> %/2u || ?* _ ? ] ;

regex [ 0 -> %/3u || ?* _ ? ] ;

regex [ 0 -> %/ou || ?* _ ? ] ;

regex [ 0 -> %/2ou || ?* _ ? ] ;

regex [ 0 -> %/3ou || ?* _ ? ] ;

regex [ ~[?*] <- $[ %/u ] ] ;

regex [ ~[?*] <- $[ %/2u ] ] ;

regex [ ~[?*] <- $[ %/3u ] ] ;

regex [ ~[?*] <- $[ %/ou ] ] ;

regex [ ~[?*] <- $[ %/2ou ] ] ;

regex [ ~[?*] <- $[ %/3ou ] ] ;

regex [ ~[?*] <- $[ %/a ] ] ;

#

compose net ;

define Total ;

source < Rules/OverrideExceptions.fst ;

source < Rules/AdditionalCases.fst ;


read regex [ OverrideExceptions .P. Total ] | AdditionalCases ;
