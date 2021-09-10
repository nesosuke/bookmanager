const baseUrl = "http://localhost:8080/api/v1/book/search";
function getIsbnfromNDL(query) {
  const moreurl = baseUrl + "/more?title=" + query;
  const responseData = fetch(moreurl).then((response) => response.json());
  return responseData;
}

async function searchByTitle() {
  const query = document.forms.booksearch.query.value;
  const url = baseUrl + "?title=" + query;
  let responseData = await fetch(url).then((response) => response.json());
  console.log(responseData.length);

  if (responseData.length < 20) {
    responseData = await getIsbnfromNDL(query);
  }
  responseData.forEach((data) => {
    const title = data["title"];
    const isbn = data["isbn"];

    const html = `
    <tr>
    <td>${title}</td>
    <td>${isbn}</td>
    </tr>`;

    table.insertAdjacentHTML("beforeend", html);
  });
}
