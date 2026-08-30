document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("img.uni-logo").forEach(function (img) {
    img.addEventListener("error", function () {
      var fallback = img.getAttribute("data-fallback");
      if (fallback && img.src.indexOf(fallback) === -1) {
        img.src = fallback;
      }
    }, { once: true });
  });
});
