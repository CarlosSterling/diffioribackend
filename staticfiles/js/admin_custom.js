/**
 * Diffiori Admin — Notificación de nuevos pedidos pagados
 */
(function () {
  const POLL_INTERVAL = 30000; // cada 30s
  const STORAGE_KEY   = "diffiori_last_paid_id";

  // ── Sonido de notificación (Web Audio API) ──────────────────
  function playNotification() {
    try {
      const ctx  = new (window.AudioContext || window.webkitAudioContext)();
      const notes = [523.25, 659.25, 783.99]; // Do-Mi-Sol
      notes.forEach(function (freq, i) {
        const osc  = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type      = "sine";
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(0, ctx.currentTime + i * 0.18);
        gain.gain.linearRampToValueAtTime(0.3, ctx.currentTime + i * 0.18 + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + i * 0.18 + 0.35);
        osc.start(ctx.currentTime + i * 0.18);
        osc.stop(ctx.currentTime  + i * 0.18 + 0.4);
      });
    } catch (e) { /* sin soporte de audio */ }
  }

  // ── Banner de nueva orden ───────────────────────────────────
  function showBanner(order) {
    const existing = document.getElementById("diffiori-order-banner");
    if (existing) existing.remove();

    const fmt = new Intl.NumberFormat("es-CO", { style: "currency", currency: "COP", minimumFractionDigits: 0 });
    const total = fmt.format(parseFloat(order.total_amount));

    const banner = document.createElement("div");
    banner.id = "diffiori-order-banner";
    banner.style.cssText = [
      "position:fixed", "top:20px", "right:20px", "z-index:99999",
      "background:#28a745", "color:#fff", "padding:16px 22px",
      "border-radius:12px", "box-shadow:0 4px 20px rgba(0,0,0,.35)",
      "font-family:sans-serif", "font-size:14px", "max-width:320px",
      "display:flex", "flex-direction:column", "gap:4px",
      "animation:slideIn .4s ease"
    ].join(";");

    banner.innerHTML =
      "<strong style='font-size:16px'>☕ Nuevo pedido pagado</strong>" +
      "<span>Pedido #" + order.id + " — " + order.contact_name + "</span>" +
      "<span style='font-size:13px;opacity:.85'>" + total + "</span>" +
      "<a href='/admin/orders/order/" + order.id + "/change/' " +
         "style='margin-top:8px;background:#fff;color:#28a745;padding:5px 12px;" +
         "border-radius:6px;text-decoration:none;font-weight:bold;text-align:center'>" +
         "Ver pedido &rarr;</a>" +
      "<button onclick=\"this.parentElement.remove()\" " +
              "style='position:absolute;top:8px;right:10px;background:none;border:none;" +
              "color:#fff;font-size:18px;cursor:pointer;line-height:1'>&times;</button>";

    const style = document.createElement("style");
    style.textContent = "@keyframes slideIn{from{transform:translateX(120%);opacity:0}to{transform:translateX(0);opacity:1}}";
    document.head.appendChild(style);

    document.body.appendChild(banner);
    setTimeout(function () { if (banner.parentElement) banner.remove(); }, 15000);
  }

  // ── Polling ─────────────────────────────────────────────────
  function getLastId() {
    return parseInt(localStorage.getItem(STORAGE_KEY) || "0", 10);
  }

  function poll() {
    var since = getLastId();
    fetch("/api/orders/new-paid/?since_id=" + since, { credentials: "include" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data || !data.orders || !data.orders.length) return;
        // Ordenar por id ascendente para mostrar el más reciente al final
        data.orders.sort(function (a, b) { return a.id - b.id; });
        var maxId = data.orders[data.orders.length - 1].id;
        localStorage.setItem(STORAGE_KEY, maxId);
        // Notificar solo si ya teníamos un since_id (no en la primera carga)
        if (since > 0) {
          playNotification();
          data.orders.forEach(showBanner);
        } else {
          // Primera carga: solo guardar el ID máximo sin notificar
          localStorage.setItem(STORAGE_KEY, maxId);
        }
      })
      .catch(function () { /* fallo silencioso */ });
  }

  // Solo activar en páginas del admin
  if (window.location.pathname.startsWith("/admin")) {
    // Si no hay last_id, inicializar sin notificar
    if (!localStorage.getItem(STORAGE_KEY)) {
      poll(); // establece baseline
      setTimeout(function () { setInterval(poll, POLL_INTERVAL); }, POLL_INTERVAL);
    } else {
      poll();
      setInterval(poll, POLL_INTERVAL);
    }
  }
})();
