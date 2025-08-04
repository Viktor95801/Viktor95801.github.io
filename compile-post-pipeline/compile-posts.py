#!usr/bin/python

import hashlib as hl
import json
import os
import subprocess as sp
import sys

import markdown as md

def checksum(file_path: str, chunk_size: int = 8192) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    
    h = hl.md5()
    
    if type(chunk_size) is not int or chunk_size <= 0:
        chunk_size = 8192
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)

    return h.hexdigest()

def file_needs_update(file_path: str, checksum_path: str | None = None) -> bool:
    if checksum_path is None:
        checksum_path = 'compile-post-pipeline/checksum/' + file_path.split('/')[-1] + '.checksum'
    
    if not os.path.exists(checksum_path):
        return True
    
    with open(checksum_path) as f:
        fchecksum: str = f.read()
    return checksum(file_path) != fchecksum

def file_update_checksum(file_path: str, checksum_path: str | None = None) -> None:
    if checksum_path is None:
        checksum_path = 'compile-post-pipeline/checksum/' + file_path.split('/')[-1] + '.checksum'
    
    with open(checksum_path, 'w') as f:
        f.write(checksum(file_path))

def main():
    with open('posts.json') as f:
        posts: list[dict] = json.load(f)

    force_build = False
    if len(sys.argv) == 2:
        if sys.argv[1] == '-B':
            force_build = True

    for p in posts:
        if force_build or file_needs_update('posts/' + p['file-name']):
            with open('posts/' + p['file-name']) as f:
                content: str = f.read()
            
            gen: str = md.markdown(
                content,
                encoding='utf8',
                
                extensions=[
                    'toc',
                    'fenced_code',
                ]
            )
            
            final_html = f"""<!DOCTYPE html>
<html lang="{p['lang']}">
    <head>
        <meta charset="UTF-8">
        
        <title>Blog - {p['title']}</title>
        
        <meta name="title" content="Blog - {p['title']}">
        <meta name="description" content="{p['description']}">
        <!-- <meta name="keywords" content=""> -->
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Open Graph / Facebook -->
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://viktor95801.github.io/blog/posts/{p['file-name']+'.html'}" />
        <meta property="og:title" content="{p['title']}" />
        <meta property="og:description" content="{p['description']}" />
        <meta property="og:image" content="/assets/preview.png" />

        <!-- X (Twitter) -->
        <meta property="twitter:card" content="summary_large_image" />
        <meta property="twitter:url" content="https://viktor95801.github.io/blog/posts/{p['file-name']+'.html'}" />
        <meta property="twitter:title" content="{p['title']}" />
        <meta property="twitter:description" content="{p['description']}" />
        <meta property="twitter:image" content="/assets/preview.png" />
        
        <!-- Favicon -->
        <link rel="shortcut icon" href="/favicon.ico">
        
        <!-- CSS -->
        <link rel="stylesheet" href="/css/content.css"/>
        <link rel="stylesheet" href="/css/style.css"/>
        <link rel="stylesheet" href="/css/top-bar.css"/>
        <link rel="stylesheet" href="/css/post.css"/>
        <link rel="stylesheet" href="/css/code-extra.css"/>
        
        <!-- Syntax highlighting -->
        <link rel="stylesheet" href="/assets/styles/paraiso.dark.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js"></script>

        <script>hljs.highlightAll();</script>
    </head>
    <body>
        <!-- Hamburger button top bar -->
        <nav id="ham-nav">
                <input 
                    id="burger"
                    type="checkbox"/>
                <label for="burger">&#9776;</label>
                
                <div id="ham-items">
                    <div> <!-- Left side -->
                        <a href="/">
                            Home
                        </a>
                        <a href="/blog/" class="active">
                            Blog
                        </a>
                    </div>
                    <div> <!-- Right side -->
                        <a href="https://github.com/Viktor95801/Viktor95801.github.io">
                            Source
                        </a>
                    </div>
                </div>
        </nav>
        
        <h1 lang="{p['lang']}">
        {
            "Voc&ecirc est&aacute lendo: '" + p['title'] + "'" if p['lang'] == 'pt'
            else "You're reading: '" + p['title'] + "'"
        }
        </h1>
        
        <div id="content">
            {gen}
        </div>
    </body>
</html>
"""
            
            with open('blog/posts/' + p['file-name'] + '.html', 'w') as f:
                f.write(final_html)
            
            file_update_checksum('posts/' + p['file-name'])

    sp.run(['git', 'add', 'blog/posts/'])

if __name__ == '__main__':
    main()
