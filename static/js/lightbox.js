// Screenshots: open a screenshot in an overlay instead of a new page.

const lightbox = document.querySelector("[data-lightbox]");
const lightboxImage = lightbox.querySelector("img");
const lightboxCaption = lightbox.querySelector("figcaption");

for (const link of document.querySelectorAll("[data-lightbox-link]")) {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    lightboxImage.src = link.href;
    lightboxImage.alt = link.dataset.caption;
    lightboxCaption.textContent = link.dataset.caption;
    lightbox.showModal();
  });
}

// Clicking the dark backdrop around the screenshot closes it.
lightbox.addEventListener("click", (event) => {
  if (event.target === lightbox) lightbox.close();
});
