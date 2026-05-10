/**
 * Handles authentication logic including login, signup, password recovery.
 *
 * NOTE: BOOTSTRAP FRAMEWORK AHHH
 *
 * EXPECTED HTML DOM ELEMENTS (To be implemented by the HTML Developer):
 *
 * 1. Login Page:
 *    - Form: ID 'loginForm'
 *    - Inputs: ID 'loginEmail', ID 'loginPassword'
 *
 * 2. Signup Page:
 *    - Form: ID 'signupForm'
 *    - Inputs: ID 'signupName', ID 'signupEmail', ID 'signupPassword', ID 'signupConfirmPassword'
 *
 * 3. Forgot Password Page:
 *    - Form: ID 'forgotPasswordForm'
 *    - Inputs: ID 'forgotEmail'
 */

document.addEventListener('DOMContentLoaded', () => {

    // --- Password Visibility Toggle ---
    function setupPasswordToggle(inputId, iconId) {
        const input = document.getElementById(inputId);
        const icon = document.getElementById(iconId);
        if (input && icon) {
            icon.addEventListener('click', function() {
                if (input.type === 'password') {
                    input.type = 'text';
                    icon.classList.remove('bi-eye-slash');
                    icon.classList.add('bi-eye');
                } else {
                    input.type = 'password';
                    icon.classList.remove('bi-eye');
                    icon.classList.add('bi-eye-slash');
                }
            });
        }
    }

    setupPasswordToggle('loginPassword', 'togglePasswordIcon');
    setupPasswordToggle('signupPassword', 'toggleSignupPasswordIcon');
    setupPasswordToggle('signupConfirmPassword', 'toggleConfirmPasswordIcon');

    // --- Login Logic ---
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('loginEmail')?.value;
            const password = document.getElementById('loginPassword')?.value;

            if (!email || !password) {
                AppMain.showToast("Please enter email and password.", "error");
                return;
            }

            AppMain.showLoader();
            try {
                const response = await AppMain.apiCall('/api/auth/login', {
                    method: 'POST',
                    body: JSON.stringify({ email, password })
                });

                if (response.status === 'success' || response.token) {
                    AppMain.showToast("Login successful!", "success");
                    // Save token if needed: localStorage.setItem('token', response.token);
                    window.location.href = '/';
                }
            } catch (error) {
                // Error handled by AppMain.apiCall toast
            } finally {
                AppMain.hideLoader();
            }
        });
    }

    // --- Signup Logic ---
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('signupName')?.value;
            const email = document.getElementById('signupEmail')?.value;
            const password = document.getElementById('signupPassword')?.value;
            const confirmPassword = document.getElementById('signupConfirmPassword')?.value;

            if (password !== confirmPassword) {
                AppMain.showToast("Passwords do not match.", "error");
                return;
            }

            AppMain.showLoader();
            try {
                const response = await AppMain.apiCall('/api/auth/signup', {
                    method: 'POST',
                    body: JSON.stringify({ name, email, password })
                });

                if (response.status === 'success') {
                    AppMain.showToast("Signup successful! Please login.", "success");
                    window.location.href = '/login';
                }
            } catch (error) {
                // Error handled by AppMain.apiCall
            } finally {
                AppMain.hideLoader();
            }
        });
    }

    // --- Forgot Password Logic ---
    const forgotForm = document.getElementById('forgotPasswordForm');
    if (forgotForm) {
        forgotForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('forgotEmail')?.value;

            if (!email) {
                AppMain.showToast("Please enter your email address.", "error");
                return;
            }

            AppMain.showLoader();
            try {
                const response = await AppMain.apiCall('/api/auth/forgot-password', {
                    method: 'POST',
                    body: JSON.stringify({ email })
                });

                AppMain.showToast("Password reset link sent to your email.", "success");
            } catch (error) {
                // Error handled by AppMain.apiCall
            } finally {
                AppMain.hideLoader();
            }
        });
    }

});
