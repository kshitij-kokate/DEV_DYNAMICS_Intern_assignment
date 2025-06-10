// Main JavaScript file for SplitApp
// Enhanced interactions and animations for modern UI

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeAnimations();
    initializeFormEnhancements();
    initializeTooltips();
    initializeLoadingStates();
    initializeSmoothScrolling();
    
    console.log('SplitApp initialized successfully');
});

// Animation System
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all cards and stats elements
    document.querySelectorAll('.card, .stats-card, .list-group-item').forEach(el => {
        observer.observe(el);
    });
    
    // Add stagger animation to multiple elements
    const staggerElements = document.querySelectorAll('.stats-card');
    staggerElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
    });
}

// Form Enhancement System
function initializeFormEnhancements() {
    // Enhanced number input formatting
    const amountInputs = document.querySelectorAll('input[type="number"]');
    amountInputs.forEach(input => {
        // Format on blur
        input.addEventListener('blur', function() {
            if (this.value && !isNaN(this.value)) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
        
        // Real-time validation
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value < 0) {
                this.setCustomValidity('Amount must be positive');
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
            }
        });
    });
    
    // Text input enhancements
    const textInputs = document.querySelectorAll('input[type="text"]');
    textInputs.forEach(input => {
        // Auto-capitalize first letter for description fields
        if (input.id === 'description') {
            input.addEventListener('input', function() {
                if (this.value.length === 1) {
                    this.value = this.value.charAt(0).toUpperCase();
                }
            });
        }
        
        // Auto-format person names
        if (input.id === 'paid_by') {
            input.addEventListener('input', function() {
                const words = this.value.split(' ');
                const formattedWords = words.map(word => {
                    if (word.length > 0) {
                        return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
                    }
                    return word;
                });
                this.value = formattedWords.join(' ');
            });
        }
    });
    
    // Form submission with loading state
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                showLoadingState(submitBtn);
            }
        });
    });
}

// Loading States
function showLoadingState(button) {
    if (!button) return;
    
    const originalContent = button.innerHTML;
    button.disabled = true;
    button.innerHTML = `
        <div class="spinner-border spinner-border-sm me-2" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        Processing...
    `;
    
    // Reset after 5 seconds as fallback
    setTimeout(() => {
        button.disabled = false;
        button.innerHTML = originalContent;
    }, 5000);
}

function initializeLoadingStates() {
    // Add loading state to all action buttons
    const actionButtons = document.querySelectorAll('.btn-primary, .btn-success, .btn-danger');
    actionButtons.forEach(btn => {
        if (btn.type === 'submit') {
            btn.addEventListener('click', function() {
                setTimeout(() => showLoadingState(this), 100);
            });
        }
    });
}

// Tooltip System
function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add custom tooltips for balance indicators
    const balanceAmounts = document.querySelectorAll('.balance-amount .badge');
    balanceAmounts.forEach(badge => {
        const amount = badge.textContent.trim();
        let tooltipText = '';
        
        if (badge.classList.contains('bg-success')) {
            tooltipText = `Should receive ${amount} from others`;
        } else if (badge.classList.contains('bg-danger')) {
            tooltipText = `Owes ${amount} to others`;
        } else {
            tooltipText = 'All settled - no money owed';
        }
        
        badge.setAttribute('data-bs-toggle', 'tooltip');
        badge.setAttribute('title', tooltipText);
        new bootstrap.Tooltip(badge);
    });
}

// Smooth Scrolling
function initializeSmoothScrolling() {
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
}

// Enhanced Button Interactions
function addButtonRippleEffect() {
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Card Hover Effects
function initializeCardEffects() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
}

// Progress Bar Animations
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = '0%';
                setTimeout(() => {
                    progressBar.style.transition = 'width 1.5s cubic-bezier(0.4, 0, 0.2, 1)';
                    progressBar.style.width = width;
                }, 200);
                observer.unobserve(progressBar);
            }
        });
    });
    
    progressBars.forEach(bar => observer.observe(bar));
}

// Toast Notifications
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('#toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${getToastIcon(type)} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Initialize and show toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 4000 });
    toast.show();
    
    // Remove element after hiding
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle',
        'primary': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showToast('An unexpected error occurred. Please refresh the page.', 'danger');
});

// Initialize enhanced interactions after DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    addButtonRippleEffect();
    initializeCardEffects();
    animateProgressBars();
});

// Export functions for use in other scripts
window.SplitApp = {
    showToast,
    showLoadingState,
    formatCurrency,
    debounce
};
