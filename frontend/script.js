const API_BASE = "http://127.0.0.1:8000";

function addMessage(text, sender = "bot") {
  const chatBox = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.innerText = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function addResults(results, explanation) {
  const chatBox = document.getElementById("chat-box");

const row = document.createElement("div");
row.className = "results-row";

results.forEach(item => {
  const card = document.createElement("div");
  card.className = "jewel-card";
  card.innerHTML = `
    <img src="${API_BASE}/images/${item.image_path}" />
    <p><strong>Category:</strong> ${item.category}</p>
  `;
  row.appendChild(card);
});

chatBox.appendChild(row);
chatBox.scrollTop = chatBox.scrollHeight;
}

window.onload = () => {
  addMessage(
    "👋 Hi! I’m your jewellery assistant.\n" +
    "Search using text, image, voice, or handwriting 💍📿",
    "bot"
  );
};

function showResults(data) {
  if (data.type === "chat") {
    addMessage(data.message, "bot");
    return;
  }

  if (!data.results || data.results.length === 0) {
    addMessage("😕 I couldn’t find matching designs.", "bot");
    return;
  }

  addResults(data.results, data.explanation);
}

// TEXT
async function sendText() {
  const input = document.getElementById("textInput");
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  });

  showResults(await res.json());
}

// IMAGE
async function sendImage() {
  const file = document.getElementById("imageInput").files[0];
  if (!file) return;

  addMessage("📷 Image uploaded", "user");

  const form = new FormData();
  form.append("file", file);

  showResults(await (await fetch(`${API_BASE}/search-by-image`, {
    method: "POST",
    body: form
  })).json());
}

// VOICE
async function sendVoice() {
  const file = document.getElementById("voiceInput").files[0];
  if (!file) return;

  addMessage("🎙 Voice uploaded", "user");

  const form = new FormData();
  form.append("file", file);

  showResults(await (await fetch(`${API_BASE}/search-by-voice`, {
    method: "POST",
    body: form
  })).json());
}

// HANDWRITING
async function sendHandwriting() {
  const file = document.getElementById("handwritingInput").files[0];
  if (!file) return;

  addMessage("✍ Handwriting uploaded", "user");

  const form = new FormData();
  form.append("file", file);

  showResults(await (await fetch(`${API_BASE}/search-by-handwriting`, {
    method: "POST",
    body: form
  })).json());
}
document.getElementById("textInput").addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    sendText();
  }
});