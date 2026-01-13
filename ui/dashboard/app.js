const API_BASE = "http://127.0.0.1:8000";

async function loadEvents() {
  const res = await fetch(`${API_BASE}/events`);
  const events = await res.json();

  const table = document.getElementById("event-table");
  table.innerHTML = "";

  events.forEach(e => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${e.id}</td>
      <td>${e.camera_id}</td>
      <td>${e.rule}</td>
      <td>${e.zone}</td>
      <td>${e.confidence}</td>
      <td>${new Date(e.timestamp * 1000).toLocaleString()}</td>
    `;

    table.appendChild(row);
  });
}

loadEvents();
setInterval(loadEvents, 3000);
