import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

let main_page;
await fetch('./main_page.en.md')
    .then(response => {
        if (!response.ok) throw new Error('Network response not ok: ' + response.status);
        return response.text();
    })
    .then(data => {
        main_page = data;
    })
    .catch(error => {
        alert('Critical error: Could not load required file. The site cannot continue.');
        document.body.innerHTML = '<h1>Site unavailable</h1><p>Please try again later.</p>';

        window.location.reload();
        // window.location.href = 'error.html';
        
        throw error; 
    });

content = marked.parse(main_page);
document.getElementById('content').innerHTML = content;
console.log(content);
