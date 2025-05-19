// control de tema/otro
const temaSelect    = document.getElementById("tema");
const temaOtroInput = document.getElementById("tema_otro");
temaSelect.addEventListener("change", () => {
  temaOtroInput.style.display = temaSelect.value === "otro"
    ? "inline"
    : "none";
});

// límite de fotos + añadir nuevos <input type="file">
const agregarFotoBtn = document.getElementById("agregarFoto");
const fotosContainer = document.getElementById("fotosContainer");
agregarFotoBtn.addEventListener("click", () => {
  const total = fotosContainer.querySelectorAll('input[type="file"]').length;
  if (total >= 5) {
    alert("Solo puedes subir hasta 5 fotos.");
    return;
  }
  const nuevo = document.createElement("input");
  nuevo.type   = "file";
  nuevo.name   = "fotos";
  nuevo.accept = "image/*";
  fotosContainer.appendChild(nuevo);
});

// dinámico: inputs para cada forma de contacto
const contactoSelect = document.getElementById("contactar_medio");
const idsContainer   = document.getElementById("ids-contacto");
contactoSelect.addEventListener("change", () => {
  // clear old
  idsContainer.innerHTML = "";
  const selected = Array.from(contactoSelect.selectedOptions);
  if (selected.length > 5) {
    alert("Máximo 5 métodos de contacto.");
    // deselect extras
    selected.slice(5).forEach(opt => opt.selected = false);
  }
  // por cada media seleccionado
  Array.from(contactoSelect.selectedOptions).forEach(opt => {
    const name = opt.value;
    const label = document.createElement("label");
    label.setAttribute("for", "contactar_id_" + name);
    label.textContent = `ID/URL para ${opt.text}`;
    const input = document.createElement("input");
    input.type      = "text";
    input.id        = "contactar_id_" + name;
    input.name      = "contactar_id";
    input.minLength = 4;
    input.maxLength = 50;
    idsContainer.appendChild(label);
    idsContainer.appendChild(input);
  });
});

// validación y confirmación previa al submit
const form       = document.getElementById("actividadForm");
const btnAgregar = document.getElementById("agregarActividad");
const divConfirm = document.getElementById("confirmacion");

btnAgregar.addEventListener("click", () => {
  // campos obligatorios
  if (!form.nombre.value.trim() ||
      !form.email.value.trim()  ||
      !form.inicio.value) {
    alert("Por favor completa nombre, email y fecha de inicio.");
    return;
  }
  // fechas
  if (form.termino.value) {
    if (new Date(form.termino.value) <= new Date(form.inicio.value)) {
      alert("La fecha de término debe ser mayor a la fecha de inicio.");
      return;
    }
  }
  // al menos 1 foto
  const archivos = Array.from(
    fotosContainer.querySelectorAll('input[type="file"]')
  ).filter(i => i.files.length > 0);
  if (archivos.length < 1) {
    alert("Debes seleccionar al menos una foto.");
    return;
  }

  // inputs de contacto: si eligió x medio, su input no puede quedar vacío
  const contactosSel = Array.from(
    idsContainer.querySelectorAll('input[name="contactar_id"]')
  );
  for (let inp of contactosSel) {
    if (!inp.value.trim()) {
      alert("Completa todos los identificadores de contacto.");
      return;
    }
  }

  // todos los checks pasan → muestro confirm y escondo form
  divConfirm.style.display = "block";
  form.style.display      = "none";
});

// al confirmar, envío realmente el formulario al servidor
document.getElementById("confirmar")
  .addEventListener("click", () => {
    divConfirm.style.display = "none";
    form.submit();
  });

// cancelar vuelve al formulario
document.getElementById("cancelar")
  .addEventListener("click", () => {
    divConfirm.style.display = "none";
    form.style.display      = "block";
});

// inicializar fechas (ahora y +3h)
const inputInicio  = document.getElementById("inicio");
const inputTermino = document.getElementById("termino");
const now          = new Date();
const later        = new Date(now.getTime() + 3*60*60*1000);
inputInicio.value  = now.toISOString().slice(0,16);
inputTermino.value = later.toISOString().slice(0,16);
