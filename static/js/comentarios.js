function cargarComentarios() {
    fetch(`/api/comentarios/${ACTIVIDAD_ID}`)
        .then(res => res.json())
        .then(data => {
            const contenedor = document.getElementById("lista-comentarios");
            contenedor.innerHTML = "";
            data.forEach(c => {
                const li = document.createElement("li");
                li.innerHTML = `<strong>${c.nombre}</strong> (${c.fecha}):<br>${c.texto}`;
                contenedor.appendChild(li);
            });
        });
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-comentario");
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(form);
        fetch(`/api/comentarios/${ACTIVIDAD_ID}`, {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.ok) {
                cargarComentarios();
                form.reset();
            } else {
                alert("Error: " + data.error);
            }
        });
    });

    cargarComentarios();  // al iniciar
});
