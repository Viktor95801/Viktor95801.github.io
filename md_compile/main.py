import sys

import pygments
import pygments as pg
import pygments.lexers as pl
import pygments.formatters as pf
import pygments.util as pu

def highlight_code(code: str, lang: str = "txt") -> str:
    """
    Highlight a code snippet.

    Args:
        code (str): The code snippet to be highlighted.
        lang (str, optional): The language of the code snippet. Defaults to "txt".
    
    Returns:
        str: The highlighted code snippet as a html string.
    
    Raises:
        pygments.util.ClassNotFound: if invalid lang is provided
    """
    if lang == '' or lang is None:
        lang = "txt"
    
    try:
        lexer: pygments.Lexer = pl.get_lexer_by_name(lang)
    except pu.ClassNotFound: 
        lexer = pl.guess_lexer(code)
    
    formatter: pf.HtmlFormatter = pf.HtmlFormatter()
    return pg.highlight(code, lexer, formatter)

def md2html(md_text: str) -> str:
    in_code_block = False
    code_block_lang = "txt"
    code_lines: list[str] = []
    
    html: list[str] = []
    for line in md_text.split('\n'):
        if in_code_block:
            if line.startswith("```"):
                in_code_block = False
                code = '\n'.join(code_lines)
                
                html.append(highlight_code(code, code_block_lang))
                
                continue
            code_lines.append(line)
            continue
        
        if line.startswith("```"):
            code_block_lang: str = line[3:] or "txt"
            in_code_block = True
            
            code_lines = []
            continue
        
        if line.startswith("#"):
            c = line[0]
            i = 0
            while c == '#':
                i += 1
                c = line[i]
            # TODO: handle unsupported level
            html.append(
                f"<h{i}>{line[i+1:]}</h{i}>"
            )
            continue
        
        html.append(line)
        
    return '\n'.join(html)

def main(args: list[str]) -> None:
    if not (2 <= len(args) <= 3):
        raise Exception()
    
    contents: str = ''
    with open(args[1]) as f:
        contents = f.read()
    
    result = md2html(contents)
    if len(args) == 3:
        with open(args[2], 'w') as f:
            f.write(result)
    else:
        print(result)


if __name__ == '__main__':
    main(sys.argv)
