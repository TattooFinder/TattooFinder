document.addEventListener("DOMContentLoaded", async () => {
  // Elementos de exibição do perfil
  const userNameEl = document.getElementById("user-name");
  const userEmailEl = document.getElementById("user-email");
  const userLocationEl = document.getElementById("user-location");
  const profilePic = document.querySelector(".profile-pic");

  // Modal e formulário
  const modal = document.getElementById("editModal");
  const editBtn = document.getElementById("editBtn");
  const closeSpan = document.querySelector(".close-modal");
  const cancelBtn = document.getElementById("cancelBtn");
  const profileForm = document.getElementById("profileForm");

  // Campos do formulário
  const inputName = document.getElementById("editName");
  const inputEmail = document.getElementById("editEmail");
  const inputLocation = document.getElementById("editLocation");
  const inputPhoto = document.getElementById("editPhoto");

  // Função para carregar dados do perfil
  async function loadProfileData() {
    try {
      const response = await fetch("/api/profile", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // Envia os cookies de autenticação
      });

      if (response.status === 401) {
        window.location.href = "index.html";
        return;
      }
      if (!response.ok) {
        throw new Error("Falha ao buscar dados do perfil.");
      }

      const userData = await response.json();

      // Preenche os dados na página
      if (userNameEl) userNameEl.textContent = userData.nome || "Nome não encontrado";
      if (userEmailEl) userEmailEl.textContent = userData.email || "";
      if (userLocationEl) userLocationEl.textContent = userData.cidade ? `📍 ${userData.cidade}` : "";
      // Adicionar lógica para foto de perfil se existir no back-end
      // if (profilePic && userData.foto_url) profilePic.src = userData.foto_url;

    } catch (error) {
      console.error("Erro ao carregar o perfil:", error);
      if (userNameEl) userNameEl.textContent = "Erro ao carregar perfil";
    }
  }

  // Funções do Modal
  function openModal() {
    // Preenche o formulário com os dados atuais da página
    inputName.value = userNameEl.textContent;
    inputEmail.value = userEmailEl.textContent;
    inputLocation.value = userLocationEl.textContent.replace("📍 ", "");
    inputPhoto.value = ""; // Limpa o campo de foto

    modal.style.display = "flex";
  }

  function closeModal() {
    modal.style.display = "none";
  }

  // Event Listeners
  editBtn.addEventListener("click", openModal);
  closeSpan.addEventListener("click", closeModal);
  cancelBtn.addEventListener("click", closeModal);
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });

  profileForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const updatedData = {
      nome: inputName.value,
      email: inputEmail.value,
      cidade: inputLocation.value,
      foto_url: inputPhoto.value.trim() || null
    };

    try {
        const response = await fetch("/api/profile", {
            method: "POST", // ou 'PUT', dependendo da sua API
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(updatedData),
        });

        if (!response.ok) {
            throw new Error("Falha ao atualizar o perfil.");
        }

        const result = await response.json();

        // Atualiza a página com os novos dados
        userNameEl.textContent = result.nome;
        userEmailEl.textContent = result.email;
        userLocationEl.textContent = `📍 ${result.cidade}`;
        if (result.foto_url) {
            profilePic.src = result.foto_url;
        }

        closeModal();
        alert("Perfil atualizado com sucesso!");

    } catch (error) {
        console.error("Erro ao atualizar perfil:", error);
        alert("Ocorreu um erro ao atualizar o perfil. Tente novamente.");
    }
  });

  // Carrega os dados do perfil ao iniciar a página
  await loadProfileData();
});
