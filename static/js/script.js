/**
 * Script principal pour l'application romantique Oumaima
 * Gère les animations, interactions et effets visuels
 */

// ==================== UTILITAIRES ====================

/**
 * Crée des confettis animés
 */
function createConfetti() {
    const canvas = document.createElement('canvas');
    canvas.id = 'confetti-canvas';
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '9999';
    canvas.style.pointerEvents = 'none';
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    const particles = [];

    // Créer les particules
    for (let i = 0; i < 100; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: -10,
            vx: (Math.random() - 0.5) * 8,
            vy: Math.random() * 5 + 3,
            angle: Math.random() * Math.PI * 2,
            size: Math.random() * 8 + 4,
            color: [
                '#FF6B9D',
                '#FF8FA3',
                '#FFABAF',
                '#FFB3C1',
                '#FFC3D0',
            ][Math.floor(Math.random() * 5)],
            life: 1,
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            p.y += p.vy;
            p.x += p.vx;
            p.life -= 0.01;
            p.vy += 0.1;

            ctx.save();
            ctx.globalAlpha = p.life;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        });

        if (particles.some(p => p.life > 0)) {
            requestAnimationFrame(animate);
        } else {
            canvas.remove();
        }
    }

    animate();
}

/**
 * Ajoute des cœurs flottants au clic
 */
function addClickHearts() {
    document.addEventListener('click', function(e) {
        // Ne pas déclencher sur les boutons
        if (e.target.closest('.btn')) return;

        const heart = document.createElement('div');
        heart.className = 'heart click-heart';
        heart.innerHTML = '❤️';
        heart.style.left = e.clientX + 'px';
        heart.style.top = e.clientY + 'px';

        const container = document.querySelector('.hearts-container');
        if (container) {
            container.appendChild(heart);
        }

        setTimeout(() => heart.remove(), 1000);
    });
}

/**
 * Ajoute des animations de parallaxe aux éléments
 */
function addParallaxEffect() {
    document.addEventListener('mousemove', function(e) {
        const cards = document.querySelectorAll('.question-card, .final-question-container');
        cards.forEach(card => {
            const x = (e.clientX - window.innerWidth / 2) / 50;
            const y = (e.clientY - window.innerHeight / 2) / 50;
            card.style.transform = `perspective(1000px) rotateX(${y}deg) rotateY(${x}deg)`;
        });
    });
}

/**
 * Ajoute des sons subtils (optionnel)
 */
function playSound(type) {
    // Créer un son avec Web Audio API
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();

    oscillator.connect(gain);
    gain.connect(audioContext.destination);

    gain.gain.setValueAtTime(0.3, audioContext.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

    switch (type) {
        case 'click':
            oscillator.frequency.value = 880;
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.1);
            break;
        case 'success':
            oscillator.frequency.setValueAtTime(523, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(659, audioContext.currentTime + 0.1);
            oscillator.frequency.setValueAtTime(784, audioContext.currentTime + 0.2);
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.3);
            break;
        case 'hover':
            oscillator.frequency.value = 440;
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.05);
            break;
    }
}

/**
 * Ajoute un debounce pour les événements
 */
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

// ==================== GESTION DES ANIMATIONS DE TEXTE ====================

/**
 * Anime les textes de la page d'accueil
 */
function animateHomeTexts() {
    const texts = document.querySelectorAll('.fade-in-text');
    texts.forEach((text, index) => {
        text.style.animationDelay = index * 0.8 + 's';
    });
}

/**
 * Anime les textes de la page success
 */
function animateSuccessTexts() {
    const texts = document.querySelectorAll('.success-text');
    texts.forEach((text, index) => {
        text.style.animationDelay = index * 0.8 + 's';
    });
}

/**
 * Anime les textes de la question finale
 */
function animateFinalTexts() {
    const texts = document.querySelectorAll('.fade-in-text');
    texts.forEach((text, index) => {
        text.style.animationDelay = index * 0.7 + 's';
    });
}

// ==================== GESTION DES QUESTIONS ====================

/**
 * Gère la sélection de réponses pour les questions
 */
function handleQuestionAnswers() {
    const answerOptions = document.querySelectorAll('.answer-option');
    let selectedAnswer = null;

    answerOptions.forEach(option => {
        option.addEventListener('change', function() {
            answerOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            selectedAnswer = this.querySelector('input').value;

            // Jouer un son (optionnel)
            try {
                playSound('click');
            } catch (e) {
                // Les sons ne sont pas toujours disponibles
            }
        });

        // Ajouter un effet au survol
        option.addEventListener('mouseenter', function() {
            if (!this.classList.contains('selected')) {
                this.style.transform = 'scale(1.02)';
            }
        });

        option.addEventListener('mouseleave', function() {
            if (!this.classList.contains('selected')) {
                this.style.transform = 'scale(1)';
            }
        });
    });

    const form = document.getElementById('questionForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            if (!selectedAnswer) {
                alert('Veuillez sélectionner une réponse');
                return;
            }

            // Ajouter l'animation de sortie
            const card = document.querySelector('.question-card');
            card.classList.add('slide-out');

            // Soumettre après l'animation
            setTimeout(() => {
                form.submit();
            }, 300);
        });
    }
}

