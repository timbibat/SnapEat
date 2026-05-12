/**
 * Handles Puter auth bootstrapping for scanner pages.
 */
(function (window, document) {
    const PuterAuth = {
        getAuthToken() {
            return window.DomUtils?.getBodyData('puterAuthToken', '') || '';
        },

        isMedianEnvironment() {
            return navigator.userAgent.includes('GoNative') || Boolean(window.gonative);
        },

        setupMedianBridge() {
            if (!this.isMedianEnvironment()) return;

            console.info("Median.co environment detected. Setting up Link Interceptor...");

            // Intercept window.open calls which Puter.js uses for the login popup
            const originalOpen = window.open;
            window.open = (url, name, specs) => {
                if (!url) return originalOpen(url, name, specs);

                const urlStr = url.toString();
                // If it's a Puter or Google auth domain, force it to be internal
                if (urlStr.includes('puter.com') || urlStr.includes('google.com') || urlStr.includes('accounts.google')) {
                    console.log("Median Bridge: Forcing internal opening for:", urlStr);
                    window.location.href = "gonative://urls/open?url=" + encodeURIComponent(urlStr) + "&internal=true";
                    return null;
                }
                return originalOpen(url, name, specs);
            };
        },

        getScanUrl() {
            return new URL('/scan', window.location.origin).toString();
        },

        redirectToScan() {
            window.location.replace(PuterAuth.getScanUrl());
        },

        signInAndReturnToScan(options = {}) {
            if (!window.puter?.auth) {
                return Promise.reject(new Error('Puter SDK is not available.'));
            }

            sessionStorage.setItem('puterReturnTo', PuterAuth.getScanUrl());

            return window.puter.auth.signIn(options)
                .then((result) => {
                    sessionStorage.removeItem('puterReturnTo');
                    PuterAuth.redirectToScan();
                    return result;
                });
        },

        checkAuth(authToken = PuterAuth.getAuthToken()) {
            if (!window.puter?.auth) {
                console.warn('Puter Auth: Puter SDK is not available.');
                return Promise.resolve();
            }

            if (authToken && authToken !== 'None') {
                return window.puter.auth.signInWithToken(authToken)
                    .then(() => {
                        console.log('Puter: Silently signed in with token.');
                    })
                    .catch((err) => {
                        console.error('Puter Auth Error:', err);
                    });
            }

            console.warn('Puter Auth: No token found. Login may be required.');
            if (PuterAuth.isMedianEnvironment()) {
                console.info("Median.co detected. IMPORTANT: Ensure 'puter.com', 'google.com', and 'accounts.google.com' are in your Internal Domains list.");
            }

            if (sessionStorage.getItem('puterReturnTo') && window.puter.auth.isSignedIn()) {
                sessionStorage.removeItem('puterReturnTo');
                PuterAuth.redirectToScan();
            }

            return Promise.resolve();
        },

        init() {
            this.setupMedianBridge();

            if (!window.puter?.ready) {
                console.warn('Puter Auth: Puter SDK did not expose ready().');
                return;
            }

            window.puter.ready().then(() => PuterAuth.checkAuth());
        }
    };

    window.PuterAuth = PuterAuth;
    window.DomUtils?.ready(() => PuterAuth.init());
})(window, document);
