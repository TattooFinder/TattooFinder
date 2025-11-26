const screens = document.querySelectorAll(".screen");
const home = document.getElementById("homeScreen");
const login = document.getElementById("loginScreen");
const regClient = document.getElementById("registerClientScreen");
const regArtist = document.getElementById("registerArtistScreen");
const forgot = document.getElementById("forgotScreen");
const forgotSent = document.getElementById("forgotSentScreen");
const reset = document.getElementById("resetScreen");
const userType = document.getElementById("userType");
const loginBtn = document.getElementById("loginButton");
const registerBtn = document.getElementById("registerButton");
const backBtns = document.querySelectorAll("[id^='backHome']");
function show(target) {
  screens.forEach((el) => {
    el.classList.remove("active");
    el.classList.add("hidden");
  });
  target.classList.remove("hidden");
  setTimeout(() => target.classList.add("active"), 10);
}
function showById(id) {
  show(document.getElementById(id));
}
loginBtn.addEventListener("click", () => show(login));
registerBtn.addEventListener("click", () => {
  if (userType.value === "Tatuador") show(regArtist);
  else show(regClient);
});
backBtns.forEach((b) => b.addEventListener("click", () => show(home)));
function validarSenhas(s, c) {
  if (s !== c) {
    alert("As senhas não coincidem!");
    return false;
  }
  if (s.length < 8) {
    alert("A senha deve ter pelo menos 8 caracteres!");
    return false;
  }
  return true;
}
document
  .getElementById("registerClientForm")
  .addEventListener("submit", (e) => {
    e.preventDefault();
    if (!validarSenhas(clientSenha.value, clientConfirmar.value)) return;
    
    const nome = document.getElementById("clientNome").value;
    const cidade = document.getElementById("clientCidade").value;
    const email = document.getElementById("clientEmail").value;
    const senha = document.getElementById("clientSenha").value;

    fetch("/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ nome, cidade, email, senha, role: "cliente" }),
    })
      .then(response => {
          if (!response.ok) {
              return response.json().then(err => {
                  throw new Error(err.error || 'Erro no servidor');
              });
          }
          return response.json();
      })
      .then((data) => {
        if (data.message) {
          alert("Cadastro de cliente enviado com sucesso!");
          show(home);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert(error.message);
      });
  });
document
  .getElementById("registerArtistForm")
  .addEventListener("submit", (e) => {
    e.preventDefault();
    if (!validarSenhas(artistSenha.value, artistConfirmar.value)) return;

    const nome = document.getElementById("artistNome").value;
    const cidade = document.getElementById("artistCidade").value;
    const email = document.getElementById("artistEmail").value;
    const senha = document.getElementById("artistSenha").value;

    fetch("/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ nome, cidade, email, senha, role: "tatuador" }),
    })
      .then(response => {
          if (!response.ok) {
              return response.json().then(err => {
                  throw new Error(err.error || 'Erro no servidor');
              });
          }
          return response.json();
      })
      .then((data) => {
        if (data.message) {
          alert("Cadastro de tatuador enviado com sucesso!");
          show(home);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert(error.message);
      });
  });
document.getElementById("loginForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const email = loginEmail.value;
  const senha = loginSenha.value;
  if (!email || !senha) return alert("Preencha todos os campos!");
  if (!email.includes("@")) return alert("Email inválido!");

  fetch("/api/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, senha }),
  })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.error || 'Erro no servidor');
            });
        }
        return response.json();
    })
    .then((data) => {
      if (data.message) { // Verifica a mensagem de sucesso
        window.location.href = "user.html"; // Redireciona para a página do usuário
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert(error.message);
    });
});
document.getElementById("forgotLink").addEventListener("click", () => {
  const emailLogin = document.getElementById("loginEmail").value || "";
  document.getElementById("forgotEmail").value = emailLogin;
  show(forgot);
});
document
  .getElementById("forgotBack")
  .addEventListener("click", () => show(login));
document.getElementById("forgotForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const email = document.getElementById("forgotEmail").value.trim();
  if (!email || !email.includes("@"))
    return alert("Informe um e-mail válido.");
  show(forgotSent);
});
document
  .getElementById("forgotSentBack")
  .addEventListener("click", () => show(login));
document
  .getElementById("openResetDirect")
  .addEventListener("click", () => show(reset));
document.getElementById("resetForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const s1 = document.getElementById("newPass").value;
  const s2 = document.getElementById("newPassConfirm").value;
  if (!validarSenhas(s1, s2)) return;
  alert("Senha redefinida com sucesso! Faça login novamente.");
  show(login);
});
document
  .getElementById("resetBack")
  .addEventListener("click", () => show(login));
(function bootFromURL() {
  const params = new URLSearchParams(location.search);
  if (params.get("resetToken")) {
    show(reset);
  }
})();
