import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

const getFileContent = async (file_name) => {
    const response = await fetch(file_name);
    if(!response.ok) {
        throw new Error("Response not OK: " + response.status);
    }
    return response.text();
}

const urlParams = new URLSearchParams(window.location.search);
const post_file = urlParams.get('post');

const post = await getFileContent("/posts/" + post_file);

const content = marked.parse(post);
document.getElementById('content').innerHTML = content;
console.log(content);
