/**
 * Handles camera access, image capture, and image data preparation for food analysis.
 *
 * NOTE: BOOTSTRAP FRAMEWORK AHHH
 *
 * EXPECTED HTML DOM ELEMENTS (To be implemented by the HTML Developer):
 * - Video Element: ID 'cameraPreview' (where the camera stream will be shown)
 * - Capture Button: ID 'captureBtn' (triggers the photo capture)
 * - Switch Camera Button: ID 'switchCameraBtn' (optional, toggles front/back camera)
 * - File Upload Input: ID 'imageUploadInput' (fallback for uploading existing photos)
 * - Hidden Canvas: ID 'captureCanvas' (used internally to process the video frame, can be hidden)
 */

document.addEventListener('DOMContentLoaded', () => {

    const video = document.getElementById('cameraPreview');
    const captureBtn = document.getElementById('captureBtn');
    const switchCameraBtn = document.getElementById('switchCameraBtn');
    const imageUploadInput = document.getElementById('imageUploadInput');

    // Create canvas dynamically if not provided by HTML
    let canvas = document.getElementById('captureCanvas');
    if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.style.display = 'none';
        document.body.appendChild(canvas);
    }

    let currentStream = null;
    let usingFrontCamera = false;

    // --- Camera Initialization ---
    async function startCamera() {
        if (!video) return; // Not on the scanner page

        // Stop existing stream if any
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
        }

        const constraints = {
            video: {
                facingMode: usingFrontCamera ? 'user' : 'environment',
                width: { ideal: 1920 },
                height: { ideal: 1080 }
            }
        };

        try {
            currentStream = await navigator.mediaDevices.getUserMedia(constraints);
            video.srcObject = currentStream;
            video.play();
        } catch (error) {
            console.error("Camera error:", error);
            if (window.AppMain) {
                AppMain.showToast("Could not access camera. Please allow permissions.", "error");
            } else {
                alert("Could not access camera.");
            }
        }
    }

    // --- Image Capture ---
    function captureImage() {
        if (!video || !currentStream) return;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert to Blob and send to backend
        canvas.toBlob((blob) => {
            if (blob) {
                uploadFoodImage(blob);
            }
        }, 'image/jpeg', 0.8); // 80% quality JPEG
    }

    // --- Upload Logic ---
    async function uploadFoodImage(imageBlob) {
        if (window.AppMain) AppMain.showLoader();

        const formData = new FormData();
        formData.append('food_image', imageBlob, 'capture.jpg');

        try {
            // Note: Using FormData — do NOT set Content-Type manually,
            // the browser sets it automatically with the boundary.
            const response = await fetch('/api/food/identify', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || "Failed to identify food.");
            }

            if (window.AppMain) AppMain.showToast("Food identified successfully!", "success");

            // Stop camera to save battery
            if (currentStream) {
                currentStream.getTracks().forEach(track => track.stop());
            }

            // Redirect to results page with food_id
            if (data.food_id) {
                window.location.href = `/api/food/details/${data.food_id}`;
            }

        } catch (error) {
            console.error("Upload error:", error);
            if (window.AppMain) {
                AppMain.showToast(error.message, "error");
                AppMain.hideLoader();
            } else {
                alert(error.message);
            }
        }
    }

    // --- Event Listeners ---
    if (video) {
        startCamera(); // Auto-start camera if video element is present
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

    // Handle manual file upload (from gallery/disk)
    if (imageUploadInput) {
        imageUploadInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                uploadFoodImage(file);
            }
        });
    }
});
