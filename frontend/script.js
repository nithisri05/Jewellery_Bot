const API_BASE = "http://127.0.0.1:8000";

function addMessage(text, sender="bot") {
  const chatBox = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.innerText = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ---------------- TEXT ----------------
async function sendText() {
  const input = document.getElementById("textInput");
  const text = input.value;
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  });

  const data = await res.json();
  showResults(data);
}

// ---------------- IMAGE ----------------
async function sendImage() {
  const file = document.getElementById("imageInput").files[0];
  const form = new FormData();
  form.append("file", file);

  addMessage("📷 Image uploaded", "user");

  const res = await fetch(`${API_BASE}/search-by-image`, {
    method: "POST",
    body: form
  });

  const data = await res.json();
  showResults(data);
}

// ---------------- VOICE ----------------
async function sendVoice() {
  const file = document.getElementById("voiceInput").files[0];
  const form = new FormData();
  form.append("file", file);

  addMessage("🎙 Voice uploaded", "user");

  const res = await fetch(`${API_BASE}/search-by-voice`, {
    method: "POST",
    body: form
  });

  const data = await res.json();
  showResults(data);
}

// ---------------- HANDWRITING ----------------
async function sendHandwriting() {
  const file = document.getElementById("handwritingInput").files[0];
  const form = new FormData();
  form.append("file", file);

  addMessage("✍ Handwriting uploaded", "user");

  const res = await fetch(`${API_BASE}/search-by-handwriting`, {
    method: "POST",
    body: form
  });

  const data = await res.json();
  showResults(data);
}

// ---------------- RESULTS ----------------
function showResults(data) {
  if (data.query) {
    addMessage(`Query understood as: "${data.query}"`, "bot");
  }

  data.results.forEach(item => {
    addMessage(`💎 ${item.category}\n🖼 ${item.image_path}`, "bot");
  });
}
