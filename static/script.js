document.addEventListener('DOMContentLoaded', function() {
    // Escuchar el evento submit del formulario
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            // Mostrar el spinner al enviar el formulario
            const spinner = document.getElementById('loading-spinner');
            if (spinner) {
                spinner.style.display = 'block';
            }
        });
    }
});
