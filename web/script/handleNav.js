var handleNav = document.getElementsByClassName('handle-nav')[0];

handleNav.addEventListener('click', function() {
  var ul = document.getElementsByTagName('ul')[0];
  
  if (!ul.classList.contains('nav-open')) {
    ul.classList.add('nav-open');
  } else {
    ul.classList.remove('nav-open');
  }
});

// fetch('http://127.0.0.1:5000/linha_de_onibus', {
//   method: 'POST',
//   headers: {
//     'Content-Type': 'application/json'
//   },
//   body: JSON.stringify({
//     destino: 'a',
//     hora_de_partida: 'a',
//     preco_passagem: 'a',
//     capacidade_de_assento: 'a',
//     assentos_disponiveis: 'a',
//   })
// })
// .then(response => response.json())
// .then(data => console.log(data))
// .catch(error => console.error(error))
