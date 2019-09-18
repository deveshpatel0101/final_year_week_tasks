var count = 0;

function postData() {
  if (count > 100) {
    return;
  }
  fetch('http://localhost:5000/nlps/entities', {
    method: 'POST',
    headers: {
      Authorization:
        'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRlc3RpbmcxMkBnbWFpbC5jb20iLCJhbGxvd2VkX2FwaXMiOlsidHJhbnNsYXRvciIsImVudGl0aWVzIl0sImFwcF9uYW1lIjoiZmlyc3RfYXBwIn0.yChy7CFHST4qr-Tls-bOPzesu1hHhqylwpB3Q3MJJKg',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: 'Apple was founded by late Steve Jobs.',
    }),
  })
    .then((res) => {
      count++;
      return res.json();
    })
    .then((data) => {
      console.log(count, data);
    });
}

setInterval(postData, 600);
