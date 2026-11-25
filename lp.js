(function () {
  var offer = document.body.dataset.offer;

  // ---- Attribution: keep UTM / click IDs from the ad URL for 30 days, sent with the lead ----
  var KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "fbclid", "gclid"];
  var qs = new URLSearchParams(location.search), attr = {};
  try { attr = JSON.parse(localStorage.getItem("ba_attr") || "{}"); } catch (e) {}
  var fresh = KEYS.some(function (k) { return qs.get(k); });
  if (fresh) { attr = { landing: location.pathname, at: new Date().toISOString() }; KEYS.forEach(function (k) { if (qs.get(k)) attr[k] = qs.get(k); }); }
  if (!attr.landing) attr.landing = location.pathname;
  try { localStorage.setItem("ba_attr", JSON.stringify(attr)); } catch (e) {}

  // ---- Meta Pixel (only when an ID is set in the page head) ----
  function fbq() { if (window.fbq) window.fbq.apply(null, arguments); }
  if (window.BA_PIXEL_ID) {
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    window.fbq("init", window.BA_PIXEL_ID);
    window.fbq("track", "PageView");
  }
  document.querySelectorAll("[data-track=call]").forEach(function (a) {
    a.addEventListener("click", function () { fbq("track", "Contact", { content_name: offer }); });
  });

  // ---- Multi-step form ----
  var form = document.getElementById("lead");
  var steps = [].slice.call(form.querySelectorAll(".step"));
  var bar = form.querySelector(".progress span"), count = document.getElementById("step-count");
  var err = form.querySelector(".err"), cur = 0, started = false;

  function show(i) {
    steps.forEach(function (s, j) { s.hidden = j !== i; });
    cur = i; bar.style.width = ((i + 1) / steps.length * 100) + "%";
    count.textContent = "Step " + (i + 1) + " of " + steps.length;
    err.hidden = true;
    var first = steps[i].querySelector("input:not([type=radio])") ;
    if (first && i > 0) first.focus({ preventScroll: true });
  }
  function valid(step) {
    var ok = true, missing = [];
    step.querySelectorAll("input[required]:not([type=radio])").forEach(function (i) {
      var bad = !i.value.trim() || (i.type === "email" && !/^\S+@\S+\.\S+$/.test(i.value)) || (i.type === "tel" && i.value.replace(/\D/g, "").length < 10);
      i.classList.toggle("invalid", bad); if (bad) { ok = false; missing.push(i.closest("label").firstChild.textContent.trim().toLowerCase()); }
    });
    var groups = {};
    step.querySelectorAll("input[type=radio]").forEach(function (r) { groups[r.name] = groups[r.name] || r.checked; });
    Object.keys(groups).forEach(function (g) { if (!groups[g]) { ok = false; missing.push("an option"); } });
    if (!ok) { err.textContent = "Please add " + missing.filter(function (v, i, a) { return a.indexOf(v) === i; }).join(", ") + "."; err.hidden = false; }
    return ok;
  }
  form.addEventListener("input", function (e) {
    e.target.classList.remove("invalid");
    if (!started) { started = true; fbq("trackCustom", "LeadFormStart", { offer: offer }); }
  });
  form.querySelectorAll(".next").forEach(function (b) {
    b.addEventListener("click", function () { if (valid(steps[cur])) { show(cur + 1); fbq("trackCustom", "LeadFormStep", { offer: offer, step: cur + 1 }); } });
  });
  form.querySelectorAll(".back").forEach(function (b) { b.addEventListener("click", function () { show(cur - 1); }); });
  // Enter key in a text field advances instead of submitting early
  form.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && e.target.tagName === "INPUT" && cur < steps.length - 1) { e.preventDefault(); var n = steps[cur].querySelector(".next"); if (n) n.click(); }
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!valid(steps[cur])) return;
    var d = Object.fromEntries(new FormData(form));
    var btn = form.querySelector("[type=submit]"), label = btn.textContent;
    btn.disabled = true; btn.textContent = "Sending…";
    var body = {
      Offer: offer === "landlords" ? "Guaranteed rent (landlord)" : "Airbnb management (owner)",
      Name: d.name, Phone: d.phone, Email: d.email, Address: d.address,
      Bedrooms: d.bedrooms, Detail1: d.q1b, Detail2: d.q2,
      Source: [attr.utm_source, attr.utm_campaign, attr.utm_content].filter(Boolean).join(" / ") || "direct",
      "Landing page": attr.landing, "Click ID": attr.fbclid || attr.gclid || "",
      _subject: "New lead (" + offer + "): " + d.name + " · " + d.address,
      _replyto: d.email, _template: "table", _captcha: "false"
    };
    fetch("https://formsubmit.co/ajax/" + window.BA_LEAD_EMAIL, {
      method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(body)
    }).then(function (r) { return r.json().then(function (j) { if (!r.ok || String(j.success) === "false") throw j; }); })
      .then(function () {
        steps.forEach(function (s) { s.hidden = true; });
        form.querySelector(".progress").hidden = true; count.hidden = true;
        form.querySelector(".done").hidden = false;
        fbq("track", "Lead", { content_name: offer });
        document.getElementById("form-card").scrollIntoView({ block: "start" });
      })
      .catch(function () {
        err.innerHTML = 'That didn’t go through. Please call <a href="tel:+16365795617">(636) 579-5617</a> and we’ll take it by phone.';
        err.hidden = false; btn.disabled = false; btn.textContent = label;
      });
  });

  // ---- Sticky mobile CTA: hide while the form is on screen ----
  var sticky = document.querySelector(".sticky"), card = document.getElementById("form-card");
  if (sticky && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { sticky.classList.toggle("hide", es[0].isIntersecting); }, { threshold: 0.15 }).observe(card);
  }
})();
