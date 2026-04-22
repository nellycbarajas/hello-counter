// hello-counter frontend — vanilla JS, no framework.

const $value = document.getElementById("counter-value");
const $button = document.getElementById("increment-btn");
const $toast = document.getElementById("toast");
const $toastMsg = document.getElementById("toast-msg");
const $toastDismiss = document.getElementById("toast-dismiss");

let toastTimer = null;

function showToast(message) {
  $toastMsg.textContent = message;
  $toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => ($toast.hidden = true), 4000);
}

$toastDismiss.addEventListener("click", () => {
  $toast.hidden = true;
  clearTimeout(toastTimer);
});

async function loadCount() {
  try {
    const res = await fetch("/count");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    $value.textContent = String(data.value);
  } catch (err) {
    console.error("loadCount failed", err);
    showToast("Counter unavailable — try again");
    $value.textContent = "—";
  }
}

async function increment() {
  $button.disabled = true;
  try {
    const res = await fetch("/increment", { method: "POST" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    $value.textContent = String(data.value);
  } catch (err) {
    console.error("increment failed", err);
    showToast("Counter unavailable — try again");
  } finally {
    $button.disabled = false;
  }
}

$button.addEventListener("click", increment);

loadCount();
