let sessionId = null;

async function startSession() {
  const res = await fetch("/api/v1/sessions", { method: "POST" });
  const data = await res.json();
  sessionId = data.session_id;
}

async function sendMessage(message) {
  const res = await fetch(`/api/v1/sessions/${sessionId}/message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  return await res.json();
}

document.addEventListener("DOMContentLoaded", async () => {
  await startSession();
  const chatBox = document.getElementById("chat-box");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("user-input");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msg = input.value.trim();
    if (!msg) return;
    chatBox.innerHTML += `<p><b>You:</b> ${msg}</p>`;
    input.value = "";

    const res = await sendMessage(msg);
    chatBox.innerHTML += `<p><b>AI:</b> ${res.reply}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;
  });
});
