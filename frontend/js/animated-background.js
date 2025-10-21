/**
 * ResearchIQ - Animated Particle Background (Figma Design)
 * Pure vanilla JS implementation of the Figma animated background
 */

class AnimatedBackground {
    constructor(container, isDark = false) {
        this.container = container;
        this.isDark = isDark;
        this.particles = [];
        this.mouse = { x: 0, y: 0 };
        this.smoothMouse = { x: 0, y: 0 };

        this.init();
    }

    init() {
        // Create background structure
        this.container.innerHTML = `
            <div class="absolute inset-0 overflow-hidden pointer-events-none">
                <!-- Gradient Background -->
                <div id="gradient-bg" class="absolute inset-0 transition-colors duration-500"></div>

                <!-- Particle Canvas -->
                <canvas id="particles-canvas" class="absolute inset-0 w-full h-full"></canvas>

                <!-- Center Icon -->
                <div class="absolute inset-0 flex items-center justify-center">
                    <div id="center-icon" class="relative"></div>
                </div>

                <!-- Gradient Overlay -->
                <div id="gradient-overlay" class="absolute inset-0 transition-colors duration-500"></div>
            </div>
        `;

        this.canvas = document.getElementById('particles-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.gradientBg = document.getElementById('gradient-bg');
        this.gradientOverlay = document.getElementById('gradient-overlay');
        this.centerIcon = document.getElementById('center-icon');

        this.resize();
        this.createParticles();
        this.createCenterIcon();
        this.setupEventListeners();
        this.updateTheme();
        this.animate();
    }

    resize() {
        this.canvas.width = this.container.offsetWidth;
        this.canvas.height = this.container.offsetHeight;
    }

    createParticles() {
        const particleCount = 40;
        this.particles = [];

        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                startX: Math.random() * this.canvas.width,
                startY: Math.random() * this.canvas.height,
                centerX: this.canvas.width / 2,
                centerY: this.canvas.height / 2,
                radius: 1.5 + Math.random() * 2,
                delay: Math.random() * 5000,
                duration: 6000 + Math.random() * 4000,
                startTime: Date.now() + Math.random() * 5000,
                opacity: 0
            });
        }
    }

    createCenterIcon() {
        this.centerIcon.innerHTML = `
            <svg width="160" height="160" viewBox="0 0 120 120" fill="none" class="animate-pulse-slow">
                <rect x="30" y="20" width="60" height="80" rx="4"
                    stroke="${this.isDark ? '#00D9C0' : '#0A1F44'}"
                    stroke-width="2.5" fill="none"/>
                <line x1="40" y1="35" x2="80" y2="35"
                    stroke="#00D9C0" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>
                <line x1="40" y1="47" x2="80" y2="47"
                    stroke="#00D9C0" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>
                <line x1="40" y1="59" x2="80" y2="59"
                    stroke="#00D9C0" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>
                <line x1="40" y1="71" x2="80" y2="71"
                    stroke="#00D9C0" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>
                <path d="M 45 85 L 52 92 L 70 74"
                    stroke="#00D9C0" stroke-width="3.5" stroke-linecap="round"
                    stroke-linejoin="round" fill="none" opacity="0.8"/>
            </svg>
        `;
    }

    setupEventListeners() {
        window.addEventListener('resize', () => this.resize());
        this.container.addEventListener('mousemove', (e) => {
            const rect = this.container.getBoundingClientRect();
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
        });
    }

    updateTheme() {
        if (this.isDark) {
            this.gradientBg.className = 'absolute inset-0 transition-colors duration-500 bg-gradient-to-br from-[#0A1F44] via-[#1a2f54] to-[#0A1F44]';
            this.gradientOverlay.className = 'absolute inset-0 transition-colors duration-500 bg-gradient-to-t from-[#0A1F44] via-transparent to-transparent';
        } else {
            this.gradientBg.className = 'absolute inset-0 transition-colors duration-500 bg-gradient-to-br from-[#FAFBFC] via-[#F0F4F8] to-[#FAFBFC]';
            this.gradientOverlay.className = 'absolute inset-0 transition-colors duration-500 bg-gradient-to-t from-[#FAFBFC] via-transparent to-transparent';
        }
    }

    animate() {
        // Smooth mouse movement
        this.smoothMouse.x += (this.mouse.x - this.smoothMouse.x) * 0.05;
        this.smoothMouse.y += (this.mouse.y - this.smoothMouse.y) * 0.05;

        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        const now = Date.now();

        // Update and draw particles
        this.particles.forEach((particle, i) => {
            const elapsed = now - particle.startTime;
            const progress = (elapsed % particle.duration) / particle.duration;

            // Animate from center to position and back
            if (progress < 0.5) {
                const t = progress * 2; // 0 to 1
                particle.x = particle.centerX + (particle.startX - particle.centerX) * this.easeInOut(t);
                particle.y = particle.centerY + (particle.startY - particle.centerY) * this.easeInOut(t);
                particle.opacity = Math.sin(t * Math.PI);
            } else {
                const t = (progress - 0.5) * 2; // 0 to 1
                particle.x = particle.startX + (particle.centerX - particle.startX) * this.easeInOut(t);
                particle.y = particle.startY + (particle.centerY - particle.startY) * this.easeInOut(t);
                particle.opacity = Math.sin((1 - t) * Math.PI);
            }

            // Draw particle with gradient
            const gradient = this.ctx.createRadialGradient(
                particle.x, particle.y, 0,
                particle.x, particle.y, particle.radius * 3
            );
            gradient.addColorStop(0, `rgba(0, 217, 192, ${particle.opacity * (this.isDark ? 1 : 0.9)})`);
            gradient.addColorStop(1, `rgba(74, 144, 226, ${particle.opacity * 0.3})`);

            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fill();

            // Draw connection lines
            if (i < 25) {
                const nextParticle = this.particles[(i + 1) % 25];
                if (particle.opacity > 0.3 && nextParticle.opacity > 0.3) {
                    const avgOpacity = (particle.opacity + nextParticle.opacity) / 2;
                    this.ctx.strokeStyle = `rgba(0, 217, 192, ${avgOpacity * 0.3})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(nextParticle.x, nextParticle.y);
                    this.ctx.stroke();
                }
            }
        });

        requestAnimationFrame(() => this.animate());
    }

    easeInOut(t) {
        return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    }

    setTheme(isDark) {
        this.isDark = isDark;
        this.updateTheme();
        this.createCenterIcon();
    }
}

// Export for use
window.AnimatedBackground = AnimatedBackground;
