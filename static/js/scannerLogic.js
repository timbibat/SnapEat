/**
 * Handles camera access, image capture, and image data preparation for food analysis.
 * Uploads images directly to backend where Google Cloud Vision is used.
 */

window.DomUtils.ready(() => {

    const video = DomUtils.byId('cameraPreview');
    const captureBtn = DomUtils.byId('captureBtn');
    const switchCameraBtn = DomUtils.byId('switchCameraBtn');
    const imageUploadInput = DomUtils.byId('imageUploadInput');
    const loadingOverlay = DomUtils.byId('loadingOverlay');

    // Create canvas if not provided by HTML
    let canvas = DomUtils.byId('captureCanvas');
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

        // 1. Security/Context Check
        if (!navigator.mediaDevices && !navigator.webkitGetUserMedia && !navigator.mozGetUserMedia) {
            alert("Error: Your browser or app does not support camera access. (Requires HTTPS)");
            return;
        }

        // Stop existing stream
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
        }

        // 2. Try High-Res Environment Camera (Ideal for food scanning)
        const constraints = {
            video: {
                facingMode: usingFrontCamera ? 'user' : { ideal: 'environment' },
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        };

        try {
            currentStream = await navigator.mediaDevices.getUserMedia(constraints);
            video.srcObject = currentStream;
            video.play().catch(e => console.error("Video play failed:", e));
        } catch (error) {
            console.warn("Primary camera failed, trying aggressive fallback...", error);

            // 3. FALLBACK: Try a completely empty constraint (Most compatible)
            try {
                const getUserMedia = (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) ||
                    navigator.webkitGetUserMedia ||
                    navigator.mozGetUserMedia;

                if (typeof getUserMedia === 'function') {
                    if (navigator.mediaDevices) {
                        currentStream = await navigator.mediaDevices.getUserMedia({ video: true });
                    } else {
                        currentStream = await new Promise((resolve, reject) => {
                            getUserMedia.call(navigator, { video: true }, resolve, reject);
                        });
                    }
                    video.srcObject = currentStream;
                    video.play();
                } else {
                    throw new Error("No getUserMedia API found");
                }
            } catch (fallbackError) {
                console.error("Final camera error:", fallbackError);

                let msg = `Could not access camera (${fallbackError.name}).\n\n`;
                if (fallbackError.name === 'NotAllowedError' || fallbackError.name === 'PermissionDeniedError') {
                    msg += "PERMISSION DENIED: Please go to your Phone Settings > Apps > SnapEat and enable Camera permissions.";
                } else if (fallbackError.name === 'NotFoundError' || fallbackError.name === 'DevicesNotFoundError') {
                    msg += "HARDWARE ERROR: No camera found or it's being used by another app.";
                } else {
                    msg += "Ensure you are using HTTPS and have granted permissions in your app settings.";
                }
                alert(msg);
            }
        }
    }

    // --- UI Controls ---
    function showLoading(show) {
        DomUtils.setHidden(loadingOverlay, !show);
        if (captureBtn) {
            captureBtn.disabled = show;
            captureBtn.style.opacity = show ? "0.5" : "1";
        }
    }

    // --- Image Capture ---
    async function captureImage() {
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

    // --- Upload and Recognition Ingestion ---
    async function uploadFoodImage(imageBlob) {
        try {
            // Show loading animation overlay
            showLoading(true);

            const formData = new FormData();
            formData.append('food_image', imageBlob, 'capture.jpg');

            // Send image directly to Flask backend which runs Google Cloud Vision
            const response = await fetch('/api/food/identify', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || "Failed to identify food.");
            }

            // Clean up camera stream resources
            if (currentStream) {
                currentStream.getTracks().forEach(track => track.stop());
            }

            // Redirect user to the nutritional analysis results screen
            if (data.food_id) {
                window.location.href = `/analysis/${data.food_id}`;
            }
        } catch (error) {
            console.error("Scanning Error:", error);
            alert("Recognition Error: " + error.message);
            showLoading(false);
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
                uploadFoodImage(file);
            }
        });
    }
});
