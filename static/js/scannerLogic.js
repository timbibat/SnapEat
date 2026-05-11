/**
 * Handles camera access, image capture, and image data preparation for food analysis.
 * Uses Puter.js (gpt-5.4-nano) for frontend AI identification.
 */

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

        // Security check: getUserMedia requires HTTPS or localhost
        if (location.protocol !== 'https:' && location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {
            console.error("Camera access blocked: Insecure context (requires HTTPS)");
            alert("Security Error: Camera access requires an HTTPS connection. Please ensure your site is served over SSL.");
            return;
        }

        // Stop existing stream
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
        }

        // Try high-resolution environment camera first
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
            video.onloadedmetadata = () => {
                video.play().catch(e => console.error("Video play failed:", e));
            };
        } catch (error) {
            console.warn("Primary camera constraints failed, trying fallback...", error);
            
            // FALLBACK: Try a very simple constraint if the first one fails
            try {
                currentStream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = currentStream;
                video.play();
            } catch (fallbackError) {
                console.error("Camera access error:", fallbackError);
                alert(`Could not access camera.\n\nTips for Median.co/Mobile:\n1. Ensure your site uses HTTPS.\n2. Allow Camera permissions in your phone settings for the app.\n3. Make sure no other app is using the camera.`);
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

            // Convert Blob to Data URL for Puter.js
            const reader = new FileReader();
            reader.readAsDataURL(imageBlob);
            reader.onloadend = async () => {
                const dataUrl = reader.result;
                
                console.log("Analyzing with Puter AI (gpt-5.4-nano)...");
                
                // Call Puter.js AI
                puter.ai.chat(
                    "Identify the primary food item in this image. Return ONLY the name of the food (e.g., 'Apple', 'Pizza').",
                    dataUrl,
                    { model: "gpt-5.4-nano" }
                )
                .then(response => {
                    const identifiedName = response.toString().trim().toLowerCase().replace(".", "");
                    console.log("Puter identified:", identifiedName);
                    
                    // Send identified name to backend for nutrition data
                    sendToBackend(imageBlob, identifiedName);
                })
                .catch(err => {
                    console.error("Puter Error:", err);
                    alert("AI Analysis failed. Please try again.");
                    showLoading(false);
                });
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
