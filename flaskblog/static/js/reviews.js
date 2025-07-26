/**
 * Review System JavaScript for Flask Blog
 */

class ReviewManager {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.initStarRatings();
    }

    bindEvents() {
        // Like/Dislike buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('like-btn')) {
                this.handleLikeDislike(e.target, 'like');
            } else if (e.target.classList.contains('dislike-btn')) {
                this.handleLikeDislike(e.target, 'dislike');
            }
        });

        // Star rating selection in forms
        document.addEventListener('change', (e) => {
            if (e.target.name === 'rating') {
                this.updateStarDisplay(e.target);
            }
        });
    }

    handleLikeDislike(button, action) {
        const reviewId = button.dataset.reviewId;
        
        if (!reviewId) return;

        // Disable button temporarily
        button.disabled = true;

        fetch(`/review/${reviewId}/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update counts
                const likesSpan = button.parentElement.querySelector('.likes-count');
                const dislikesSpan = button.parentElement.querySelector('.dislikes-count');
                
                if (likesSpan) likesSpan.textContent = data.likes;
                if (dislikesSpan) dislikesSpan.textContent = data.dislikes;

                // Add visual feedback
                button.classList.add('clicked');
                setTimeout(() => button.classList.remove('clicked'), 300);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        })
        .finally(() => {
            button.disabled = false;
        });
    }

    initStarRatings() {
        // Display existing ratings
        document.querySelectorAll('.star-rating').forEach(rating => {
            const stars = rating.dataset.rating;
            this.displayStars(rating, parseInt(stars));
        });

        // Interactive star rating for forms
        document.querySelectorAll('.star-input').forEach(starContainer => {
            this.makeStarsInteractive(starContainer);
        });
    }

    displayStars(container, rating) {
        const maxStars = 5;
        let html = '';
        
        for (let i = 1; i <= maxStars; i++) {
            if (i <= rating) {
                html += '<i class="fas fa-star star"></i>';
            } else {
                html += '<i class="far fa-star star empty"></i>';
            }
        }
        
        container.innerHTML = html;
    }

    makeStarsInteractive(container) {
        const stars = container.querySelectorAll('.star');
        const hiddenInput = container.querySelector('input[type="hidden"]');

        stars.forEach((star, index) => {
            star.addEventListener('click', () => {
                const rating = index + 1;
                hiddenInput.value = rating;
                this.displayStars(container, rating);
                
                // Update select element if exists
                const select = document.querySelector('select[name="rating"]');
                if (select) {
                    select.value = rating;
                }
            });

            star.addEventListener('mouseover', () => {
                this.displayStars(container, index + 1);
            });
        });

        container.addEventListener('mouseleave', () => {
            const currentRating = hiddenInput.value || 0;
            this.displayStars(container, parseInt(currentRating));
        });
    }

    updateStarDisplay(selectElement) {
        const rating = parseInt(selectElement.value);
        const starContainer = document.querySelector('.star-input');
        
        if (starContainer) {
            this.displayStars(starContainer, rating);
            const hiddenInput = starContainer.querySelector('input[type="hidden"]');
            if (hiddenInput) {
                hiddenInput.value = rating;
            }
        }
    }

    getCSRFToken() {
        const token = document.querySelector('meta[name="csrf-token"]');
        return token ? token.getAttribute('content') : '';
    }
}

// Star rating utility functions
function createStarRating(rating, maxStars = 5) {
    let html = '<div class="star-rating" data-rating="' + rating + '">';
    
    for (let i = 1; i <= maxStars; i++) {
        if (i <= rating) {
            html += '<i class="fas fa-star star"></i>';
        } else {
            html += '<i class="far fa-star star empty"></i>';
        }
    }
    
    html += '</div>';
    return html;
}

// Initialize review manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new ReviewManager();
    
    // Add animation to review items
    const reviewItems = document.querySelectorAll('.review-item');
    reviewItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
        item.classList.add('slide-in');
    });
    
    // Auto-expand textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
});

// Add CSS for clicked animation
const style = document.createElement('style');
style.textContent = `
    .like-btn.clicked, .dislike-btn.clicked {
        transform: scale(1.2);
        transition: transform 0.3s ease;
    }
    
    .star {
        cursor: pointer;
        transition: color 0.2s ease;
    }
    
    .star:hover {
        color: #ffc107 !important;
    }
`;
document.head.appendChild(style);