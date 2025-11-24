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
});
