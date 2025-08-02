
const blogList = document.getElementById('post-list');
const content = document.getElementById('content');

const browser_lang = navigator.language.split('-')[0];

const getFileContent = async (file_name) => {
    const response = await fetch(file_name);
    if(!response.ok) {
        throw new Error("Response not OK: " + response.status);
    }
    return response.text();
};

const posts = JSON.parse(await getFileContent('/posts.json'));

posts.forEach(post => {
    // console.log(post.title + ': ' + post.description);
    if(post.lang != browser_lang) {
        return;
    }
    const li = document.createElement('li');
    li.innerHTML = `<h3>
        ${post.title}
    </h3>
    <p>
        ${post.description}
    </p>`;
    // for(let i = 0; i < 10; i++) {
    //     console.log(i);
    //     blogList.innerHTML += (li).outerHTML;
    // }
    blogList.appendChild(li)
});
