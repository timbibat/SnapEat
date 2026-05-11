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
                console.info("Median.co detected. If the login popup is blank, ensure 'puter.com' is in your Internal Domains list.");
            }

            return Promise.resolve();
        },

        init() {
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
