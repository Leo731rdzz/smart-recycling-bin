document.addEventListener("DOMContentLoaded", () => {
    const socket = io();
    const slider = document.getElementById("threshold");
    const thValue = document.getElementById("th-value");
    const logBox = document.getElementById("detection-log");

    slider.addEventListener("input", (event) => {
        const value = parseFloat(event.target.value);
        thValue.innerText = value.toFixed(2);
        socket.emit("override_th", value);
    });

    socket.on("detection", (data) => {
        const className = data.content;
        const confidence = (data.confidence * 100).toFixed(1) + "%";
        
        logBox.innerHTML = `
            <div>Detectado: <span class="obj-name">${className}</span></div>
            <div style="font-size: 0.7em; color: #aaa; margin-top: 5px;">Confianza: ${confidence}</div>
        `;
    });

    socket.on("connect", () => {
        logBox.innerHTML = "Conectado. Esperando imagen...";
    });

    socket.on("disconnect", () => {
        logBox.innerHTML = "Desconectado...";
    });
});
