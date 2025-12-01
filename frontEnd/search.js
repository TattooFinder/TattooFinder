document.addEventListener("DOMContentLoaded", () => {
  const pageSearchForm = document.getElementById("pageSearchForm");
  const pageSearchQuery = document.getElementById("pageSearchQuery");
  const headerSearchForm = document.getElementById("headerSearchForm");
  const resultsGrid = document.getElementById("results-grid");
  const resultsSection = document.getElementById("results-section");

  const placeholderImage = "/pics/artist-placeholder.jpeg"; // Caminho para a imagem placeholder

  // Função que executa a busca
  const performSearch = async (query) => {
    if (!query || !query.trim()) {
      return;
    }

    try {
      const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
      if (!response.ok) {
        throw new Error("A requisição para a busca falhou.");
      }
      const artists = await response.json();
      displayResults(artists);
    } catch (error) {
      console.error("Erro ao buscar:", error);
      resultsGrid.innerHTML = "<p>Ocorreu um erro ao realizar a busca. Tente novamente.</p>";
    }
  };

  // Função que exibe os resultados na tela
  const displayResults = (artists) => {
    resultsGrid.innerHTML = ""; // Limpa resultados anteriores

    if (artists.length === 0) {
      resultsGrid.innerHTML = "<p>Nenhum artista encontrado para esta busca.</p>";
      return;
    }

    artists.forEach((artist) => {
      const card = document.createElement("div");
      card.className = "artist-card-result";

      const imageUrl = artist.foto_url ? `/${artist.foto_url}` : placeholderImage;
      const styles = artist.estilos ? artist.estilos.split(',').map(s => `<span class="tag">${s.trim()}</span>`).join('') : '<span>Nenhum estilo</span>';

      card.innerHTML = `
        <a href="/tattooer/${artist.id_tatuador}">
          <img src="${imageUrl}" alt="Foto de ${artist.nome}" class="artist-photo">
          <div class="artist-info">
            <h3>${artist.nome}</h3>
            <p class="location">📍 ${artist.cidade}</p>
            <div class="styles-tags">
              ${styles}
            </div>
          </div>
        </a>
      `;
      resultsGrid.appendChild(card);
    });
  };

  // Adiciona evento ao formulário de busca da página
  if (pageSearchForm) {
    pageSearchForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const query = pageSearchQuery.value;
      // Atualiza o URL sem recarregar a página para que o usuário possa compartilhar o link
      window.history.pushState({}, '', `?q=${encodeURIComponent(query)}`);
      performSearch(query);
    });
  }

  // Adiciona evento ao formulário de busca do cabeçalho
  if (headerSearchForm) {
    headerSearchForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const query = document.getElementById("headerSearchQuery").value;
      window.location.href = `/search?q=${encodeURIComponent(query)}`;
    });
  }

  // Verifica se há um parâmetro 'q' na URL quando a página carrega
  const searchParams = new URLSearchParams(window.location.search);
  const initialQuery = searchParams.get("q");
  if (initialQuery) {
    pageSearchQuery.value = initialQuery;
    performSearch(initialQuery);
  }
});
