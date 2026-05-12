/**
 * Handles Puter auth bootstrapping for scanner pages.
 * Optimized for Median.co (GoNative) and mobile webviews.
 */
(function (window, document) {
    const PuterAuth = {
        getAuthToken() {
            return window.DomUtils?.getBodyData('puterAuthToken', '') || '';
        },

        isMedianEnvironment() {
            // Check for UA markers or injected JS bridge objects
            return navigator.userAgent.includes('GoNative') || 
                   navigator.userAgent.includes('Median') ||
                   Boolean(window.gonative) || 
                   Boolean(window.median);
        },

        setupMedianBridge() {
            if (!this.isMedianEnvironment()) return;

            console.info("Median.co environment detected. Setting up Link Interceptor...");

            // Intercept window.open calls which Puter.js uses for the login popup
            const originalOpen = window.open;
            window.open = (url, name, specs) => {
                if (!url) return originalOpen(url, name, specs);

                const urlStr = url.toString();
                
                // For Google Auth specifically, if User Agent is overridden in Dashboard,
                // we can try to open it internally. Otherwise, it might still need Chrome.
                if (urlStr.includes('puter.com') || urlStr.includes('google.com') || urlStr.includes('accounts.google')) {
                    console.log("Median Bridge: Routing auth URL through app container:", urlStr);
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

            // In Median/Mobile, popups are often blocked or fail to redirect back.
            // Using 'redirect: true' forces Puter to use the current window for login.
            if (this.isMedianEnvironment() || /Android|iPhone|iPad/i.test(navigator.userAgent)) {
                console.info("Using Puter Redirect flow for mobile/webview compatibility...");
                return window.puter.auth.signIn({ ...options, redirect: true });
            }

            // Default popup flow for Desktop
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

            // 1. Check if we just returned from a redirect login
            if (window.puter.auth.isSignedIn()) {
                console.log('Puter: User is signed in.');
                if (sessionStorage.getItem('puterReturnTo')) {
                    sessionStorage.removeItem('puterReturnTo');
                    PuterAuth.redirectToScan();
                }
                return Promise.resolve();
            }

            // 2. Try to sign in with provided token from backend
            if (authToken && authToken !== 'None') {
                return window.puter.auth.signInWithToken(authToken)
                    .then(() => {
                        console.log('Puter: Silently signed in with token.');
                    })
                    .catch((err) => {
                        console.error('Puter Auth Error:', err);
                    });
            }

            console.warn('Puter Auth: No session found. Login may be required.');
            
            if (PuterAuth.isMedianEnvironment()) {
                console.info("Median.co environment active.");
                // Reminder: disallowed_useragent fix requires Dashboard UA change.
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
