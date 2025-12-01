document.addEventListener("DOMContentLoaded", async () => {
  const pathParts = window.location.pathname.split("/");
  const isGenericTattooerPage = pathParts.length === 2 && pathParts[1] === "tattooer";
  const isSpecificTattooerPage = pathParts.length === 3 && pathParts[1] === "tattooer";
  const tatuadorIdFromUrl = isSpecificTattooerPage ? pathParts[2] : null;

  // --- Elementos de exibição ---
  const artistNameEl = document.getElementById("artist-name");
  const artistLocationEl = document.getElementById("artist-location");
  const artistEmailEl = document.getElementById("artist-email");
  const artistPhoneEl = document.getElementById("artist-phone");
  const artistDescriptionEl = document.getElementById("artist-description");
  const profilePicEl = document.getElementById("profile-pic");
  const artistTagsEl = document.querySelector(".artist-tags");
  const editBtn = document.getElementById("editBtn");
  const contactBtn = document.querySelector(".btn-primary");

  // --- Modal e formulário ---
  const modal = document.getElementById("editModal");
  const closeSpan = document.querySelector(".close-modal");
  const cancelBtn = document.getElementById("cancelBtn");
  const profileForm = document.getElementById("profileForm");

  // --- Campos do formulário ---
  const inputName = document.getElementById("editName");
  const inputEmail = document.getElementById("editEmail");
  const inputLocation = document.getElementById("editLocation");
  const inputDescription = document.getElementById("editDescription");
  const inputStyles = document.getElementById("editStyles");
  const inputPhones = document.getElementById("editPhones");
  const inputPhoto = document.getElementById("editPhoto");
  const uploadBtn = document.getElementById("uploadBtn");
  const fileNameSpan = document.querySelector(".file-name");

  let loggedInUser = null;
  let currentProfileData = {};

  async function getLoggedInUser() {
    try {
      const response = await fetch("/api/perfil", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
      });
      if (response.ok) {
        loggedInUser = await response.json();
      }
    } catch (error) {
      console.error("Não foi possível verificar o usuário logado.", error);
    }
  }

  function displayProfileData(artistData) {
    currentProfileData = artistData;

    artistNameEl.childNodes[0].nodeValue = artistData.nome || "Nome não disponível";
    artistLocationEl.textContent = artistData.cidade ? `📍 ${artistData.cidade}` : "";
    artistEmailEl.textContent = artistData.email ? `✉️ ${artistData.email}` : "";
    artistPhoneEl.textContent = artistData.telefones ? `📞 ${artistData.telefones}` : "";
    artistDescriptionEl.textContent = artistData.descricao || "Nenhuma descrição disponível.";
    if (artistData.foto_url) {
      profilePicEl.src = `/${artistData.foto_url.replace(/\\/g, "/")}`;
    }

    artistTagsEl.innerHTML = '';
    if (artistData.estilos) {
      artistData.estilos.split(',').forEach(styleName => {
        const style = styleName.trim();
        if (style) {
          const tag = document.createElement('span');
          tag.className = 'tag';
          tag.textContent = style;
          artistTagsEl.appendChild(tag);
        }
      });
    }
  }

  async function loadProfile() {
    await getLoggedInUser();
    let profileDataUrl = "";
    
    if (isGenericTattooerPage) {
      if (loggedInUser && loggedInUser.role === 'tatuador') {
        profileDataUrl = "/api/perfil";
        editBtn.style.display = "block";
        contactBtn.style.display = "none";
      } else {
        artistNameEl.textContent = "Perfil não encontrado ou acesso negado.";
        editBtn.style.display = "none";
        return;
      }
    } else if (isSpecificTattooerPage) {
      profileDataUrl = `/tatuador/${tatuadorIdFromUrl}`;
      if (loggedInUser && loggedInUser.role === 'tatuador' && loggedInUser.id.toString() === tatuadorIdFromUrl) {
        editBtn.style.display = "block";
        contactBtn.style.display = "none";
      } else {
        editBtn.style.display = "none";
      }
    } else {
      return; 
    }

    try {
      const response = await fetch(profileDataUrl, { credentials: "include" });
      if (!response.ok) throw new Error("Falha ao carregar dados do perfil.");
      const artistData = await response.json();
      displayProfileData(artistData);
    } catch (error) {
      console.error("Erro:", error);
      artistNameEl.textContent = "Erro ao carregar perfil";
    }
  }

  function openModal() {
    inputName.value = currentProfileData.nome || '';
    inputEmail.value = currentProfileData.email || '';
    inputLocation.value = currentProfileData.cidade || '';
    inputDescription.value = currentProfileData.descricao || '';
    inputStyles.value = currentProfileData.estilos || '';
    inputPhones.value = currentProfileData.telefones || '';
    inputPhoto.value = "";
    fileNameSpan.textContent = "Nenhum arquivo selecionado";
    modal.style.display = "flex";
  }

  function closeModal() {
    modal.style.display = "none";
  }

  editBtn.addEventListener("click", openModal);
  closeSpan.addEventListener("click", closeModal);
  cancelBtn.addEventListener("click", closeModal);
  window.addEventListener("click", (event) => {
    if (event.target === modal) closeModal();
  });

  uploadBtn.addEventListener("click", () => inputPhoto.click());
  inputPhoto.addEventListener("change", () => {
    fileNameSpan.textContent = inputPhoto.files.length > 0 ? inputPhoto.files[0].name : "Nenhum arquivo selecionado";
  });

  profileForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("nome", inputName.value);
    formData.append("email", inputEmail.value);
    formData.append("cidade", inputLocation.value);
    formData.append("descricao", inputDescription.value);
    formData.append("estilos", inputStyles.value);
    formData.append("telefones", inputPhones.value);
    if (inputPhoto.files.length > 0) {
      formData.append("photo", inputPhoto.files[0]);
    }

    try {
      const response = await fetch("/api/perfil", {
        method: "POST",
        credentials: "include",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Falha ao atualizar o perfil.");
      }
      
      const updatedProfile = await response.json();
      displayProfileData(updatedProfile);
      closeModal();
      alert("Perfil atualizado com sucesso!");

    } catch (error) {
      console.error("Erro ao atualizar:", error);
      alert(`Erro: ${error.message}`);
    }
  });

  loadProfile();
});