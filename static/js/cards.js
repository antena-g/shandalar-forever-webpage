// Card archive: filter the grid and show a card up close in a dialog.

const filters = document.querySelector("[data-card-filters]");
const items = [...document.querySelectorAll("[data-card-grid] > li")];
const count = document.querySelector("[data-card-count]");
const empty = document.querySelector("[data-card-empty]");

function applyFilters() {
  const query = filters.elements.query.value.trim().toLowerCase();
  const color = filters.elements.color.value;
  const type = filters.elements.type.value;

  let shown = 0;
  for (const item of items) {
    const matches =
      (!query || item.dataset.name.includes(query) || item.dataset.rules.includes(query)) &&
      (!color || item.dataset.color === color) &&
      (!type || item.dataset.type === type);
    item.hidden = !matches;
    if (matches) shown += 1;
  }

  count.textContent = `${shown} of ${items.length} cards`;
  empty.hidden = shown > 0;
}

filters.addEventListener("input", applyFilters);
filters.addEventListener("submit", (event) => event.preventDefault());

const dialog = document.querySelector("[data-card-dialog]");
const dialogCard = dialog.querySelector("[data-dialog-card]");
const dialogFlavor = dialog.querySelector("[data-dialog-flavor]");

function showCard(button) {
  const card = button.querySelector(".card").cloneNode(true);

  const flavor = button.parentElement.querySelector(".card-flavor");
  dialogFlavor.textContent = flavor ? flavor.content.textContent : "";
  dialogFlavor.hidden = !flavor;

  dialogCard.replaceChildren(card);
  dialog.showModal();
}

document.querySelector("[data-card-grid]").addEventListener("click", (event) => {
  const button = event.target.closest(".card-button");
  if (button) showCard(button);
});

// Clicking the dark backdrop around the dialog closes it.
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});
