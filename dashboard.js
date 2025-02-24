document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('imageFile');
    const uploadBtn = document.getElementById('uploadBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const previewImage = document.getElementById('previewImage');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');

    // Click "Upload Image" button -> Opens file dialog
    uploadBtn.addEventListener('click', () => {
        imageInput.click();
    });

    // When an image is selected, show the preview and the analyze button
    imageInput.addEventListener('change', () => {
        if (imageInput.files.length > 0) {
            previewImage.src = URL.createObjectURL(imageInput.files[0]);
            previewImage.style.display = 'block';
            analyzeBtn.style.display = 'block';  // Show analyze button
        }
    });

    // When "Analyze Image" is clicked, send the image for inference
    analyzeBtn.addEventListener('click', async () => {
        const file = imageInput.files[0];
        if (!file) {
            alert('Please select an image file');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            loading.style.display = 'block';
            result.style.display = 'none';  // Hide previous result
            analyzeBtn.disabled = true;  // Prevent multiple clicks

            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                result.textContent = `Prediction: ${data.prediction} (Confidence: ${data.confidence})`;
                result.style.color = data.color;
                result.style.display = 'block';  // Show result
            } else {
                alert(data.error || 'Analysis failed');
            }
        } catch (error) {
            alert('Error during analysis');
        } finally {
            loading.style.display = 'none';
            analyzeBtn.disabled = false;
        }
    });
});
