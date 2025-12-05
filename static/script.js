document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const chatBox = document.getElementById("chat-box");

    async function sendMessage() {
        const userText = input.value.trim();
        if (userText === "") return;

        // Tampilkan pesan user
        addMessage(userText, "user-message");
        input.value = "";

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userText }),
            });

            const data = await response.json();

            // baca field sesuai format API FastAPI
            const botReply =
                data.reply ||
                data.response ||
                data.message ||
                "⚠ Bot tidak mengirim respons.";

            addMessage(botReply, "bot-message");

        } catch (error) {
            addMessage("⚠ Terjadi kesalahan koneksi ke server.", "bot-message");
        }
    }

    function addMessage(text, className) {
        const msg = document.createElement("div");
        msg.className = className;
        msg.innerText = text;
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Klik tombol
    sendBtn.addEventListener("click", sendMessage);

    // Tekan Enter
    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
});
