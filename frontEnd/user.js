document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/api/profile", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include", // Envia os cookies de autenticação
    });

    if (response.status === 401) {
      // Não autorizado (token inválido ou expirado)
      // Redireciona para a página de login
      window.location.href = "index.html";
      return;
    }

    if (!response.ok) {
      // Outros erros de servidor
      throw new Error("Falha ao buscar dados do perfil.");
    }

    const userData = await response.json();

    // Preenche os dados na página
    const userName = document.getElementById("user-name");
    const userEmail = document.getElementById("user-email");
    const userLocation = document.getElementById("user-location");

    if (userName) {
      userName.textContent = userData.nome || "Nome não encontrado";
    }
    if (userEmail) {
      userEmail.textContent = userData.email || "";
    }
    if (userLocation) {
      userLocation.textContent = `📍 ${userData.cidade}` || "";
    }
  } catch (error) {
    console.error("Erro ao carregar o perfil:", error);
    // Opcional: mostrar uma mensagem de erro na tela
    const userName = document.getElementById("user-name");
    if (userName) {
      userName.textContent = "Erro ao carregar perfil";
    }
    // Opcional: redirecionar para o login após um tempo
    // setTimeout(() => { window.location.href = '/index.html'; }, 3000);
  }
});
