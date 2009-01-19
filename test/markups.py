bold_text   = [ "''this is bold text''" ]
italic_text = [ '//this is italics text//' ]
linebreak   = [ '\\' ]
heading     = [ '=', '==', '===', '====', '=====' ]
hrule       = [ '-----', '-------------', ]
olist       = [ '*', '**', '***', '****', '*****' ]
ulist       = [ '#', '##', '###', '####', '#####' ]
openlink    = [ '[[' ]
closelink   = [ ']]' ]
openmacro   = [ '{{' ]
closemacro  = [ '}}' ]
opennowiki  = [ '{{{' ]
closenowiki = [ '}}}' ]
tablestart  = [ '|' ]
tablehead   = [ '|=' ]

normaltext  = [ '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ `!@%&:;"<>,.?\t$^()+' ]

specialtext = [ r"'", r"'''", r"''''",
                '/', '///', '////',
                '======', '=======',
                '-', '--', '---', '----',
                '******', '********',
                '######', '#######',
                '[', '[[[', '[[[['.
                ']', ']]]', ']]]]'.
                '{', '{{{{'.
                '||', '|=|', '=|=||=',
                '\\', '\\\\\\', '\\\\\\\\',
              ]
