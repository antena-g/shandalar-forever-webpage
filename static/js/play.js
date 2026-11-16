const frame = document.getElementById('game-frame');
const cover = document.getElementById('game-cover');
const launch = document.getElementById('game-launch');
const status = document.getElementById('game-status');
const size = document.getElementById('game-size');
let startupTimer;

function showFailure() {
  clearTimeout(startupTimer);
  status.textContent = 'Could not start the game. Try again, or use a desktop browser with WebGL 2 enabled.';
  frame.hidden = true;
  frame.src = 'about:blank';
  cover.hidden = false;
  launch.disabled = false;
  launch.textContent = 'Try again';
}

function showGameWindow() {
  const top = document.querySelector('.game-window').getBoundingClientRect().top + window.scrollY;
  const header = document.querySelector('.site-header').getBoundingClientRect().height;
  window.scrollTo({ top: top - header - 12, behavior: 'instant' });
}

launch.addEventListener('click', () => {
  launch.disabled = true;
  cover.hidden = true;
  frame.hidden = false;
  status.textContent = 'Loading the game… This can take a moment on the first visit.';
  startupTimer = setTimeout(showFailure, 120000);
  frame.src = frame.dataset.src;
  showGameWindow();
});

window.addEventListener('message', event => {
  if (event.origin !== location.origin || event.source !== frame.contentWindow) return;
  if (event.data?.type === 'shandalar-ready') {
    clearTimeout(startupTimer);
    status.textContent = 'Game ready. Click inside to play.';
  } else if (event.data?.type === 'shandalar-error') {
    showFailure();
  }
});

size.addEventListener('click', () => {
  const expanded = document.body.classList.toggle('play-page--wide');
  size.setAttribute('aria-pressed', String(expanded));
  size.textContent = expanded ? 'Standard view' : 'Larger view';
  showGameWindow();
});
