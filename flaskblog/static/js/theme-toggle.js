/**
 * Theme Toggle Functionality for Flask Blog
 */

class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Set initial theme
        this.setTheme(this.currentTheme);
        
        // Create theme toggle button
        this.createThemeToggle();
        
        // Listen for system theme changes
        this.listenForSystemTheme();
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.currentTheme = theme;
        this.updateToggleButton();
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    createThemeToggle() {
        const themeToggle = document.createElement('button');
        themeToggle.className = 'theme-toggle';
        themeToggle.setAttribute('aria-label', 'Toggle theme');
        themeToggle.innerHTML = this.getToggleIcon();
        
        // Add to navbar
        const navbar = document.querySelector('.navbar-nav');
        if (navbar) {
            const themeItem = document.createElement('li');
            themeItem.className = 'nav-item';
            themeItem.appendChild(themeToggle);
            navbar.appendChild(themeItem);
        }
        
        // Add click event
        themeToggle.addEventListener('click', () => this.toggleTheme());
    }

    getToggleIcon() {
        if (this.currentTheme === 'light') {
            return '<i class="fas fa-moon"></i>';
        } else {
            return '<i class="fas fa-sun"></i>';
        }
    }

    updateToggleButton() {
        const toggleButton = document.querySelector('.theme-toggle');
        if (toggleButton) {
            toggleButton.innerHTML = this.getToggleIcon();
        }
    }

    listenForSystemTheme() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                if (!localStorage.getItem('theme')) {
                    this.setTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    }
}

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new ThemeManager();
    
    // Add fade-in animation to content sections
    const contentSections = document.querySelectorAll('.content-section');
    contentSections.forEach((section, index) => {
        section.style.animationDelay = `${index * 0.1}s`;
        section.classList.add('fade-in');
    });
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Add loading animation
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});