document.addEventListener("DOMContentLoaded", function () {
    const config = { fps: 10, qrbox: { width: 250, height: 250 } };
    let html5QrcodeScanner = new Html5QrcodeScanner("qr-reader", config, /* verbose= */ false);

    function processTicket(ticketCode, isFromCamera = true) {
        if (isFromCamera) {
            html5QrcodeScanner.pause(true);
        }

        document.getElementById('scan-result').innerHTML =
            `<div class="alert alert-info py-2">Đang kiểm tra vé...</div>`;

        fetch('/admin/api/check-ticket', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticket_code: ticketCode })
        })
        .then(response => response.json())
        .then(data => {
            if (data.valid) {
                document.getElementById('scan-result').innerHTML =
                    `<div class="alert alert-success py-2">Vé hợp lệ! Khách: <strong>${data.customer_name}</strong></div>`;
            } else {
                const ten = data.customer_name ? ` (Khách: ${data.customer_name})` : "";
                document.getElementById('scan-result').innerHTML =
                    `<div class="alert alert-danger py-2">${data.message || "Vé không hợp lệ!"}${ten}</div>`;
            }

            if (isFromCamera) {
                setTimeout(() => html5QrcodeScanner.resume(), 2500);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('scan-result').innerHTML =
                `<div class="alert alert-warning py-2">⚠️ Lỗi kết nối máy chủ!</div>`;
            if (isFromCamera) {
                setTimeout(() => html5QrcodeScanner.resume(), 2500);
            }
        });
    }

    const qrCodeSuccessCallback = (decodedText) => {
        processTicket(decodedText, true);
    };

    html5QrcodeScanner.render(qrCodeSuccessCallback);

    const manualForm = document.getElementById('manual-checkin-form');
    if (manualForm) {
        manualForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const inputEl = document.getElementById('manual-ticket-code');
            const code = inputEl.value.trim();
            if (code) {
                processTicket(code, false);
                inputEl.value = '';
            }
        });
    }
});
