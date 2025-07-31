import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";


const browser_lang = navigator.language.split('-')[0];

const file_map = {
    'en': 'main_page.en.md',
    'pt': 'main_page.pt.md'
}

const getFileContent = async (file_name) => {
    return await fetch(file_name)
        .then(response => {
            if (!response.ok) throw new Error('Network response not ok: ' + response.status);
            return response.text();
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            throw error;
        });
}

// let main_page;
// if(file_map[browser_lang] != null) {
//     main_page = await getFileContent(file_map[browser_lang]);
// } else {
//     main_page = await getFileContent(file_map['en']);
// }

let main_page = `# Bem-vindo  

Este é meu site, aqui encontrará meu blog (com artigos) e outras coisas aleatórias que eu gostaria de aprender.
Este site é feito para ajudar-me ao aprender e espero que vocês também aprendam com seu código.

## O que posso fazer aqui?

1. Bom, este é o hub para interagir com meu blog. [Você pode ver meu blog aqui](/blog/).

## Código fonte!! 💢

Pode encontrar o código fonte [disponível aqui](https://github.com/Viktor95801/viktor95801.github.io).`

// content = marked.parse(main_page);
content = main_page;
document.getElementById('content').innerHTML = content;
console.log(content);
