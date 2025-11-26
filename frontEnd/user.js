<<<<<<< HEAD
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
=======
document.addEventListener("DOMContentLoaded", () => {
  const profileName = document.querySelector(".name-section h1");
  const profileEmail = document.querySelector(".email");
  const profileLocation = document.querySelector(".location");
  const profilePic = document.querySelector(".profile-pic");

  const modal = document.getElementById("editModal");
  const editBtn = document.getElementById("editBtn");
  const closeSpan = document.querySelector(".close-modal");
  const cancelBtn = document.getElementById("cancelBtn");
  const profileForm = document.getElementById("profileForm");

  const inputName = document.getElementById("editName");
  const inputEmail = document.getElementById("editEmail");
  const inputLocation = document.getElementById("editLocation");
  const inputPhoto = document.getElementById("editPhoto");

  editBtn.addEventListener("click", () => {
    inputName.value = profileName.textContent;
    inputEmail.value = profileEmail.textContent;
    inputLocation.value = profileLocation.textContent.replace("📍 ", "");
    inputPhoto.value = "";

    modal.style.display = "flex";
  });

  function closeModal() {
    modal.style.display = "none";
  }

  closeSpan.addEventListener("click", closeModal);
  cancelBtn.addEventListener("click", closeModal);
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });

  profileForm.addEventListener("submit", (e) => {
    e.preventDefault();
    profileName.textContent = inputName.value;
    profileEmail.textContent = inputEmail.value;

    let newLoc = inputLocation.value;
    if (!newLoc.includes("📍")) {
      newLoc = "📍 " + newLoc;
    }
    profileLocation.textContent = newLoc;

    if (inputPhoto.value.trim() !== "") {
      profilePic.src = inputPhoto.value;
    }
    closeModal();
    alert("Perfil atualizado com sucesso!");
  });
>>>>>>> 69dc3c874265538bf8612a9eb7704ab1898e8b6b
});
