const API_BASE = "/api";

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || res.statusText);
  }
  return res;
}

export async function getProfile() {
  const res = await request("/user/profile");
  return res.json();
}

export async function updateProfile(data) {
  const res = await request("/user/profile", {
    method: "PUT",
    body: JSON.stringify(data),
  });
  return res.json();
}

export function createChatStream(message, user_id = 1) {
  const url = `${API_BASE}/chat/stream`;
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, user_id }),
  });
}

export async function analyzeImage(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/image/analyze`, {
    method: "POST",
    body: formData,
  });
  return res.json();
}
