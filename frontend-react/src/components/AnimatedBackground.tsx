import { motion, useMotionValue, useSpring } from 'motion/react';
import { useEffect, useState } from 'react';

interface Particle {
  id: number;
  startX: number;
  startY: number;
  delay: number;
  duration: number;
  scale: number;
}

interface AnimatedBackgroundProps {
  isDark: boolean;
}

export function AnimatedBackground({ isDark }: AnimatedBackgroundProps) {
  const [particles, setParticles] = useState<Particle[]>([]);
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  
  const springConfig = { damping: 40, stiffness: 50 };
  const smoothMouseX = useSpring(mouseX, springConfig);
  const smoothMouseY = useSpring(mouseY, springConfig);

  useEffect(() => {
    // Generate particles
    const newParticles: Particle[] = Array.from({ length: 40 }, (_, i) => ({
      id: i,
      startX: Math.random() * 100,
      startY: Math.random() * 100,
      delay: Math.random() * 5,
      duration: 6 + Math.random() * 4,
      scale: 0.5 + Math.random() * 0.8,
    }));
    setParticles(newParticles);
  }, []);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      // Reduce the movement range for subtlety
      const x = ((e.clientX / window.innerWidth) - 0.5) * 30;
      const y = ((e.clientY / window.innerHeight) - 0.5) * 30;
      mouseX.set(x);
      mouseY.set(y);
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [mouseX, mouseY]);

  return (
    <div className="absolute inset-0 overflow-hidden">
      {/* Gradient Background */}
      <div className={`absolute inset-0 transition-colors duration-500 ${
        isDark 
          ? 'bg-gradient-to-br from-[#0A1F44] via-[#1a2f54] to-[#0A1F44]' 
          : 'bg-gradient-to-br from-[#FAFBFC] via-[#F0F4F8] to-[#FAFBFC]'
      }`}></div>
      
      {/* Floating Particles */}
      <svg className="absolute inset-0 w-full h-full" style={{ opacity: isDark ? 0.7 : 0.6 }}>
        <defs>
          {/* Gradient for particles */}
          <linearGradient id="particleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00D9C0" stopOpacity={isDark ? "1" : "0.9"} />
            <stop offset="100%" stopColor={isDark ? "#4A90E2" : "#0A1F44"} stopOpacity="0.8" />
          </linearGradient>
          
          {/* Enhanced Glow filter */}
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        {particles.map((particle) => (
          <motion.circle
            key={particle.id}
            r={3 * particle.scale}
            fill="url(#particleGradient)"
            filter="url(#glow)"
            initial={{
              cx: `${particle.startX}%`,
              cy: `${particle.startY}%`,
            }}
            animate={{
              cx: ['50%', `${particle.startX}%`, '50%'],
              cy: ['50%', `${particle.startY}%`, '50%'],
              opacity: [0, 1, 0],
              scale: [0.5, 1, 0.5],
            }}
            transition={{
              duration: particle.duration,
              delay: particle.delay,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          />
        ))}

        {/* Connection Lines - More visible */}
        {particles.slice(0, 25).map((particle, index) => {
          const nextParticle = particles[(index + 1) % 25];
          return (
            <motion.line
              key={`line-${particle.id}`}
              stroke="url(#particleGradient)"
              strokeWidth="1"
              initial={{
                x1: `${particle.startX}%`,
                y1: `${particle.startY}%`,
                x2: `${nextParticle.startX}%`,
                y2: `${nextParticle.startY}%`,
              }}
              animate={{
                x1: ['50%', `${particle.startX}%`, '50%'],
                y1: ['50%', `${particle.startY}%`, '50%'],
                x2: ['50%', `${nextParticle.startX}%`, '50%'],
                y2: ['50%', `${nextParticle.startY}%`, '50%'],
                opacity: [0, 0.5, 0],
              }}
              transition={{
                duration: particle.duration,
                delay: particle.delay,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            />
          );
        })}
      </svg>

      {/* Center Report Icon (Convergence Point) - Subtle Cursor Interactive */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <motion.div
          style={{
            x: smoothMouseX,
            y: smoothMouseY,
          }}
          animate={{ 
            scale: [1, 1.05, 1],
            rotate: [0, 2, -2, 0],
          }}
          transition={{
            duration: 6,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <svg width="160" height="160" viewBox="0 0 120 120" fill="none">
            {/* Document/Report Icon */}
            <motion.rect
              x="30"
              y="20"
              width="60"
              height="80"
              rx="4"
              stroke={isDark ? "#00D9C0" : "#0A1F44"}
              strokeWidth="2.5"
              fill="none"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            />
            
            {/* Document Lines */}
            {[0, 1, 2, 3].map((i) => (
              <motion.line
                key={i}
                x1="40"
                y1={35 + i * 12}
                x2="80"
                y2={35 + i * 12}
                stroke="#00D9C0"
                strokeWidth="2.5"
                strokeLinecap="round"
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 0.8 }}
                transition={{
                  duration: 2,
                  delay: i * 0.2,
                  repeat: Infinity,
                  repeatDelay: 2,
                  ease: 'easeInOut',
                }}
              />
            ))}
            
            {/* Checkmark */}
            <motion.path
              d="M 45 85 L 52 92 L 70 74"
              stroke="#00D9C0"
              strokeWidth="3.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="none"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{
                duration: 1,
                delay: 2,
                repeat: Infinity,
                repeatDelay: 4,
                ease: 'easeOut',
              }}
            />
          </svg>
        </motion.div>
      </div>

      {/* Subtle Cursor Glow */}
      <motion.div
        className="absolute pointer-events-none w-full h-full flex items-center justify-center"
      >
        <motion.div
          style={{
            x: smoothMouseX,
            y: smoothMouseY,
          }}
          className={`w-24 h-24 rounded-full ${
            isDark 
              ? 'bg-gradient-radial from-[#00D9C0]/10 via-[#00D9C0]/5 to-transparent' 
              : 'bg-gradient-radial from-[#00D9C0]/8 via-[#00D9C0]/3 to-transparent'
          }`}
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      </motion.div>

      {/* Subtle Gradient Overlay */}
      <div className={`absolute inset-0 pointer-events-none transition-colors duration-500 ${
        isDark 
          ? 'bg-gradient-to-t from-[#0A1F44] via-transparent to-transparent' 
          : 'bg-gradient-to-t from-[#FAFBFC] via-transparent to-transparent'
      }`}></div>
    </div>
  );
}
