set char-encoding utf-8

# extra definitions for words in vocative

define VocativeSG [ müm %+Noun:0 %+F:0 | büw %+Noun:0 %+M:0 | bow %+Noun:0 %+N:0 | pot %+Noun:0 %+N:0 | knȧht %+Noun:0 %+M:0 ] %+sg:0 %+voc:y ;
define VocativePL [ łoüt %+Noun:0 %+M:0 ] %+pl:0 %+voc:y ;

define Prepositions [ {yn}:{ys} | {uf}:{ufs} | {fjy}:{fjys} | {nö}:{nös}] %+Preposition:0 %+Cl:0 %+Article:0 %+def:0 %+N:0 %+sg:0 %+acc:0 ;

define AdditionalCases VocativeSG | VocativePL | Prepositions ;
