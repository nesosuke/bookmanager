const apiBaseUrl = 'http://localhost:8080/api/v1';
async function findBookinfo() {
    const isbn = document.forms.inputISBN.isbn.value;
    const url = apiBaseUrl + '/book/' + isbn;
    const bookinfo = await fetch(url).then(response => response.json());

    const title = bookinfo['title'];
    const bookisbn = bookinfo['isbn'];
    document.getElementById('booktitle').textContent = title;
    document.getElementById('bookisbn').textContent = bookisbn;
}

async function updateReadingStatus() {
    const status = document.forms.updateStatus.status.value;
    const isbn = document.getElementById('bookisbn').textContent
    const username = 'neso'
    const url = apiBaseUrl + '/record'
    // curl POST json data
    const data = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            isbn: isbn,
            username: username,
            status: status
        })
    }).then(response => response.json());
    console.log(data)
}

async function fetchReadingStatus() {
    const isbn = document.forms.inputISBN.isbn.value;
    const username = 'neso';
    const url = apiBaseUrl + '/user/' + username + '/' + isbn
    const responseData = await fetch(url).then(response => response.json());

    const status = responseData['status']
    document.getElementById('status').textContent = status;
    console.log(responseData)
}

function handleOnClick() {
    Promise.all([findBookinfo(), fetchReadingStatus()]).then((values) => { console.log(values) });
}