document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("aysa-form");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var universidad = form.universidad.value;
    var nivel = form.nivel.value;
    var capitulo = form.capitulo.value;
    var fecha = form.fecha.value || "no indicada";
    var text = [
      "Hola AYSA, quiero información.",
      "Universidad: " + universidad,
      "Pregrado / Maestría: " + nivel,
      "Etapa (plan, observaciones, sustentación…): " + capitulo,
      "Fecha límite: " + fecha
    ].join("\n");
    window.location.href = "https://wa.me/51963554495?text=" + encodeURIComponent(text);
  });
});
