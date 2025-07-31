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

let main_page;
if(file_map[browser_lang] != null) {
    main_page = await getFileContent(file_map[browser_lang]);
} else {
    main_page = await getFileContent(file_map['en']);
}

content = marked.parse(main_page);
document.getElementById('content').innerHTML = content;
console.log(content);
