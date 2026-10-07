(function () {
  "use strict";

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function showTab(id) {
    $all(".tab").forEach(function (t) { t.classList.toggle("active", t.dataset.tab === id); });
    $all(".panel").forEach(function (p) { p.classList.toggle("active", p.id === id); });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function initTabs() {
    $all(".tab").forEach(function (t) {
      t.addEventListener("click", function () { showTab(t.dataset.tab); });
    });
    $all("[data-goto]").forEach(function (b) {
      b.addEventListener("click", function () { showTab(b.dataset.goto); });
    });
  }

  function initIdToggle() {
    var cb = $("#toggle-ids");
    if (!cb) return;
    cb.addEventListener("change", function () { document.body.classList.toggle("hide-ids", !cb.checked); });
  }

  function initRentGrid() {
    $all(".rent-grid").forEach(function (grid) {
      function recalc() {
        var total = 0, years = 0;
        $all("tbody tr", grid).forEach(function (tr) {
          var v = parseFloat($("input.rent", tr).value || "0");
          var annual = v * 12;
          $(".annual", tr).textContent = annual ? annual.toLocaleString("en-IN") : "";
          if (v) { total += annual; years += 1; }
        });
        var out = $(".aar", grid);
        if (out) out.value = years ? Math.round(total / years).toLocaleString("en-IN") : "";
      }
      grid.addEventListener("input", recalc);
      var add = $(".add-year", grid);
      if (add) add.addEventListener("click", function () {
        var body = $("tbody", grid);
        var n = body.children.length + 1;
        var tr = document.createElement("tr");
        tr.innerHTML = "<td>Year " + n + "</td><td><div class='money'><input type='number' class='rent'></div></td><td class='annual'></td>";
        body.appendChild(tr);
      });
    });
  }

  function initWizard() {
    var node = $("#wizard-data");
    var host = $("#wizard");
    if (!node || !host) return;
    var data = JSON.parse(node.textContent);
    var resultHost = $("#wizard-result");

    function renderResult(keys, text) {
      resultHost.innerHTML = "";
      if (!keys.length) {
        resultHost.innerHTML = "<div class='note amber'>" + escapeHtml(text) + "</div>";
        return;
      }
      keys.forEach(function (k) {
        var r = data.rules[k];
        if (!r) return;
        var div = document.createElement("div");
        div.className = "result";
        var rows = [
          ["Instrument", r.instrument],
          ["Duty basis", r.basis],
          ["Proper stamp duty", r.duty],
          ["Minimum", r.min],
          ["Maximum", r.max],
          ["Provisos / adjustments", r.proviso],
          ["Exemptions", r.exempt],
          ["Sec 45-A MV check", r.s45a],
          ["Calculation inputs", r.calc],
        ].filter(function (x) { return x[1]; });
        div.innerHTML =
          "<div class='art'>Article " + escapeHtml(k) + "</div>" +
          (text && keys.length === 1 && text.replace(/^=>\s*/, "") !== k ? "<div class='note amber'>" + escapeHtml(text) + "</div>" : "") +
          "<dl>" + rows.map(function (x) { return "<dt>" + x[0] + "</dt><dd>" + escapeHtml(x[1]) + "</dd>"; }).join("") + "</dl>";
        resultHost.appendChild(div);
      });
    }

    function renderStep(stepId, depth) {
      $all(".wstep", host).forEach(function (el) {
        if (parseInt(el.dataset.depth, 10) >= depth) el.remove();
      });
      resultHost.innerHTML = "";
      var step = data.steps[stepId];
      if (!step) return;
      var div = document.createElement("div");
      div.className = "wstep";
      div.dataset.depth = depth;
      var ids = step.input && step.input !== "-" ? " <span class='fid'>" + escapeHtml(step.input) + "</span>" : "";
      div.innerHTML = "<div class='wq'>Step " + escapeHtml(stepId) + ": " + escapeHtml(step.question) + ids + "</div><div class='wopts'></div>";
      var opts = $(".wopts", div);
      step.options.forEach(function (o) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "wopt";
        b.textContent = o.answer;
        b.addEventListener("click", function () {
          $all(".wopt", opts).forEach(function (x) { x.classList.remove("sel"); });
          b.classList.add("sel");
          if (o.next) {
            renderStep(o.next, depth + 1);
          } else {
            $all(".wstep", host).forEach(function (el) {
              if (parseInt(el.dataset.depth, 10) > depth) el.remove();
            });
            if (o.link) {
              resultHost.innerHTML = "<div class='note'>" + escapeHtml(o.result) + " &rarr; <a href='" + o.link + "'>open screen</a></div>";
            } else {
              renderResult(o.keys, o.result);
            }
          }
        });
        opts.appendChild(b);
      });
      host.appendChild(div);
    }

    renderStep(data.start, 0);
    var reset = $("#wizard-reset");
    if (reset) reset.addEventListener("click", function () { renderStep(data.start, 0); });
  }

  function initSearch() {
    var s = $("#search");
    if (!s) return;
    s.addEventListener("input", function () {
      var q = s.value.toLowerCase();
      $all(".ncard").forEach(function (c) {
        c.style.display = c.textContent.toLowerCase().indexOf(q) >= 0 ? "" : "none";
      });
      $all(".intent-block").forEach(function (b) {
        var any = $all(".ncard", b).some(function (c) { return c.style.display !== "none"; });
        b.style.display = any ? "" : "none";
      });
    });
  }

  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTabs();
    initIdToggle();
    initRentGrid();
    initWizard();
    initSearch();
  });
})();
