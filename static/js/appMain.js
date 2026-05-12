/**
 * Shared application helpers for API calls and optional global UI elements.
 */

const AppMain = {
    /**
     * Shows a global loading overlay
     */
    showLoader: function () {
        const loader = window.DomUtils?.byId('global-loader') || document.getElementById('global-loader');
        if (loader) {
            loader.style.display = 'flex';
        }
    },

    /**
     * Hides the global loading overlay
     */
    hideLoader: function () {
        const loader = window.DomUtils?.byId('global-loader') || document.getElementById('global-loader');
        if (loader) {
            loader.style.display = 'none';
        }
    },

    /**
     * Displays a toast notification message to the user.
     * @param {string} message - The message to display.
     * @param {string} type - 'error', 'success', or 'info'
     */
    showToast: function (message, type = 'info') {
        const toast = window.DomUtils?.byId('global-toast') || document.getElementById('global-toast');
        if (toast) {
            toast.textContent = message;
            toast.className = `toast show ${type}`;

            // Auto hide after 3 seconds
            setTimeout(() => {
                toast.className = 'toast hidden';
            }, 3000);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
            if (type === 'error') {
                alert(message);
            }
        }
    },

    /**
     * Handles API requests with built-in error handling and JSON parsing
     * @param {string} url - The endpoint URL
     * @param {object} options - Fetch options (method, headers, body, etc)
     */
    apiCall: async function (url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Something went wrong');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            AppMain.showToast(error.message, 'error');
            throw error;
        }
    }
};

window.AppMain = AppMain;
