/* SUBSCRIBE_URL: paste the form URL from your free email service (MailerLite, Kit…) here.
   Until then the Subscribe button opens the Gumroad page. */
const SUBSCRIBE_URL = "";
const FALLBACK_URL = "https://ranumbreanna.gumroad.com";

document.querySelectorAll(".subForm").forEach(f => {
  f.addEventListener("submit", ev => {
    ev.preventDefault();
    const email = f.querySelector("input[type=email]").value.trim();
    if (!SUBSCRIBE_URL) { window.open(FALLBACK_URL, "_blank", "noopener"); return; }
    const fd = new FormData(); fd.append("email", email); fd.append("fields[email]", email);
    fetch(SUBSCRIBE_URL, { method: "POST", body: fd, mode: "no-cors" }).finally(() => {
      const ok = f.parentElement.querySelector(".ok"); if (ok) ok.style.display = "block"; f.reset();
    });
  });
});

document.querySelectorAll('a[href="#subscribe"]').forEach(a => a.addEventListener("click", ev => {
  const s = document.getElementById("subscribe"); if (!s) return;
  ev.preventDefault(); s.scrollIntoView({ behavior: "smooth" });
  const i = s.querySelector("input"); if (i) i.focus({ preventScroll: true });
}));

const results = document.getElementById("results");
if (results) {
  const q = (new URLSearchParams(location.search).get("q") || "").trim();
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  document.getElementById("sh").textContent = q ? `Search: "${q}"` : "Search";
  const box = document.querySelector('.search input[name="q"]'); if (box) box.value = q;
  fetch("/posts.json").then(r => r.json()).then(posts => {
    const hits = q ? posts.filter(p => (p.title + " " + p.dek + " " + p.cat + " " + p.text).toLowerCase().includes(q.toLowerCase())) : [];
    document.getElementById("sc").textContent = q ? `${hits.length} result${hits.length === 1 ? "" : "s"}` : "Type a word in the search box above.";
    results.innerHTML = hits.length ? hits.map(p => `<div class="item"><a class="thumb" href="/${p.slug}/" aria-hidden="true" tabindex="-1">${esc(p.cat)}</a>
      <div><span class="label" style="margin-top:0">${esc(p.cat)}</span><h2><a href="/${p.slug}/">${esc(p.title)}</a></h2>
      <p>${esc(p.dek)}</p><small>${p.date} · ${p.read} min read</small></div></div>`).join("")
      : (q ? '<div class="empty">No posts match that yet. Try another word.</div>' : "");
  });
}
