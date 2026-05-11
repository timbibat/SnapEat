/**
 * Handles camera access, image capture, and image data preparation for food analysis.
 */

document.addEventListener('DOMContentLoaded', () => {

    const video = document.getElementById('cameraPreview');
    const captureBtn = document.getElementById('captureBtn');
    const switchCameraBtn = document.getElementById('switchCameraBtn');
    const imageUploadInput = document.getElementById('imageUploadInput');

    // Create canvas if not provided by HTML
    let canvas = document.getElementById('captureCanvas');
    if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'captureCanvas';
        canvas.style.display = 'none';
        document.body.appendChild(canvas);
    }

    let currentStream = null;
    let usingFrontCamera = false;

    // --- Camera Initialization ---
    async function startCamera() {
        if (!video) return;

        // Stop existing stream
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
        }

        const constraints = {
            video: {
                facingMode: usingFrontCamera ? 'user' : 'environment'
            }
        };

        try {
            currentStream = await navigator.mediaDevices.getUserMedia(constraints);
            video.srcObject = currentStream;
            video.onloadedmetadata = () => {
                video.play().catch(e => console.error("Video play failed:", e));
            };
        } catch (error) {
            console.error("Camera access error:", error);
            alert(`Could not access camera.\nError: ${error.name}\n\nTip: Ensure you have granted permission and are not using the camera in another app.`);
        }
    }

    // --- Image Capture ---
    function captureImage() {
        if (!video || !currentStream) {
            alert("Camera is not ready.");
            return;
        }

        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;
        
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
            if (blob) {
                uploadFoodImage(blob);
            }
        }, 'image/jpeg', 0.85);
    }

    // --- Upload Logic ---
    async function uploadFoodImage(imageBlob, name = null) {
        const formData = new FormData();
        formData.append('food_image', imageBlob, 'capture.jpg');
        
        if (name) {
            formData.append('food_name', name);
        }
        // NOTE: We don't send a default 'apple' anymore, so the AI can identify it!

        try {
            // Show some feedback
            if (captureBtn) {
                captureBtn.disabled = true;
                captureBtn.style.opacity = "0.5";
            }

            const response = await fetch('/api/food/identify', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || "Failed to identify food.");
            }

            // Stop camera
            if (currentStream) {
                currentStream.getTracks().forEach(track => track.stop());
            }

            if (data.food_id) {
                window.location.href = `/analysis/${data.food_id}`;
            }

        } catch (error) {
            console.error("Upload error:", error);
            alert("Error: " + error.message);
            if (captureBtn) {
                captureBtn.disabled = false;
                captureBtn.style.opacity = "1";
            }
        }
    }

    // --- Event Listeners ---
    if (video) {
        startCamera();
    }

    if (captureBtn) {
        captureBtn.addEventListener('click', captureImage);
    }

    if (switchCameraBtn) {
        switchCameraBtn.addEventListener('click', () => {
            usingFrontCamera = !usingFrontCamera;
            startCamera();
        });
    }

    if (imageUploadInput) {
        imageUploadInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                // If it's a generic capture name, don't send it so AI can identify
                const lowerName = file.name.toLowerCase();
                if (lowerName.includes('image') || lowerName.includes('capture') || lowerName.includes('img')) {
                    uploadFoodImage(file);
                } else {
                    const cleanName = file.name.split('.')[0];
                    uploadFoodImage(file, cleanName);
                }
            }
        });
    }
});
