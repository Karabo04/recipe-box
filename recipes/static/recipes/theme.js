(() => {
    const root = document.documentElement;
    const toggle = document.querySelector('.theme-toggle');

    if (!toggle) return;

    const syncToggle = () => {
        const isDark = root.dataset.theme === 'dark';
        toggle.setAttribute('aria-pressed', String(isDark));
        toggle.setAttribute('aria-label', `Switch to ${isDark ? 'light' : 'dark'} mode`);
        toggle.querySelector('.theme-icon').textContent = isDark ? '☀' : '☾';
        toggle.querySelector('.theme-label').textContent = isDark ? 'Light' : 'Dark';
        document.querySelector('meta[name="theme-color"]')?.setAttribute('content', isDark ? '#171c19' : '#f7f5ef');
    };

    syncToggle();
    toggle.addEventListener('click', () => {
        root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
        try {
            localStorage.setItem('recipe-theme', root.dataset.theme);
        } catch (error) {
            // Keep the current selection for this page when storage is unavailable.
        }
        syncToggle();
    });
})();
