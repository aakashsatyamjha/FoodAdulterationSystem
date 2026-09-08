import React, { useEffect, useState } from 'react';
import { ShieldCheck } from 'lucide-react';

export default function SplashAnimation({ onComplete }) {
  const [stage, setStage] = useState(0); // 0: init, 1: glow+logo, 2: scan, 3: text, 4: exit

  useEffect(() => {
    // Stage 1: Logo scales in + soft glow
    const t1 = setTimeout(() => setStage(1), 60);

    // Stage 2: Laser scan beam sweeps through
    const t2 = setTimeout(() => setStage(2), 400);

    // Stage 3: Brand typography fades in
    const t3 = setTimeout(() => setStage(3), 700);

    // Stage 4: Smooth exit fade
    const t4 = setTimeout(() => setStage(4), 1250);

    // Stage 5: Complete
    const t5 = setTimeout(() => {
      if (onComplete) onComplete();
    }, 1450);

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
      clearTimeout(t4);
      clearTimeout(t5);
    };
  }, [onComplete]);

  return (
    <div className={`
      fixed inset-0 z-[99999] w-screen h-screen flex flex-col items-center justify-center bg-[#070b14] text-white
      transition-all duration-300 ease-out select-none
      ${stage === 4 ? 'opacity-0 pointer-events-none scale-105' : 'opacity-100 pointer-events-auto scale-100'}
    `}>
      
      {/* Background Radial Glow */}
      <div className={`
        absolute w-96 h-96 rounded-full bg-emerald-500/20 blur-3xl pointer-events-none transition-all duration-700
        ${stage >= 1 ? 'opacity-100 scale-100' : 'opacity-0 scale-75'}
      `} />
      
      <div className="relative z-10 flex flex-col items-center justify-center space-y-6">
        
        {/* Shield Logo with Glass Box & Laser Sweep */}
        <div className={`
          relative w-20 h-20 rounded-2xl bg-gradient-to-br from-emerald-400/20 to-teal-500/10 border border-emerald-500/40
          flex items-center justify-center shadow-2xl shadow-emerald-500/30 overflow-hidden
          transition-all duration-500 transform
          ${stage >= 1 ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-90 translate-y-4'}
        `}>
          
          {/* Central Shield Icon */}
          <ShieldCheck className="w-11 h-11 text-emerald-400 stroke-[2.2] relative z-10 drop-shadow-[0_0_12px_rgba(16,185,129,0.6)]" />

          {/* Laser Scanning Beam Sweep */}
          <div className={`
            absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-cyan-300 to-transparent
            shadow-[0_0_15px_#06b6d4] transition-all duration-700 ease-in-out
            ${stage >= 2 ? 'top-full opacity-100' : 'top-0 opacity-0'}
          `} />

          {/* Ambient Inner Pulse */}
          <div className="absolute inset-0 bg-emerald-400/10 animate-pulse pointer-events-none" />
        </div>

        {/* Brand Name & Subtitle Typography */}
        <div className={`
          text-center space-y-1.5 transition-all duration-500 transform
          ${stage >= 3 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-3'}
        `}>
          <div className="flex items-center justify-center gap-2">
            <span className="text-3xl font-extrabold tracking-tight text-white drop-shadow-sm">
              FoodGuard
            </span>
            <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              AI
            </span>
          </div>

          <p className="text-xs font-medium text-slate-400 tracking-widest uppercase">
            AI Food Safety Platform
          </p>
        </div>

        {/* Status indicator bar */}
        <div className={`
          w-32 h-1 rounded-full bg-slate-800 overflow-hidden transition-opacity duration-300
          ${stage >= 2 ? 'opacity-100' : 'opacity-0'}
        `}>
          <div className="h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-400 rounded-full animate-[shimmer_1s_infinite] w-full" />
        </div>

      </div>

    </div>
  );
}
