/**
 * Social Sharing and Additional Features for Flask Blog
 */

// Social sharing functionality
function sharePost(postId, title, url) {
    if (navigator.share) {
        // Use native sharing if available (PWA)
        navigator.share({
            title: title,
            text: 'Check out this blog post: ' + title,
            url: url
        }).then(() => {
            console.log('Post shared successfully');
        }).catch((error) => {
            console.log('Error sharing:', error);
            fallbackShare(title, url);
        });
    } else {
        fallbackShare(title, url);
    }
}

function fallbackShare(title, url) {
    // Fallback sharing options
    const shareData = {
        title: encodeURIComponent(title),
        url: encodeURIComponent(url),
        text: encodeURIComponent('Check out this blog post: ' + title)
    };
    
    // Create sharing modal
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Share Post</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="d-grid gap-2">
                        <a href="https://twitter.com/intent/tweet?text=${shareData.text}&url=${shareData.url}" 
                           target="_blank" class="btn btn-primary">
                            <i class="fab fa-twitter me-2"></i>Share on Twitter
                        </a>
                        <a href="https://www.facebook.com/sharer/sharer.php?u=${shareData.url}" 
                           target="_blank" class="btn btn-primary">
                            <i class="fab fa-facebook me-2"></i>Share on Facebook
                        </a>
                        <a href="https://www.linkedin.com/sharing/share-offsite/?url=${shareData.url}" 
                           target="_blank" class="btn btn-primary">
                            <i class="fab fa-linkedin me-2"></i>Share on LinkedIn
                        </a>
                        <button class="btn btn-secondary" onclick="copyToClipboard('${url}')">
                            <i class="fas fa-copy me-2"></i>Copy Link
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
    
    modal.addEventListener('hidden.bs.modal', () => {
        document.body.removeChild(modal);
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show success message
        const toast = document.createElement('div');
        toast.className = 'toast-container position-fixed top-0 end-0 p-3';
        toast.innerHTML = `
            <div class="toast show" role="alert">
                <div class="toast-header">
                    <strong class="me-auto">Success</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">
                    Link copied to clipboard!
                </div>
            </div>
        `;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 3000);
    });
}

// Enhanced error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // You could send this to a logging service
});

// Performance monitoring
window.addEventListener('load', function() {
    if ('performance' in window) {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart + 'ms');
        }, 0);
    }
});

// Install prompt for PWA
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    // Show install button
    const installBtn = document.createElement('button');
    installBtn.className = 'btn btn-success position-fixed';
    installBtn.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000;';
    installBtn.innerHTML = '<i class="fas fa-download me-1"></i>Install App';
    installBtn.onclick = () => {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the install prompt');
            }
            deferredPrompt = null;
            document.body.removeChild(installBtn);
        });
    };
    
    document.body.appendChild(installBtn);
    
    // Auto-hide after 10 seconds
    setTimeout(() => {
        if (installBtn.parentNode) {
            document.body.removeChild(installBtn);
        }
    }, 10000);
});

// Initialize enhanced features
document.addEventListener('DOMContentLoaded', function() {
    // Add share buttons to posts if they exist
    const posts = document.querySelectorAll('.article-title');
    posts.forEach(post => {
        const shareBtn = document.createElement('button');
        shareBtn.className = 'btn btn-sm btn-outline-primary ms-2';
        shareBtn.innerHTML = '<i class="fas fa-share-alt"></i>';
        shareBtn.onclick = () => {
            const url = window.location.origin + post.getAttribute('href');
            const title = post.textContent;
            sharePost(null, title, url);
        };
        post.parentNode.appendChild(shareBtn);
    });
});