// Bestiary: show a card when its name is hovered, focused or tapped.

const popup = document.querySelector("[data-card-peek]");
const GAP = 12; // Pixels between the card name and the popup.
let shownFor = null;

function show(button) {
  const card = button.nextElementSibling.content.cloneNode(true);
  popup.replaceChildren(card);
  popup.hidden = false;
  shownFor = button;
  place(button);
}

function hide() {
  popup.hidden = true;
  shownFor = null;
}

// Put the popup beside the name, on whichever side has room, inside the window.
function place(button) {
  const name = button.getBoundingClientRect();
  const width = popup.offsetWidth;
  const height = popup.offsetHeight;

  let left = name.right + GAP;
  if (left + width > window.innerWidth - GAP) left = name.left - width - GAP;
  left = Math.max(GAP, left);

  const top = Math.min(
    Math.max(GAP, name.top + name.height / 2 - height / 2),
    window.innerHeight - height - GAP,
  );

  popup.style.left = `${left}px`;
  popup.style.top = `${top}px`;
}

for (const button of document.querySelectorAll(".card-peek")) {
  button.addEventListener("mouseenter", () => show(button));
  button.addEventListener("mouseleave", hide);
  button.addEventListener("focus", () => show(button));
  button.addEventListener("blur", hide);
  // On touch screens there is no hover: a tap shows the card...
  button.addEventListener("click", () => show(button));
}

// ...and a tap anywhere else hides it.
document.addEventListener("click", (event) => {
  if (shownFor && !event.target.closest(".card-peek")) hide();
});

window.addEventListener("scroll", hide, { passive: true });
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") hide();
});
