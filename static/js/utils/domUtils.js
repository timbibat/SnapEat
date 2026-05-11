/**
 * Shared DOM helpers for plain-script pages.
 */
(function (window, document) {
    const DomUtils = {
        ready(callback) {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', callback, { once: true });
                return;
            }

            callback();
        },

        byId(id) {
            return document.getElementById(id);
        },

        setHidden(element, hidden) {
            if (element) {
                element.hidden = hidden;
            }
        },

        setDisabled(element, disabled) {
            if (element) {
                element.disabled = disabled;
            }
        },

        getBodyData(name, fallback = '') {
            return document.body?.dataset?.[name] || fallback;
        }
    };

    window.DomUtils = DomUtils;
})(window, document);
