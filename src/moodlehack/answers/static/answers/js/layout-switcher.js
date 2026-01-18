/**
 * Layout switching and card expansion module.
 */
function initLayoutHandlers() {
  const container = document.getElementById("answers-container");
  const listBtn = document.getElementById("list-view-btn");
  const gridBtn = document.getElementById("grid-view-btn");

  const getCookie = (name) => {
    let parts = ("; " + document.cookie).split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
  };

  const applyView = (view) => {
    if (!container) return;

    if (view === "grid") {
      container.classList.remove("list-mode");
      container.classList.add("grid-mode");
      container.classList.remove("row-cols-1");
      container.classList.add("row-cols-1", "row-cols-md-2", "row-cols-xl-3");
      gridBtn?.classList.add("active");
      listBtn?.classList.remove("active");
    } else {
      container.classList.remove("grid-mode");
      container.classList.add("list-mode");
      container.classList.remove("row-cols-md-2", "row-cols-xl-3");
      container.classList.add("row-cols-1");
      listBtn?.classList.add("active");
      gridBtn?.classList.remove("active");
    }
  };

  // Re-bind click events to handle potential DOM updates
  listBtn?.replaceWith(listBtn.cloneNode(true));
  gridBtn?.replaceWith(gridBtn.cloneNode(true));

  document.getElementById("list-view-btn")?.addEventListener("click", () => {
    document.cookie = "answers_view=list; path=/; max-age=" + (30*24*60*60);
    applyView("list");
  });

  document.getElementById("grid-view-btn")?.addEventListener("click", () => {
    document.cookie = "answers_view=grid; path=/; max-age=" + (30*24*60*60);
    applyView("grid");
  });

  applyView(getCookie("answers_view") || "list");
}

// Initial initialization
document.addEventListener("DOMContentLoaded", initLayoutHandlers);

// Re-initialize after HTMX content swap
document.addEventListener("htmx:afterSwap", function(evt) {
    if (evt.detail.target.id === "answers") {
        initLayoutHandlers();
    }
});

// Global delegate for card expansion in grid mode
document.addEventListener("click", function(e) {
  const container = document.getElementById("answers-container");
  if (!container?.classList.contains("grid-mode")) return;

  const clickedCard = e.target.closest(".card");
  const isInteractive = e.target.closest("button") || e.target.closest("a") || e.target.classList.contains("bi");

  if (!clickedCard || isInteractive) {
    if (!isInteractive) {
      document.querySelectorAll('.card.expanded').forEach(c => c.classList.remove('expanded'));
    }
    return;
  }

  document.querySelectorAll('.card.expanded').forEach(c => {
    if (c !== clickedCard) c.classList.remove('expanded');
  });
  
  clickedCard.classList.toggle("expanded");
});
