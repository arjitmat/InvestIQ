import { Moon, Sun } from 'lucide-react';
import { motion } from 'motion/react';

interface ThemeToggleProps {
  isDark: boolean;
  setIsDark: (isDark: boolean) => void;
}

export function ThemeToggle({ isDark, setIsDark }: ThemeToggleProps) {
  return (
    <motion.button
      onClick={() => setIsDark(!isDark)}
      className={`fixed top-6 right-6 z-50 p-3 rounded-full transition-all duration-300 ${
        isDark 
          ? 'bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/20' 
          : 'bg-[#0A1F44]/10 hover:bg-[#0A1F44]/20 backdrop-blur-sm border border-[#0A1F44]/20'
      }`}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      aria-label="Toggle theme"
    >
      <motion.div
        initial={false}
        animate={{ rotate: isDark ? 180 : 0 }}
        transition={{ duration: 0.3 }}
      >
        {isDark ? (
          <Sun className="w-6 h-6 text-[#00D9C0]" />
        ) : (
          <Moon className="w-6 h-6 text-[#0A1F44]" />
        )}
      </motion.div>
    </motion.button>
  );
}