/**
 * Gère la sélection pour la question finale
 */
function handleFinalAnswer() {
    const form = document.getElementById('finalForm');
    const answerOptions = document.querySelectorAll('.final-answer-option');

    answerOptions.forEach(option => {
        option.addEventListener('change', function() {
            answerOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');

            try {
                playSound('success');
            } catch (e) {
                // Les sons ne sont pas toujours disponibles
            }
        });

        option.addEventListener('mouseenter', function() {
            if (!this.classList.contains('selected')) {
                this.style.transform = 'scale(1.05)';
            }
        });

        option.addEventListener('mouseleave', function() {
            if (!this.classList.contains('selected')) {
                this.style.transform = 'scale(1)';
            }
        });
    });

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const selectedAnswer = form.querySelector('input[name="answer"]:checked');
            if (!selectedAnswer) {
                return;
            }

            // Déclencher les confettis
            createConfetti();

            // Soumettre après un délai
            setTimeout(() => {
                form.submit();
            }, 1000);
        });
    }
}

// ==================== GESTION DE LA PAGE SUCCESS ====================

/**
 * Lance les confettis sur la page success
 */
function launchConfetti() {
    const canvas = document.getElementById('confetti');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];

    // Créer les particules de confettis
    for (let i = 0; i < 150; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: -10,
            vx: (Math.random() - 0.5) * 10,
            vy: Math.random() * 6 + 4,
            angle: Math.random() * Math.PI * 2,
            size: Math.random() * 10 + 5,
            color: [
                '#FF1493',
                '#FF69B4',
                '#FFB6C1',
                '#FFC0CB',
                '#FF6B9D',
                '#E91E63',
            ][Math.floor(Math.random() * 6)],
            life: 1,
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            p.y += p.vy;
            p.x += p.vx;
            p.vy += 0.15;
            p.angle += 0.05;
            p.life -= 0.008;

            ctx.save();
            ctx.globalAlpha = p.life;
            ctx.translate(p.x, p.y);
            ctx.rotate(p.angle);
            ctx.fillStyle = p.color;

            // Dessiner un carré (confetti)
            ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);

            ctx.restore();
        });

        if (particles.some(p => p.life > 0)) {
            requestAnimationFrame(animate);
        }
    }

    animate();
}

/**
 * Ajoute des cœurs animés au clic sur la page success
 */
function addSuccessClickHearts() {
    document.addEventListener('click', function(e) {
        if (e.target.closest('.btn')) return;

        const heart = document.createElement('span');
        heart.innerHTML = ['❤️', '💕', '💖', '🥰'][Math.floor(Math.random() * 4)];
        heart.style.position = 'fixed';
        heart.style.left = e.clientX + 'px';
        heart.style.top = e.clientY + 'px';
        heart.style.fontSize = '2em';
        heart.style.zIndex = '9999';
        heart.style.pointerEvents = 'none';
        heart.style.animation = 'floatingHeart 1.5s ease-out forwards';

        document.body.appendChild(heart);

        setTimeout(() => heart.remove(), 1500);
    });
}

// ==================== GESTION DE LA RÉACTIVITÉ ====================

/**
 * Ajuste les dimensions du canvas lors du redimensionnement
 */
function handleWindowResize() {
    const canvas = document.getElementById('confetti');
    if (canvas) {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    const confettiCanvas = document.getElementById('confetti-canvas');
    if (confettiCanvas) {
        confettiCanvas.width = window.innerWidth;
        confettiCanvas.height = window.innerHeight;
    }
}

// ==================== INITIALISATION ====================

document.addEventListener('DOMContentLoaded', function() {
    // Vérifier quelle page est active
    const body = document.body;

    // Animer les textes selon la page
    if (document.querySelector('.home-content')) {
        animateHomeTexts();
        addClickHearts();
    }

    if (document.querySelector('.question-card')) {
        handleQuestionAnswers();
    }

    if (document.querySelector('.final-question-container')) {
        animateFinalTexts();
        handleFinalAnswer();
    }

    if (document.querySelector('.success-content')) {
        animateSuccessTexts();
        launchConfetti();
        addSuccessClickHearts();
    }

    // Ajouter un parallaxe subtil
    // addParallaxEffect(); // Décommenter si souhaité

    // Gérer le redimensionnement
    window.addEventListener('resize', debounce(handleWindowResize, 250));

    // Ajouter des effets de survol aux boutons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            try {
                playSound('hover');
            } catch (e) {
                // Les sons ne sont pas toujours disponibles
            }
        });
    });

    // Précharger les images (si nécessaire)
    preloadImages();
});

/**
 * Précharge les images
 */
function preloadImages() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        const preload = new Image();
        preload.src = img.src;
    });
}

// Exporter les fonctions pour les templates
window.createConfetti = createConfetti;
window.playSound = playSound;
window.launchConfetti = launchConfetti;
