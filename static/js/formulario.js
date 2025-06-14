// control en temas /otros
const temaSelect    = document.getElementById("tema");
const temaOtroInput = document.getElementById("tema_otro");
temaSelect.addEventListener("change", () => {
  temaOtroInput.style.display = temaSelect.value === "otro"
    ? "inline"
    : "none";
});

// limite de fotos validacion
const agregarFotoBtn = document.getElementById("agregarFoto");
const fotosContainer = document.getElementById("fotosContainer");
agregarFotoBtn.addEventListener("click", () => {
  const total = fotosContainer.querySelectorAll('input[type="file"]').length;
  if (total >= 5) {
    mostrarErrores(["Solo puedes subir hasta 5 fotos."]);
    return;
  }
  const nuevo = document.createElement("input");
  nuevo.type   = "file";
  nuevo.name   = "fotos";
  nuevo.accept = "image/*";
  fotosContainer.appendChild(nuevo);
});

// inputs para cada forma de contacto
const contactoSelect = document.getElementById("contactar_medio");
const idsContainer   = document.getElementById("ids-contacto");
contactoSelect.addEventListener("change", () => {
  idsContainer.innerHTML = "";
  const selected = Array.from(contactoSelect.selectedOptions);
  if (selected.length > 5) {
    mostrarErrores(["Máximo 5 métodos de contacto."]);
    selected.slice(5).forEach(opt => opt.selected = false);
  }
  selected.forEach(opt => {
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

// mostrar errores en el bloque devalidacion
function mostrarErrores(lista) {
  const valBox  = document.getElementById("val-box");
  const valList = document.getElementById("val-list");
  valList.innerHTML = ""; // limpiar errores anteriores

  lista.forEach(msg => {
    const li = document.createElement("li");
    li.textContent = msg;
    valList.appendChild(li);
  });

  valBox.style.display = "block";
}

// validacion antes del submit
const form       = document.getElementById("actividadForm");
const btnAgregar = document.getElementById("agregarActividad");
const divConfirm = document.getElementById("confirmacion");

btnAgregar.addEventListener("click", () => {
  const errores = [];

  if (!form.nombre.value.trim() ||
      !form.email.value.trim()  ||
      !form.inicio.value) {
    errores.push("Por favor completa nombre, email y fecha de inicio.");
  }

  if (form.termino.value) {
    if (new Date(form.termino.value) <= new Date(form.inicio.value)) {
      errores.push("La fecha de término debe ser mayor a la fecha de inicio.");
    }
  }

  const archivos = Array.from(
    fotosContainer.querySelectorAll('input[type="file"]')
  ).filter(i => i.files.length > 0);
  if (archivos.length < 1) {
    errores.push("Debes seleccionar al menos una foto.");
  }

  const contactosSel = Array.from(
    idsContainer.querySelectorAll('input[name="contactar_id"]')
  );
  for (let inp of contactosSel) {
    if (!inp.value.trim()) {
      errores.push("Completa todos los identificadores de contacto.");
      break;
    }
  }

  if (errores.length > 0) {
    mostrarErrores(errores);
    return;
  }

  // todos los checks pasan a ocultar errores y mostrar confirmación
  document.getElementById("val-box").style.display = "none";
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

