/**
 * SnapEat - History Log Frontend Logic
 * Implements real-time filtering, search, sorting, and stats calculation.
 */

window.DomUtils.ready(() => {
    // --- Context & DOM elements ---
    const userEmail = document.body.dataset.userEmail || 'default';
    const username = document.body.dataset.userName || '';
    
    const historyList = DomUtils.byId('historyList');
    const historyEmptyState = DomUtils.byId('historyEmptyState');
    const historySearchInput = DomUtils.byId('historySearchInput');
    const historyFilterRating = DomUtils.byId('historyFilterRating');
    const historySort = DomUtils.byId('historySort');
    
    // Stats elements
    const statTotalScans = DomUtils.byId('statTotalScans');
    const statAvgScore = DomUtils.byId('statAvgScore');
    const statTodayCalories = DomUtils.byId('statTodayCalories');
    
    // In-memory data store for live filtering/sorting
    let originalScans = [];
    let filteredScans = [];

    // --- Category Emoji Map ---
    const categoryEmojis = {
        'beverages': '🥤',
        'drinks': '🥤',
        'dairy': '🥛',
        'fruits': '🍎',
        'fruit': '🍎',
        'vegetables': '🥗',
        'vegetable': '🥗',
        'salad': '🥗',
        'bakery': '🍞',
        'bread': '🍞',
        'meat': '🥩',
        'seafood': '🐟',
        'fish': '🐟',
        'snacks': '🍿',
        'snack': '🍿',
        'sweets': '🍬',
        'dessert': '🍰',
        'grains': '🌾',
        'fast food': '🍔',
        'junk food': '🍕',
        'default': '🍽️'
    };

    function getCategoryEmoji(category, name) {
        const catLower = (category || '').toLowerCase();
        const nameLower = (name || '').toLowerCase();
        
        // Try direct category match
        if (categoryEmojis[catLower]) return categoryEmojis[catLower];
        
        // Search inside category name
        for (const [key, emoji] of Object.entries(categoryEmojis)) {
            if (catLower.includes(key) || nameLower.includes(key)) {
                return emoji;
            }
        }
        
        return categoryEmojis.default;
    }

    // --- Date Formatter ---
    function formatDateTime(dbDateStr) {
        if (!dbDateStr) return '';
        
        // SQLite returns timestamps as 'YYYY-MM-DD HH:MM:SS' in UTC
        // Parse manually to avoid browser inconsistencies
        const t = dbDateStr.split(/[- :]/);
        if (t.length < 6) return dbDateStr;
        
        const utcDate = new Date(Date.UTC(t[0], t[1] - 1, t[2], t[3], t[4], t[5]));
        
        const today = new Date();
        const yesterday = new Date();
        yesterday.setDate(today.getDate() - 1);
        
        const isToday = utcDate.toLocaleDateString() === today.toLocaleDateString();
        const isYesterday = utcDate.toLocaleDateString() === yesterday.toLocaleDateString();
        
        const timeOptions = { hour: 'numeric', minute: '2-digit', hour12: true };
        const formattedTime = utcDate.toLocaleTimeString([], timeOptions);
        
        if (isToday) {
            return `Today, ${formattedTime}`;
        } else if (isYesterday) {
            return `Yesterday, ${formattedTime}`;
        } else {
            const dateOptions = { month: 'short', day: 'numeric', year: 'numeric' };
            return `${utcDate.toLocaleDateString([], dateOptions)} • ${formattedTime}`;
        }
    }

    // --- Load History Data ---
    async function loadHistory() {
        AppMain.showLoader();
        try {
            // 1. Fetch recent scans (limit 100)
            const scansResponse = await AppMain.apiCall(`/api/user/recent?user_id=${encodeURIComponent(userEmail)}&limit=100`);
            originalScans = scansResponse.scans || [];
            
            // 2. Fetch today's totals for calories stat
            const todayResponse = await AppMain.apiCall(`/api/user/log?user_id=${encodeURIComponent(userEmail)}`);
            const todayTotals = todayResponse.totals || {};
            
            // Render dashboard stats
            updateStatsDashboard(todayTotals);
            
            // Initialize filter & render
            applyFiltersAndSort();
        } catch (error) {
            console.error("Error loading scan history:", error);
            AppMain.showToast("Failed to load your history. Please refresh.", "error");
        } finally {
            AppMain.hideLoader();
        }
    }

    // --- Update Quick Stats Widgets ---
    function updateStatsDashboard(todayTotals) {
        // Total scans count
        statTotalScans.textContent = originalScans.length;
        
        // Average Health Score calculation
        if (originalScans.length > 0) {
            const sumScores = originalScans.reduce((sum, item) => sum + (item.health_score || 0), 0);
            const avg = Math.round(sumScores / originalScans.length);
            statAvgScore.textContent = `${avg}/100`;
        } else {
            statAvgScore.textContent = '--';
        }
        
        // Today's Calories
        const calories = todayTotals.total_calories || 0;
        statTodayCalories.textContent = `${Math.round(calories)} kcal`;
    }

    // --- Apply Filters and Sorting ---
    function applyFiltersAndSort() {
        const searchQuery = (historySearchInput?.value || '').toLowerCase().trim();
        const ratingFilter = historyFilterRating?.value || 'all';
        const sortType = historySort?.value || 'date_desc';
        
        // 1. Filter original list
        filteredScans = originalScans.filter(item => {
            const matchesSearch = item.food_name.toLowerCase().includes(searchQuery) || 
                                  (item.category || '').toLowerCase().includes(searchQuery);
            
            const matchesRating = ratingFilter === 'all' || 
                                  (item.health_status || '').toLowerCase() === ratingFilter;
                                  
            return matchesSearch && matchesRating;
        });

        // 2. Sort filtered list
        filteredScans.sort((a, b) => {
            if (sortType === 'date_desc') {
                return new Date(b.scanned_at + ' UTC') - new Date(a.scanned_at + ' UTC');
            } else if (sortType === 'date_asc') {
                return new Date(a.scanned_at + ' UTC') - new Date(b.scanned_at + ' UTC');
            } else if (sortType === 'score_desc') {
                return (b.health_score || 0) - (a.health_score || 0);
            } else if (sortType === 'score_asc') {
                return (a.health_score || 0) - (b.health_score || 0);
            }
            return 0;
        });

        // 3. Render list in DOM
        renderScansList();
    }

    // --- Render Scans List to DOM ---
    function renderScansList() {
        historyList.innerHTML = '';
        
        // If the database has absolutely NO scans for this user, show the main empty state
        if (originalScans.length === 0) {
            historyEmptyState.style.display = 'block';
            // Hide filter panel and stats row
            const filterPanel = document.querySelector('.filter-panel');
            const statsRow = document.querySelector('.stats-row');
            if (filterPanel) filterPanel.style.display = 'none';
            if (statsRow) statsRow.style.display = 'none';
            return;
        }
        
        // If filters return no matching logs
        if (filteredScans.length === 0) {
            historyList.innerHTML = `
                <div class="text-center py-5 bg-white rounded-4 shadow-sm border border-light-subtle">
                    <i class="bi bi-search text-muted mb-3" style="font-size: 2.5rem; display: block;"></i>
                    <h5 class="fw-bold text-dark">No Matching Items Found</h5>
                    <p class="text-muted mb-0">Try adjusting your search keywords or health rating filters.</p>
                </div>
            `;
            return;
        }

        historyEmptyState.style.display = 'none';
        
        // Build cards
        filteredScans.forEach((item, index) => {
            const card = document.createElement('div');
            card.className = 'history-item';
            // Stagger animation timing for premium effect
            card.style.animationDelay = `${index * 0.05}s`;
            
            const emoji = getCategoryEmoji(item.category, item.food_name);
            const formattedTime = formatDateTime(item.scanned_at);
            const statusClass = (item.health_status || 'good').toLowerCase();
            
            // Build nutrition pills content
            const cals = Math.round(item.calories || 0);
            const carbs = Math.round(item.carbs || 0);
            const protein = Math.round(item.protein || 0);
            const fat = Math.round(item.fat || 0);
            
            card.innerHTML = `
                <!-- Left Section: Avatar & Info -->
                <div class="food-meta">
                    <div class="food-avatar">
                        ${emoji}
                    </div>
                    <div class="food-details">
                        <h4 class="food-name">${item.food_name}</h4>
                        <div class="food-category-time">
                            <span>${item.category || 'Logged Food'}</span>
                            <span class="bullet-separator"></span>
                            <span>${formattedTime}</span>
                        </div>
                    </div>
                </div>
                
                <!-- Middle Section: Nutrition Mini-Pill Grid -->
                <div class="nutrition-grid my-2 my-lg-0">
                    <div class="nutrition-pill">
                        <span class="nutrition-pill-val">${cals}</span>
                        <span class="nutrition-pill-lbl">kcal</span>
                    </div>
                    <div class="nutrition-pill">
                        <span class="nutrition-pill-val">${carbs}g</span>
                        <span class="nutrition-pill-lbl">carbs</span>
                    </div>
                    <div class="nutrition-pill">
                        <span class="nutrition-pill-val">${protein}g</span>
                        <span class="nutrition-pill-lbl">pro</span>
                    </div>
                    <div class="nutrition-pill">
                        <span class="nutrition-pill-val">${fat}g</span>
                        <span class="nutrition-pill-lbl">fat</span>
                    </div>
                </div>
                
                <!-- Right Section: Rating Badge, Score circle & Action button -->
                <div class="badge-and-score-wrapper d-flex align-items-center gap-3">
                    <span class="badge-health ${statusClass}">
                        <i class="bi bi-circle-fill" style="font-size: 0.5rem;"></i> ${item.health_status || 'Good'}
                    </span>
                    
                    <div class="score-circle-wrapper">
                        <div class="score-circle ${statusClass}">
                            ${item.health_score || 0}
                        </div>
                        <span class="score-label">Score</span>
                    </div>
                    
                    <a href="/analysis/${encodeURIComponent(item.food_name.toLowerCase())}" class="btn-view-details" title="View Full Analysis">
                        <i class="bi bi-arrow-right-short"></i>
                    </a>
                </div>
            `;
            
            historyList.appendChild(card);
        });
    }

    // --- Wire Up Live Search & Filters ---
    if (historySearchInput) {
        historySearchInput.addEventListener('input', applyFiltersAndSort);
    }
    if (historyFilterRating) {
        historyFilterRating.addEventListener('change', applyFiltersAndSort);
    }
    if (historySort) {
        historySort.addEventListener('change', applyFiltersAndSort);
    }

    // --- Kickstart Ingestion ---
    loadHistory();
});
