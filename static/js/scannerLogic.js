/**
 * Handles camera access, image capture, and image data preparation for food analysis.
 * Uses Puter.js (gpt-5.4-nano) for frontend AI identification.
 */

// Puter App ID is now injected from scanFood.html (Backend -> Template -> JS)
// puter.setAppId is called in the script tag within scanFood.html

document.addEventListener('DOMContentLoaded', () => {

    const video = document.getElementById('cameraPreview');
    const captureBtn = document.getElementById('captureBtn');
    const switchCameraBtn = document.getElementById('switchCameraBtn');
    const imageUploadInput = document.getElementById('imageUploadInput');
    const loadingOverlay = document.getElementById('loadingOverlay');

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
                // Support legacy prefixes if needed
                const getUserMedia = (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) ||
                    navigator.webkitGetUserMedia ||
                    navigator.mozGetUserMedia;

                if (typeof getUserMedia === 'function') {
                    // If using legacy, we need to bind context
                    if (navigator.mediaDevices) {
                        currentStream = await navigator.mediaDevices.getUserMedia({ video: true });
                    } else {
                        // Legacy callback-style wrapped in Promise
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
        if (loadingOverlay) {
            loadingOverlay.hidden = !show;
        }
        if (captureBtn) {
            captureBtn.disabled = show;
            captureBtn.style.opacity = show ? "0.5" : "1";
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
        if (name) {
            // If name is already known (from file upload), skip AI and send to backend
            sendToBackend(imageBlob, name);
            return;
        }

        try {
            // Show the "Analyzing..." spinner
            showLoading(true);

            // Convert Blob to Data URL (Keeping this just in case it's needed later, but not strictly required for the prompt)
            const reader = new FileReader();
            reader.readAsDataURL(imageBlob);
            reader.onloadend = async () => {
                console.log("Bypassing Puter AI to avoid login popup...");

                // Safety timeout: If AI doesn't respond in 15s, stop loading
                const timeout = setTimeout(() => {
                    showLoading(false);
                }, 15000);

                // Simulate AI delay and ask user for food name to test the pipeline
                setTimeout(() => {
                    clearTimeout(timeout);
                    const userInput = prompt("Puter AI is disabled to prevent the login popup.\nFor testing, please enter the food name (e.g., Apple, Banana):", "Apple");
                    
                    if (userInput) {
                        const identifiedName = userInput.toString().trim().toLowerCase().replace(/[^a-z ]/g, "");
                        console.log("Manually identified:", identifiedName);
                        sendToBackend(imageBlob, identifiedName);
                    } else {
                        // User cancelled
                        showLoading(false);
                    }
                }, 500);
            };

        } catch (error) {
            console.error("Upload error:", error);
            alert("Error: " + error.message);
            showLoading(false);
        }
    }

    async function sendToBackend(imageBlob, identifiedName) {
        try {
            const formData = new FormData();
            formData.append('food_image', imageBlob, 'capture.jpg');
            if (identifiedName) {
                formData.append('food_name', identifiedName);
            }

            const response = await fetch('/api/food/identify', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.message || "Failed to log food.");

            // Stop camera and redirect
            if (currentStream) {
                currentStream.getTracks().forEach(track => track.stop());
            }
            if (data.food_id) {
                window.location.href = `/analysis/${data.food_id}`;
            }
        } catch (err) {
            console.error("Backend error:", err);
            alert("Food identified, but failed to retrieve nutrition data.");
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
                // ALWAYS use AI identification for uploads to get clean names
                uploadFoodImage(file);
            }
        });
    }
});
