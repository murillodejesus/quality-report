document.addEventListener('DOMContentLoaded', () => {
    const photoFileInput = document.getElementById('photo-file');
    const previewImage = document.getElementById('preview-image');
    const uploadButton = document.getElementById('upload-button');
    const photoNameInput = document.getElementById('photo-name');
    const statusMessage = document.getElementById('status-message');
    
    // Escuta a mudança no campo de arquivo para pré-visualizar a imagem
    photoFileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                previewImage.style.display = 'block';
                uploadButton.disabled = false; // Habilita o botão de upload
                uploadButton.classList.remove('opacity-50', 'cursor-not-allowed');
            };
            reader.readAsDataURL(file);
        }
    });

    // Escuta o clique no botão de upload
    uploadButton.addEventListener('click', async () => {
        // Valida se os campos obrigatórios estão preenchidos
        const photoName = photoNameInput.value.trim();
        const file = photoFileInput.files[0];

        if (!photoName || !file) {
            statusMessage.textContent = 'Por favor, digite um nome e selecione uma foto.';
            statusMessage.classList.add('text-red-600');
            return;
        }

        statusMessage.textContent = 'Enviando...';
        statusMessage.classList.remove('text-red-600');
        statusMessage.classList.add('text-blue-600');
        uploadButton.disabled = true;
        uploadButton.classList.add('opacity-50', 'cursor-not-allowed');

        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = async () => {
            const base64Image = reader.result.split(',')[1]; // Remove o prefixo data:image/jpeg;base64,...

            const payload = {
                name: photoName,
                base64Image: base64Image
            };

            try {
                // Substitua o URL abaixo pelo URL do seu servidor Flask (http://localhost:5000)
                const response = await fetch('http://localhost:5000/upload', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    statusMessage.textContent = `Sucesso! ${result.message}`;
                    statusMessage.classList.remove('text-red-600', 'text-blue-600');
                    statusMessage.classList.add('text-green-600');
                    // Opcional: Limpar campos após o sucesso
                    photoNameInput.value = '';
                    photoFileInput.value = '';
                    previewImage.style.display = 'none';
                } else {
                    statusMessage.textContent = `Erro: ${result.message}`;
                    statusMessage.classList.remove('text-green-600', 'text-blue-600');
                    statusMessage.classList.add('text-red-600');
                }
            } catch (error) {
                statusMessage.textContent = `Erro de conexão: ${error.message}`;
                statusMessage.classList.remove('text-green-600', 'text-blue-600');
                statusMessage.classList.add('text-red-600');
            } finally {
                uploadButton.disabled = false;
                uploadButton.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        };
    });
});