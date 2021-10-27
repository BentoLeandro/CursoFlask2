console.log('esta carregando o script bento Leandro Reis');

$('form input[type="file"]').change(event => {
    console.log('entrou na rotina...');
    let arquivos = event.target.files;
    if (arquivos.length === 0) {
      console.log('sem imagem pra mostrar')
    } else {
        if(arquivos[0].type == 'image/jpeg') {
          $('img').remove();
          let imagem = $('<img class="img-responsive">');
          imagem.attr('src', window.URL.createObjectURL(arquivos[0]));
          $('figure').prepend(imagem);
        } else {
          alert('Formato não suportado')
        }
    }
  });
