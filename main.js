import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";


const browser_lang = navigator.language.split('-')[0];

const file_map = {
    'en': 'main_page.en.md',
    'pt': 'main_page.pt.md'
}

let main_page = '';
if(file_map[browser_lang] != null) {
    main_page = await fetch(file_map[browser_lang])
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
} else {
    main_page = await fetch(file_map['en'])
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

content = marked.parse(main_page);
document.getElementById('content').innerHTML = content;
console.log(content);
