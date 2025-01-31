document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('booking-form');
    const message = document.getElementById('message');
    const appointmentSelect = document.getElementById('appointment');

    // Fetch available appointments
    fetch('/api/appointments')
        .then(response => response.json())
        .then(data => {
            data.forEach(app => {
                if (app.status === 'available') {
                    const option = document.createElement('option');
                    option.value = app.id;
                    option.textContent = `${app.date} at ${app.time}`;
                    appointmentSelect.appendChild(option);
                }
            });
        });

    // Handle form submission
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            appointment_id: appointmentSelect.value
        };

        fetch('/api/book', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        })
            .then(response => response.json())
            .then(data => {
                message.textContent = data.message;
                form.reset();
            })
            .catch(error => {
                message.textContent = 'Booking failed. Please try again.';
            });
    });
});