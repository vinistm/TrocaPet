function verificarSenha() {
  const senha = document.getElementById("senha").value;
  const barraSenha = document.getElementById("barra-senha");
  const textoSenha = document.getElementById("texto-senha");
  const forcaSenha = document.getElementById("forca-senha");
  const requisitosSenha = document.getElementById("requisitos-senha");

  let forca = 0;
  if (senha.length >= 8) {
    forca++;
  }

  if (senha.match(/[a-z]/) && senha.match(/[A-Z]/)) {
    forca++;
  }
  if (senha.match(/\d+/)) {
    forca++;
  }
  if (senha.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,(,)]/)) {
    forca++;
  }

  switch (forca) {
    case 0:
      barraSenha.style.width = "0%";
      forcaSenha.style.backgroundColor = "red";
      break;
    case 1:
      barraSenha.style.width = "25%";
      forcaSenha.style.backgroundColor = "red";
      break;
    case 2:
      barraSenha.style.width = "50%";
      forcaSenha.style.backgroundColor = "orange";
      break;
    case 3:
      barraSenha.style.width = "75%";
      forcaSenha.style.backgroundColor = "green";
      break;
    case 4:
      barraSenha.style.width = "100%";
      forcaSenha.style.backgroundColor = "blue";
      break;
  }

  let requisitos = "";
  if (!senha.match(/[A-Z]/)) {
    requisitos += "• Uma letra maiúscula<br>";
  }
  if (!senha.match(/\d+/)) {
    requisitos += "• Um número<br>";
  }
  if (!senha.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,(,)]/)) {
    requisitos += "• Um caractere especial<br>";
  }

  if (requisitos) {
    requisitosSenha.innerHTML = "Para uma senha forte:<br>" + requisitos;
  } else {
    requisitosSenha.textContent = "Senha forte!";
  }
}
