const API_BASE = "http://127.0.0.1:8000";

let pendingImageFile = null;

// ---------------- GREETING ----------------
window.onload = () => {
  addMessage(
    "👋 Hi! I’m your jewellery assistant.\n\n" +
    "You can search using text, image, voice, or handwriting.\n" +
    "Try asking for rings or necklaces 💍📿",
    "bot"
  );
};

// ---------------- HELPERS ----------------
function addMessage(text, sender = "bot") {
  const chatBox = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.innerText = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function addImagePreview(file) {
  const img = document.createElement("img");
  img.src = URL.createObjectURL(file);
  img.className = "image-preview";
  document.getElementById("chat-box").appendChild(img);
}

// ---------------- TEXT ----------------
async function sendText() {
  const input = document.getElementById("textInput");
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  // 🔥 If image is pending, wait logic applies
  if (pendingImageFile) {
    await sendImageWithQuery(text);
    pendingImageFile = null;
    return;
  }

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  });

  const data = await res.json();
  showResults(data);
}

// ---------------- IMAGE (WAIT MODE) ----------------
function sendImage() {
  const input = document.getElementById("imageInput");
  const file = input.files[0];
  if (!file) return;

  pendingImageFile = file;
  addImagePreview(file);

  addMessage(
    "📷 Image uploaded.\nWhat would you like to find from this image?",
    "bot"
  );

  input.value = "";
}

async function sendImageWithQuery(query) {
  const form = new FormData();
  form.append("file", pendingImageFile);
  form.append("query", query);

  const res = await fetch(`${API_BASE}/search-by-image`, {
    method: "POST",
    body: form
  });

  const data = await res.json();
  showResults(data);
}

// ---------------- VOICE ----------------
async function sendVoice() {
  const input = document.getElementById("voiceInput");
  const file = input.files[0];
  if (!file) return;

  addMessage("🎙 Voice uploaded", "user");

  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_BASE}/search-by-voice`, {
    method: "POST",
    body: form
  });

  const data = await res.json();
  showResults(data);
  input.value = "";
}

// ---------------- HANDWRITING ----------------
async function sendHandwriting() {
  const input = document.getElementById("handwritingInput");
  const file = input.files[0];
  if (!file) return;

  addImagePreview(file);
  addMessage("✍ Handwriting uploaded", "user");

  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_BASE}/search-by-handwriting`, {
    method: "POST",
    body: form
  });

  const data = await res.json();
  showResults(data);
  input.value = "";
}

// ---------------- RESULTS ----------------
function showResults(data) {
  const chatBox = document.getElementById("chat-box");

  if (!data.supported) {
    let msg = "😕 I don’t have that.\nTry:\n";
    (data.suggested_categories || []).forEach(c => msg += `• ${c}\n`);
    addMessage(msg, "bot");
    return;
  }

  if (data.explanation) {
    addMessage(`🧠 ${data.explanation}`, "bot");
  }

  (data.results || []).forEach(item => {
    const card = document.createElement("div");
    card.className = "jewel-card";
    card.innerHTML = `
      <img src="${API_BASE}/images/${item.image_path}">
      <p>💎 ${item.category}</p>
    `;
    chatBox.appendChild(card);
  });

  chatBox.scrollTop = chatBox.scrollHeight;
}
