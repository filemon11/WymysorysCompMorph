set char-encoding utf-8

# Rules for lexc

define V [ e | i | ȧ | a | o | u | ü | y | ö ] ;
define C [ p | b | t | d | k | j | k | g | f | w | s | z | ś | ź | ż | h | n | ń | m | r | l | ł | ć ] ;
define DescDiph [ a i | e i | o ü | o i ] ;

# Ablaut

define Ablaut1 [ %/ou -> [ %/u | 0 ] ] ;
define Ablaut2 [ u -> y , a -> e , o -> e , {iöe} -> ȧ , ö -> y , ü -> i , {ej} -> y || %/u _ ?* %/d ] ;
define Ablaut3 [ %/2ou -> [ %/2u | 0 ] ] ;
define Ablaut4 [ o -> a , ü -> {jy} , e -> ȧ j , {iöe} -> a || %/2u _ ?* %/d ] ;
define Ablaut5 [ %/3ou -> [ %/3u | 0 ] ] ;
define Ablaut6 [ o -> yy || %/3u _ ?* %/d ] ;
define AblautElim [ %/u -> 0 , %/d -> 0 , %/2u -> 0 , %/3u -> 0 ] ;
define Ablaut Ablaut1 .o. Ablaut2 .o. Ablaut3 .o. Ablaut4 .o. Ablaut5 .o. Ablaut6 .o. AblautElim ;

# Dative A
define Dat1 [ {^A} -> 0 || n _ , a _ , {um} _ ] ;
define Dat2 [ {^A} -> {^a} ] ;
define Dat Dat1 .o. Dat2 ;

# Suppletive Comparative
define SuppComp1 [ {güt} -> {bes} , {ryś} -> {ej} , {gröp} -> {gryw} || _ ?* %/comp ] ;
define SuppCompElim [ %/comp -> 0 ] ;
define SuppComp SuppComp1 .o. SuppCompElim ;

# Phonological Rules
define Pre1 ~[ $[ [ [ ? - a ] %/aadj ] ] ] ;                                # only words ending with -a are allowed to have the tag
define Pre2 [ %/aadj -> 0 ] ;
define Pre3 ~[ $[ [ a %/radj ] ] ] ;                                    # only words not ending with -a are allowed to have the tag
define Pre4 [ %/radj -> 0 ] ;
define Pre Pre1 .o. Pre2 .o. Pre3 .o. Pre4 ;

define Post1 ~[ $[ [ C - l - ł ] %^ n ] | $[ V %^ a ] ] | $[ DescDiph %^ a ] ;       # no morpheme boundary between consonant and n possible (except for l^ or ł^)
define Post2 ~[ $[ [ [ [ ? ? ] - {er} ] %/oe ] ] ] ;                         # only words ending with -er are allowed to have the tag
define Post Post1 .o. Post2 ;

define Phon1 [ %/a n -> 0 || _ %^ ? ] ;
define Phon2 [ %^ -> u || f _ m , t _ m ] ;
define Phon3 [ %^ -> e || f _ r , t _ r ] ;
define Phon4 [ r -> 0 || _ {^n} , [ ? - e ] _ {^a} , _ {^s} ] ;
define Phon5 [ {yr^} -> [ {y} | {ere} ] || _ r ] ;
define Phon6 [ {yr^} -> [ {eru} | {u} ] || _ m ] ;
define Phon7a [ %^ -> 0 || DescDiph  _ a ] ;        # define Phon7a [ %^ -> 0 || DescDiph  _ [ a | e ] ] ;
define Phon7b [ %^ -> j || [ k | h | V - y ] _ a , [ k | g | h ] _ e ] ;
define Phon8 [ e -> y || _ %^ [ n | s ] ] ;
define Phon11 [ %^ -> y %^ || [ C - l - ł - f ] _ [ n | s .#. ] ] ;
define Phon10 [ {guł^} -> {gl} || _ n ] ;
define Phon9 [ {y^s} -> {yś} ] ;
define Phon12 [ {^er} -> 0 || {er} _ ] ;
define Phon13 [ s -> 0 || [ s | c ] %^ _ ] ;

define Phon Pre .o. Phon1 .o. Phon2 .o. Phon3 .o. Phon4 .o. Phon5 .o. Phon6 .o. Phon7a .o. Phon7b .o. Phon8 .o. Phon11 .o. Phon10 .o. Phon9 .o. Phon12 .o. Phon13 .o. Post ;

define Elim [ {^} -> 0 , %/a -> 0 , %/oe -> 0 ] ;

define PhonologicalRules Ablaut .o. Dat .o. SuppComp .o. Phon .o. Elim ;
