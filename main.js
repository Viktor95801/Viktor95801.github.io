import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";


const browser_lang = navigator.language.split('-')[0];

const file_map = {
    'en': 'main_page.en.md',
    'pt': 'main_page.pt.md'
}

const getFileContent = async (file_name) => {
    const response = await fetch(file_name);
    if(!response.ok) {
        throw new Error("Response not OK: " + response.status);
    }
    return response.text();
}

let main_page;
if(file_map[browser_lang] != null) {
    main_page = await getFileContent(file_map[browser_lang]);
} else {
    main_page = await getFileContent(file_map['en']);
}

const content = marked.parse(main_page);
document.getElementById('content').innerHTML = content;
console.log(content);
