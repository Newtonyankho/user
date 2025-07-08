// dashboard.js

// 🔁 Orientation-aware label display
function adjustLayoutByOrientation() {
  const isPortrait = window.matchMedia("(orientation: portrait)").matches;
  const navLinks = document.querySelectorAll(".main-nav li a");

  navLinks.forEach(link => {
    const label = link.getAttribute("data-label");
    const icon = link.getAttribute("data-icon");
    link.innerHTML = isPortrait ? icon : `${icon} <span>${label}</span>`;
  });
}

// 📤 Handle posting new content (optional, requires Flask POST setup)
function handlePostSubmit() {
  const postButton = document.querySelector(".post-box button");
  const postInput = document.querySelector(".post-box textarea");
  const feed = document.querySelector(".feed");

  postButton.addEventListener("click", () => {
    const content = postInput.value.trim();
    if (!content) return;

    // Create new post DOM element
    const newPost = document.createElement("div");
    newPost.classList.add("post");
    newPost.innerHTML = `
      <div class="post-header">
        <div class="post-author">You</div>
        <div class="post-time">Just now</div>
      </div>
      <div class="post-content">${content}</div>
      <div class="post-actions">
        <span>Like</span>
        <span>Comment</span>
        <span>Share</span>
      </div>
    `;

    feed.prepend(newPost); // Add to top of feed
    postInput.value = "";
  });
}

// 🧪 Toggle Welcome Section (optional)
document.getElementById("toggleButton")?.addEventListener("click", () => {
  document.querySelector(".welcome")?.classList.toggle("hidden");
});

// 🟢 Init on load
window.addEventListener("load", () => {
  adjustLayoutByOrientation();
  handlePostSubmit();
});

// 🔄 Re-check on resize/orientation change
window.addEventListener("resize", adjustLayoutByOrientation);

function updateNavLabels() {
  const isPortrait = window.matchMedia("(orientation: portrait)").matches;
  document.querySelectorAll('.main-nav a, .sidebar a').forEach(link => {
    const icon = link.getAttribute('data-icon');
    const label = link.getAttribute('data-label');
    if (isPortrait) {
      link.innerHTML = icon; // Show only icon
    } else {
      link.innerHTML = `${icon} <span>${label}</span>`; // Show icon + label
    }
  });
}

window.addEventListener('load', updateNavLabels);
window.addEventListener('resize', updateNavLabels);
