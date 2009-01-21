import zwast as zwast

wiki2html    = { 
        "''"  : ('<strong>','</strong>' ),
        '//'  : ('<em>','</em>' ),
        '__'  : ('<u>','</u>' ),
        '^^'  : ('<sup>','</sup>' ),
        ',,'  : ('<sub>','</sub>' ),
        "'/"  : ('<strong><em>','</em></strong>' ),
        "'/_" : ('<strong><em><u>','</u></em></strong>' ),
}

ref2markups  = [ "''", '//', '__', '^^', ',,', "'/" ]
ref3markups  = [ "'/_" ]


def translate_textline( text_content, i, html ) :
    item = text_content[i]
    i    += 1
    if isinstance( item, (zwast.Link, zwast.Macro, zwast.BasicText, zwast.Empty) ) :
        html.append( item.tohtml() )
    else :
        raise Exception

    if i < len(text_content) :
        translate_textline( text_content, i, html )
    return

def match_markups( begins, ends ) :
    for i in begins :
        if i not in ends :
            continue
        j = i
        break
    else :
        return begins, ends
    return i, j

def process_text( text_content ) :
    html = []
    translate_textline( text_content, 0, html )
    i = 0
    while i < len(html) :
        if isinstance( html[i], str ) :
            i += 1
            continue
        for j in range( i+1, len(html) ) :
            if isinstance( html[j], str ) :
                continue
            b, e = match_markups( html[i][1], html[j][1] )
            if isinstance( b, str ) and isinstance( e, str ) :
                html[i] = html[i][0].replace( b, wiki2html[b][0], 1 )
                html[j] = html[j][0].replace( e, wiki2html[e][1], 1 )
                break
        if isinstance( html[i], str ) :
            for k in range(i+1, j) :
                if isinstance( html[k], tuple ) :
                    html[k] = html[k][0]
            i = j + 1
        else :
            i += 1
    for i in range(len(html)) :
        if isinstance( html[i], tuple ) :
            html[i] = html[i][0]
    return html

def parse_text( text ) :
    markups = []
    i = 0
    while i < len(text) :
        if text[i:i+2] in ref2markups :
            markup = text[i:i+2]
            i += 2
        elif text[i:i+3] in ref3markups :
            markup = text[i:i+3]
            i += 3
        else :
            markup = None
            i += 1
        if markup :
            markups.append( markup )
    return markups

