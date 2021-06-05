const baseurl = 'http://localhost:5000';
async function findBookinfo() {
    const isbn = document.forms.inputISBN.isbn.value;
    const url = baseurl + '/book/' + isbn;
    const bookinfo = await fetch(url).then(response => response.json());

    const title = bookinfo['title'];
    const bookisbn = bookinfo['isbn'];
    document.getElementById('booktitle').textContent = title;
    document.getElementById('bookisbn').textContent = bookisbn;
}

async function updateReadingStatus() {
    let status = document.forms.updateStatus.status.value;
    if (status === '') {
        alert('input status');
        return;
    }

    const isbn = document.getElementById('bookisbn').textContent // TODO: DOMから取るのをやめる．
    const uid = 'neso'
    let url = baseurl + '/status'
    if (typeof isbn == 'string') {
        const XHR = new XMLHttpRequest();
        const encodedUrl = baseurl + '/status' + '?' + 'isbn=' + isbn + '&status=' + status + '&uid=' + uid;

        XHR.open('POST', encodedUrl);
        XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        XHR.send(encodedUrl);

        url = url + '?isbn=' + isbn + '&uid=' + uid;
        const data = await fetch(url).then(response => response.json());
        status = data['status'];
        console.log(status);
        document.getElementById('status').textContent = status;
    }
    else {
        alert('input valid ISBN!')
    }
}

async function fetchReadingStatus() {
    const isbn = document.forms.inputISBN.isbn.value;
    const uid = 'neso';
    const url = baseurl + '/status' + '?isbn=' + isbn + '\&uid=' + uid;
    const responseData = await fetch(url).then(response => response.json());

    const status = responseData['status']
    document.getElementById('status').textContent = status;

}

function handleOnClick() {
    Promise.all([findBookinfo(), fetchReadingStatus()]).then((values) => { console.log(values) });
}