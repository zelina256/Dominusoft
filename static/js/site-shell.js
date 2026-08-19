(function () {
  "use strict";

  var header = document.querySelector("[data-site-header]");
  var yearNodes = document.querySelectorAll("[data-current-year]");

  yearNodes.forEach(function (node) {
    node.textContent = new Date().getFullYear();
  });

  if (!header || !document.body.classList.contains("home-page")) {
    return;
  }

  var updateHeader = function () {
    header.classList.toggle("is-scrolled", window.scrollY > 32);
  };

  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });
})();
