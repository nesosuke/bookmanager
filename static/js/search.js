const baseurl = 'http://172.22.242.210:8080';
const apiBaseUrl = baseurl+'/api/v1';

async function searchByTitle() {
    const query = document.forms.booksearch.query.value;
    const url = apiBaseUrl + '/book/search?title=' + query;
    const responseData = await fetch(url).then(response => response.json());
    console.log(responseData)

    responseData.forEach(data => {
        const title = data['title'];
        const isbn = data['isbn'];

        const html = `
    <tr>
    <td>${title}</td>
    <td>${isbn}</td>
    </tr>`;

        table.insertAdjacentHTML("beforeend", html);

    });
}


    // //  insert json to HTML
    // for (let i = 0; i < responseData.length; i++) {
    //     console.log(responseData[i].title);

    //     const booktitle = responseData[i].title;
    //     const bookisbn = responseData[i].isbn;
    //     document.getElementById('booktitle').textContent += booktitle;
    //     document.getElementById('isbn').textContent += bookisbn;

    //     const table = document.createElement('table');

    //     responseData.forEach((data) => {
    //         const tr = document.createElement('tr')
    //         Object.entries(data).forEach(([key, val]) => {
    //             const td = document.createElement('td');
    //             const text = document.createTextNode(val);
    //             td.appendChild(text);
    //             tr.appendChild(td)
    //         })
    //         table.appendChild(tr)
    //     })

    // }

