#!usr/bin/python

import os
from pathlib import Path
import json
import subprocess as sub
import re

def get_posts(blog):
    posts: list[Path] = [f for f in (blog/'posts').iterdir() if f.is_file() and f.name.endswith('.md')]

    posts_processed = []

    meta_data_pattern = re.compile(r"""<!--.*date:"(.*)".*title:"(.*)".*description:"(.*)".*-->""", re.DOTALL)
    for p in posts:
        pc: str = p.read_text('utf-8')
        
        data: re.Match[str] | None = meta_data_pattern.search(pc)
        if data is None:
            print(f'Unable to find meta data in {p.name}')
            continue
        ptitle: str = data.group(2)
        pdate: str = data.group(1)
        pdescription: str = data.group(3)
        plang: str = p.name.split('.')[1]
        
        posts_processed.append(
            {
                "title": ptitle,
                "date": pdate,
                "description": pdescription,
                "lang": plang,
                "file-name": p.name
            }
        )
    
    return posts_processed


def main():
    blog = Path.cwd()
    # print(cwd)
    # blog = cwd / '../' / '../'
    # blog = blog.resolve()
    
    # os.chdir(blog)
    
    posts = get_posts(blog)
    with open('posts.json', 'w') as f:
        f.write(json.dumps(posts, indent=2))

    sub.run(['git', 'add', 'posts.json'])

if __name__ == '__main__':
    main()
