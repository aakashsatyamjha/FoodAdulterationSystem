import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Barcode, 
  FileText, 
  Sparkles, 
  ArrowRight, 
  CheckCircle2, 
  AlertTriangle, 
  ShieldAlert, 
  Scale, 
  Cpu, 
  Database, 
  Camera, 
  Activity, 
  BookOpen, 
  ChevronRight, 
  Sun, 
  Moon, 
  Laptop, 
  Menu, 
  X, 
  ScanLine, 
  Layers, 
  Award,
  Check,
  Zap,
  Info
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useAuth } from '../context/AuthContext';

export default function LandingPage({ 
  onGetStarted, 
  onSignIn, 
  onOpenDashboard 
}) {
  const { theme, resolvedTheme, setTheme } = useTheme();
  const { isAuthenticated, user } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const scrollToSection = (id) => {
    setMobileMenuOpen(false);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handlePrimaryAction = () => {
    if (isAuthenticated) {
      onOpenDashboard();
    } else {
      onGetStarted();
    }
  };

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 font-sans selection:bg-emerald-500 selection:text-slate-950 transition-colors">
      
      {/* ── 1. Top Glass Navbar ── */}
      <header className="sticky top-0 z-50 glass-panel border-b border-white/10 px-4 sm:px-6 lg:px-12 h-16 sm:h-20 flex items-center justify-between transition-all backdrop-blur-md">
        
        {/* Brand Logo */}
        <div 
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-emerald-400/20 to-teal-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 group-hover:scale-105 transition-transform shadow-xs">
            <ShieldCheck className="w-5 h-5 sm:w-6 sm:h-6 stroke-[2.2]" />
          </div>
          <div className="flex flex-col">
            <span className="text-base sm:text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
              FoodGuard <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">AI</span>
            </span>
            <span className="text-[10px] font-medium text-slate-400 -mt-0.5 hidden sm:block">
              AI Food Safety Platform
            </span>
          </div>
        </div>

        {/* Center Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-7 text-xs font-semibold text-slate-300">
          <button 
            onClick={() => scrollToSection('problem')}
            className="hover:text-emerald-400 transition-colors cursor-pointer"
          >
            Product
          </button>
          <button 
            onClick={() => scrollToSection('how-it-works')}
            className="hover:text-emerald-400 transition-colors cursor-pointer"
          >
            How It Works
          </button>
          <button 
            onClick={() => scrollToSection('features')}
            className="hover:text-emerald-400 transition-colors cursor-pointer"
          >
            Features
          </button>
          <button 
            onClick={() => scrollToSection('technology')}
            className="hover:text-emerald-400 transition-colors cursor-pointer"
          >
            Technology
          </button>
          <button 
            onClick={() => scrollToSection('about')}
            className="hover:text-emerald-400 transition-colors cursor-pointer"
          >
            About
          </button>
        </nav>

        {/* Right Actions */}
        <div className="flex items-center gap-2.5 sm:gap-4">
          
          {/* Theme Switcher Button */}
          <button
            onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
            className="p-2 rounded-xl text-slate-300 hover:text-white bg-white/5 hover:bg-white/10 border border-white/10 transition-colors cursor-pointer"
            title={`Switch to ${resolvedTheme === 'dark' ? 'Light' : 'Dark'} mode`}
          >
            {resolvedTheme === 'dark' ? (
              <Sun className="w-4 h-4 text-amber-400" />
            ) : (
              <Moon className="w-4 h-4 text-cyan-400" />
            )}
          </button>

          {/* Authentication Action Buttons */}
          {isAuthenticated ? (
            <button
              onClick={onOpenDashboard}
              className="flex items-center gap-2 px-4 py-2 sm:py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs sm:text-sm transition-all shadow-md shadow-emerald-500/20 cursor-pointer"
            >
              <span>Open Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <>
              <button
                onClick={onSignIn}
                className="hidden sm:block px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-white/5 transition-colors cursor-pointer"
              >
                Sign In
              </button>

              <button
                onClick={onGetStarted}
                className="flex items-center gap-1.5 px-4 py-2 sm:py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs sm:text-sm transition-all shadow-md shadow-emerald-500/20 cursor-pointer"
              >
                <span>Get Started</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </>
          )}

          {/* Mobile menu hamburger */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-xl text-slate-300 hover:text-white md:hidden cursor-pointer"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>

        </div>

      </header>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="fixed inset-x-0 top-16 z-40 glass-panel border-b border-white/10 p-6 space-y-4 md:hidden shadow-2xl bg-[#070b14]/95 backdrop-blur-xl">
          <nav className="flex flex-col space-y-3 text-sm font-semibold text-slate-300">
            <button 
              onClick={() => scrollToSection('problem')}
              className="text-left py-2 hover:text-emerald-400"
            >
              Product
            </button>
            <button 
              onClick={() => scrollToSection('how-it-works')}
              className="text-left py-2 hover:text-emerald-400"
            >
              How It Works
            </button>
            <button 
              onClick={() => scrollToSection('features')}
              className="text-left py-2 hover:text-emerald-400"
            >
              Features
            </button>
            <button 
              onClick={() => scrollToSection('technology')}
              className="text-left py-2 hover:text-emerald-400"
            >
              Technology
            </button>
            <button 
              onClick={() => scrollToSection('about')}
              className="text-left py-2 hover:text-emerald-400"
            >
              About
            </button>
          </nav>

          <div className="pt-4 border-t border-white/10 flex flex-col gap-2">
            {!isAuthenticated && (
              <button
                onClick={onSignIn}
                className="w-full py-2.5 rounded-xl border border-white/10 text-white font-semibold text-xs text-center"
              >
                Sign In
              </button>
            )}
            <button
              onClick={handlePrimaryAction}
              className="w-full py-2.5 rounded-xl bg-emerald-500 text-slate-950 font-bold text-xs text-center shadow-md shadow-emerald-500/20"
            >
              {isAuthenticated ? 'Open Dashboard' : 'Get Started — It\'s Free'}
            </button>
          </div>
        </div>
      )}

      {/* ── 2. Hero Section ── */}
      <section className="relative pt-12 pb-20 sm:pt-20 sm:pb-28 px-4 sm:px-6 lg:px-12 max-w-7xl mx-auto overflow-hidden">
        
        {/* Ambient background glow orbs */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[500px] bg-gradient-to-tr from-emerald-500/10 via-teal-500/5 to-transparent rounded-full blur-3xl pointer-events-none" />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center relative z-10">
          
          {/* Left Column (7 cols): Main Headline & CTAs */}
          <div className="lg:col-span-7 space-y-6 sm:space-y-8 text-center lg:text-left">
            
            {/* Pill Badge */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 text-xs font-bold tracking-wide uppercase">
              <Sparkles className="w-3.5 h-3.5" />
              <span>AI-Powered Food Safety Platform</span>
            </div>

            {/* Headline */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight text-white leading-[1.1]">
              Know What's <br />
              <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
                Inside Your Food.
              </span>
            </h1>

            {/* Supporting Subtitle */}
            <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto lg:mx-0 leading-relaxed font-normal">
              Scan packaged food, analyze ingredients, and understand potential health and safety risks with intelligent AI-powered multi-model screening.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
              <button
                onClick={handlePrimaryAction}
                className="w-full sm:w-auto flex items-center justify-center gap-2.5 px-7 py-3.5 rounded-2xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-sm sm:text-base transition-all shadow-xl shadow-emerald-500/25 hover:shadow-emerald-500/40 hover:-translate-y-0.5 cursor-pointer"
              >
                <Barcode className="w-5 h-5 stroke-[2.2]" />
                <span>Scan a Product</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <button
                onClick={() => scrollToSection('features')}
                className="w-full sm:w-auto flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl glass-panel hover:bg-white/10 text-white font-bold text-sm sm:text-base border border-white/10 transition-all cursor-pointer"
              >
                <span>Explore FoodGuard</span>
                <ChevronRight className="w-4 h-4 text-slate-400" />
              </button>
            </div>

            {/* Trust Indicators Strip */}
            <div className="pt-4 border-t border-white/10 flex flex-wrap items-center justify-center lg:justify-start gap-x-6 gap-y-2 text-xs font-semibold text-slate-400">
              <div className="flex items-center gap-1.5">
                <Check className="w-4 h-4 text-emerald-400" />
                <span>Ingredient Analysis</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Check className="w-4 h-4 text-emerald-400" />
                <span>Barcode Scanning</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Check className="w-4 h-4 text-emerald-400" />
                <span>OCR Detection</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Check className="w-4 h-4 text-emerald-400" />
                <span>Food Safety Insights</span>
              </div>
            </div>

          </div>

          {/* Right Column (5 cols): Floating Glass Product Inspection Preview */}
          <div className="lg:col-span-5 flex justify-center">
            <div className="relative w-full max-w-md rounded-3xl glass-panel p-6 border border-white/15 shadow-2xl shadow-emerald-950/50 space-y-5 overflow-hidden">
              
              {/* Subtle Laser Scan Line Animation */}
              <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_15px_#10b981] animate-[pulse_3s_infinite] top-1/4 opacity-40 pointer-events-none" />

              {/* Product Header */}
              <div className="flex items-center justify-between pb-3 border-b border-white/10">
                <div className="flex items-center gap-3">
                  <img
                    src="https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=120&auto=format&fit=crop&q=60"
                    alt="Inspected Product"
                    className="w-12 h-12 rounded-xl object-cover border border-white/10 bg-slate-900 shrink-0"
                  />
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">
                      Dairy Category
                    </span>
                    <h3 className="font-bold text-sm text-white mt-1">
                      Amul Pure Cow Ghee
                    </h3>
                  </div>
                </div>

                <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  Verified Clean
                </span>
              </div>

              {/* Quality Score Meter */}
              <div className="p-4 rounded-2xl bg-white/5 border border-white/5 flex items-center justify-between">
                <div>
                  <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider block">
                    Food Safety Score
                  </span>
                  <div className="text-2xl font-black text-white mt-0.5 flex items-baseline gap-1">
                    <span>98</span>
                    <span className="text-xs font-normal text-slate-400">/ 100</span>
                  </div>
                  <span className="text-xs font-semibold text-emerald-400">
                    Generally Safe & Pure
                  </span>
                </div>

                <div className="w-12 h-12 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                  <ShieldCheck className="w-6 h-6" />
                </div>
              </div>

              {/* Ingredient Detection Badges */}
              <div className="space-y-2">
                <span className="text-xs font-bold text-slate-300 block">
                  Ingredient Screening Signals
                </span>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span className="truncate">100% Milk Fat</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span className="truncate">Natural Vitamin A</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-white/5 border border-white/5 text-slate-300 flex items-center gap-2">
                    <Check className="w-4 h-4 text-cyan-400 shrink-0" />
                    <span className="truncate">Zero Added Dyes</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span className="truncate">FSSAI 2.1 Compliant</span>
                  </div>
                </div>
              </div>

              {/* Mini CTA preview */}
              <button
                onClick={handlePrimaryAction}
                className="w-full py-2.5 rounded-xl bg-white/10 hover:bg-white/15 text-white font-bold text-xs transition-colors border border-white/10 flex items-center justify-center gap-2 cursor-pointer"
              >
                <span>Inspect Full Laboratory Report</span>
                <ArrowRight className="w-3.5 h-3.5 text-emerald-400" />
              </button>

            </div>
          </div>

        </div>

      </section>

      {/* ── 3. Trust Strip ── */}
      <section className="border-y border-white/10 bg-white/[0.02] py-6 px-4 sm:px-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-semibold text-slate-400">
          <span className="uppercase tracking-widest text-slate-500 font-bold text-[11px]">
            Built for smarter food decisions:
          </span>
          <div className="flex flex-wrap items-center justify-center gap-4 sm:gap-8 text-slate-300">
            <span className="flex items-center gap-1.5"><Barcode className="w-4 h-4 text-emerald-400" /> Barcode Intelligence</span>
            <span className="flex items-center gap-1.5"><Camera className="w-4 h-4 text-cyan-400" /> Ingredient OCR</span>
            <span className="flex items-center gap-1.5"><Scale className="w-4 h-4 text-purple-400" /> Nutrition Analysis</span>
            <span className="flex items-center gap-1.5"><ShieldAlert className="w-4 h-4 text-rose-400" /> Risk Detection</span>
            <span className="flex items-center gap-1.5"><BookOpen className="w-4 h-4 text-amber-400" /> FSSAI Compliance</span>
          </div>
        </div>
      </section>

      {/* ── 4. Problem Section (Editorial Style) ── */}
      <section id="problem" className="py-20 px-4 sm:px-6 lg:px-12 max-w-7xl mx-auto space-y-12">
        
        <div className="max-w-3xl space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
            The Problem With Packaged Food
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
            Food labels tell you what's inside. <br className="hidden sm:inline" />
            We help you understand what it means.
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Problem 01 */}
          <div className="glass-panel rounded-3xl p-8 space-y-4 border border-white/10 hover:border-emerald-500/30 transition-all">
            <div className="text-4xl font-black text-emerald-400/40 font-mono">
              01
            </div>
            <h3 className="text-xl font-bold text-white">
              Hidden Ingredients
            </h3>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-normal">
              Artificial preservatives, hidden trans fats, and non-permitted chemical colorants often hide behind scientific names and generic codes.
            </p>
          </div>

          {/* Problem 02 */}
          <div className="glass-panel rounded-3xl p-8 space-y-4 border border-white/10 hover:border-emerald-500/30 transition-all">
            <div className="text-4xl font-black text-cyan-400/40 font-mono">
              02
            </div>
            <h3 className="text-xl font-bold text-white">
              Complex Food Labels
            </h3>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-normal">
              Cryptic INS and E-numbers make it nearly impossible for everyday consumers and families to gauge the real nutritional and chemical safety.
            </p>
          </div>

          {/* Problem 03 */}
          <div className="glass-panel rounded-3xl p-8 space-y-4 border border-white/10 hover:border-emerald-500/30 transition-all">
            <div className="text-4xl font-black text-purple-400/40 font-mono">
              03
            </div>
            <h3 className="text-xl font-bold text-white">
              Hard-to-Understand Risks
            </h3>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-normal">
              Absence of plain-English statutory context leaves consumers unaware of whether high sugar, sodium, or preservatives violate standard limits.
            </p>
          </div>

        </div>

      </section>

      {/* ── 5. How It Works (3-Step Connected Sequence) ── */}
      <section id="how-it-works" className="py-20 px-4 sm:px-6 lg:px-12 max-w-7xl mx-auto space-y-12">
        
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
            Simple 3-Step Verification
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            How FoodGuard Works
          </h2>
          <p className="text-xs sm:text-sm text-slate-300">
            From raw barcode scanning to intelligent explainable safety verdicts in seconds.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          
          {/* Step 1 */}
          <div className="glass-panel rounded-3xl p-8 space-y-4 border border-white/10 relative">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-black text-base">
              01
            </div>
            <h3 className="text-xl font-bold text-white">
              Scan
            </h3>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-normal">
              Scan the product barcode with your camera or capture a photo of the printed ingredient label using optical character recognition.
            </p>
          </div>

          {/* Step 2 */}
          <div className="glass-panel rounded-3xl p-8 space-y-4 border border-white/10 relative">
            <div className="w-12 h-12 rounded-2xl bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-black text-base">
              02
            </div>
            <h3 className="text-xl font-bold text-white">
              Analyze
            </h3>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-normal">
              FoodGuard cross-examines ingredients against chemical adulteration knowledge bases, FSSAI regulations, and trained ML classifiers.
            </p>
          </div>

          {/* Step 3 */}
          <div className="glass-panel rounded-3xl p-8 space-y-4 border border-white/10 relative">
            <div className="w-12 h-12 rounded-2xl bg-purple-500/20 border border-purple-500/30 flex items-center justify-center text-purple-400 font-black text-base">
              03
            </div>
            <h3 className="text-xl font-bold text-white">
              Understand
            </h3>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-normal">
              Receive a clear 0–100 Safety Score, plain-English adulteration verdict, and an explainable breakdown of positive vs negative factors.
            </p>
          </div>

        </div>

      </section>

      {/* ── 6. Features Grid (6 Minimal Glass Cards) ── */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-12 max-w-7xl mx-auto space-y-12">
        
        <div className="max-w-2xl space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
            Platform Capabilities
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Everything you need to understand your food.
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          
          {/* Feature 1 */}
          <div className="glass-panel rounded-3xl p-6 space-y-3 border border-white/10 hover:border-emerald-500/30 transition-all">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/15 border border-emerald-500/25 flex items-center justify-center text-emerald-400">
              <Barcode className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-white">Barcode Scanner</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Instantly identify packaged products using live camera EAN-13 barcode scanning connected to global food registries.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="glass-panel rounded-3xl p-6 space-y-3 border border-white/10 hover:border-cyan-500/30 transition-all">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/15 border border-cyan-500/25 flex items-center justify-center text-cyan-400">
              <Camera className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-white">Ingredient OCR</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Capture ingredient packaging labels and extract formulation text with client-side WebAssembly Tesseract.js.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="glass-panel rounded-3xl p-6 space-y-3 border border-white/10 hover:border-rose-500/30 transition-all">
            <div className="w-10 h-10 rounded-xl bg-rose-500/15 border border-rose-500/25 flex items-center justify-center text-rose-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-white">AI Risk Analysis</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Identify potentially concerning additives, banned dyes (Metanil Yellow, Lead Chromate), and food-quality risks.
            </p>
          </div>

          {/* Feature 4 */}
          <div className="glass-panel rounded-3xl p-6 space-y-3 border border-white/10 hover:border-purple-500/30 transition-all">
            <div className="w-10 h-10 rounded-xl bg-purple-500/15 border border-purple-500/25 flex items-center justify-center text-purple-400">
              <Scale className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-white">Nutrition Profiling</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Understand critical nutritional values including sugar density, sodium per 100g, saturated fat, and trans-fat limits.
            </p>
          </div>

          {/* Feature 5 */}
          <div className="glass-panel rounded-3xl p-6 space-y-3 border border-white/10 hover:border-amber-500/30 transition-all">
            <div className="w-10 h-10 rounded-xl bg-amber-500/15 border border-amber-500/25 flex items-center justify-center text-amber-400">
              <BookOpen className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-white">FSSAI Compliance</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Check statutory compliance parameters under the Food Safety and Standards Act (2006) for Indian food products.
            </p>
          </div>

          {/* Feature 6 */}
          <div className="glass-panel rounded-3xl p-6 space-y-3 border border-white/10 hover:border-emerald-500/30 transition-all">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/15 border border-emerald-500/25 flex items-center justify-center text-emerald-400">
              <Database className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-white">Scan History & Audit Trail</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Track previously analyzed products with full MongoDB database persistence and timestamped records.
            </p>
          </div>

        </div>

      </section>

      {/* ── 7. Product Showcase Section ── */}
      <section id="technology" className="py-20 px-4 sm:px-6 lg:px-12 max-w-7xl mx-auto space-y-12">
        
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
            Interactive Product Showcase
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            From a barcode to a complete food safety report.
          </h2>
          <p className="text-xs sm:text-sm text-slate-300">
            A comprehensive, high-density analytics view providing transparency across chemical, nutritional, and regulatory factors.
          </p>
        </div>

        {/* Large Glass Dashboard Mockup Preview */}
        <div className="relative rounded-3xl glass-panel p-6 sm:p-10 border border-white/15 shadow-2xl overflow-hidden">
          
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            
            {/* Score & Gauge Column */}
            <div className="lg:col-span-5 space-y-6">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-emerald-400 bg-emerald-500/15 px-3 py-1 rounded-full border border-emerald-500/30">
                  Live Audit Result
                </span>
                <span className="text-xs text-slate-400">Maggi 2-Minute Masala Noodles</span>
              </div>

              <div className="space-y-2">
                <div className="text-5xl font-black text-white tracking-tight">
                  64 <span className="text-lg font-normal text-slate-400">/ 100</span>
                </div>
                <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/15 text-amber-400 border border-amber-500/30">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>Moderate Nutritional Risk</span>
                </div>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">
                FSSAI compliant for commercial sale, but flags moderate sodium (860mg) and flavor enhancers (INS 635).
              </p>

              <button
                onClick={handlePrimaryAction}
                className="px-5 py-2.5 rounded-xl bg-emerald-500 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-md shadow-emerald-500/20 cursor-pointer"
              >
                <span>Try Instant Scan</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>

            {/* Visual Breakdown Cards */}
            <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              
              <div className="p-4 rounded-2xl bg-white/5 border border-white/5 space-y-2">
                <span className="text-[11px] font-bold text-slate-400 uppercase">FSSAI Status</span>
                <div className="font-bold text-white text-sm">Regulation 2.4.6 (Noodles)</div>
                <p className="text-slate-400 text-[11px]">Approved for market distribution with standard permitted additives.</p>
              </div>

              <div className="p-4 rounded-2xl bg-white/5 border border-white/5 space-y-2">
                <span className="text-[11px] font-bold text-slate-400 uppercase">Adulterant Screen</span>
                <div className="font-bold text-emerald-400 text-sm flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Zero Toxic Dyes</span>
                </div>
                <p className="text-slate-400 text-[11px]">No Lead Chromate or Metanil Yellow identified.</p>
              </div>

              <div className="p-4 rounded-2xl bg-white/5 border border-white/5 space-y-2">
                <span className="text-[11px] font-bold text-slate-400 uppercase">Nutritional Profiling</span>
                <div className="font-bold text-amber-400 text-sm">860mg Sodium (High)</div>
                <p className="text-slate-400 text-[11px]">Exceeds 40% of standard daily recommended intake.</p>
              </div>

              <div className="p-4 rounded-2xl bg-white/5 border border-white/5 space-y-2">
                <span className="text-[11px] font-bold text-slate-400 uppercase">Model Benchmark</span>
                <div className="font-bold text-cyan-400 text-sm">Gradient Boosting</div>
                <p className="text-slate-400 text-[11px]">99.86% F1 validation score across 3,500 labeled products.</p>
              </div>

            </div>

          </div>

        </div>

      </section>

      {/* ── 8. AI Explanation Section ── */}
      <section className="py-20 px-4 sm:px-6 lg:px-12 max-w-7xl mx-auto space-y-12">
        
        <div className="max-w-2xl space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
            Explainable AI
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Don't just get a score. <br />
            Understand why.
          </h2>
          <p className="text-xs sm:text-sm text-slate-300">
            FoodGuard breaks down every evaluation into clear positive and negative contributors.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* Positive Factors */}
          <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-4 border border-emerald-500/25 bg-emerald-500/5">
            <div className="flex items-center gap-2 text-emerald-400 font-bold text-base">
              <CheckCircle2 className="w-5 h-5" />
              <span>Nutritional Assets (+ Positive)</span>
            </div>
            <ul className="space-y-2 text-xs sm:text-sm text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 font-bold">•</span>
                <span>Clean crude protein content from dietary wheat gluten.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 font-bold">•</span>
                <span>Zero industrial trans-fat isomers (&lt; 0.2g / 100g).</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 font-bold">•</span>
                <span>Fortified with Calcium Carbonate for mineral enrichment.</span>
              </li>
            </ul>
          </div>

          {/* Negative Factors */}
          <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-4 border border-rose-500/25 bg-rose-500/5">
            <div className="flex items-center gap-2 text-rose-400 font-bold text-base">
              <AlertTriangle className="w-5 h-5" />
              <span>Score Dampening Factors (− Negative)</span>
            </div>
            <ul className="space-y-2 text-xs sm:text-sm text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-rose-400 font-bold">•</span>
                <span>High sodium concentration (860mg per serving).</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-rose-400 font-bold">•</span>
                <span>Contains synthetic flavor enhancers (INS 635, INS 627).</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-rose-400 font-bold">•</span>
                <span>High refined palm oil density contributing to saturated fats.</span>
              </li>
            </ul>
          </div>

        </div>

      </section>

      {/* ── 8B. FoodGuard AI Chatbot Assistant Showcase ── */}
      <section className="py-20 px-4 sm:px-6 lg:px-12 max-w-7xl mx-auto space-y-12">
        <div className="rounded-3xl glass-panel p-8 sm:p-12 border border-emerald-500/30 bg-gradient-to-br from-emerald-950/40 via-slate-900/60 to-slate-950/90 shadow-2xl">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            
            {/* Left Content */}
            <div className="lg:col-span-5 space-y-5">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-bold uppercase">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Conversational Food Intelligence</span>
              </div>

              <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
                Your personal AI food safety companion.
              </h2>

              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                Got questions about unpronounceable additives, sodium limits, or FSSAI compliance? FoodGuard AI is context-aware and ready to answer any food formulation question in real time.
              </p>

              <div className="space-y-2.5 text-xs text-slate-300">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>Breaks down complex INS/E-numbers and preservatives</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>Explains why specific products received their safety scores</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>Audits statutory FSSAI compliance and permissible limits</span>
                </div>
              </div>

              <div className="pt-2">
                <button
                  onClick={handlePrimaryAction}
                  className="flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs sm:text-sm shadow-md shadow-emerald-500/20 transition-all cursor-pointer"
                >
                  <span>Try FoodGuard AI Assistant</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Right Chat Mockup */}
            <div className="lg:col-span-7">
              <div className="rounded-2xl glass-panel border border-white/10 p-5 space-y-3.5 bg-slate-950/80 shadow-xl max-w-lg mx-auto">
                
                {/* Chat Mockup Header */}
                <div className="flex items-center justify-between pb-3 border-b border-white/10 text-xs">
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-[10px]">
                      AI
                    </div>
                    <span className="font-bold text-white">FoodGuard AI</span>
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  </div>
                  <span className="text-[10px] text-slate-400">Active Context: Maggi Noodles</span>
                </div>

                {/* User Message */}
                <div className="flex justify-end">
                  <div className="rounded-2xl rounded-tr-xs bg-emerald-600 text-slate-950 font-medium px-3.5 py-2 text-xs max-w-[85%]">
                    Why did Maggi Noodles get a 64/100 score?
                  </div>
                </div>

                {/* AI Response */}
                <div className="flex justify-start">
                  <div className="rounded-2xl rounded-tl-xs glass-card border border-white/10 text-slate-200 p-3.5 text-xs max-w-[90%] space-y-1.5 leading-relaxed">
                    <p>
                      <strong>Maggi 2-Minute Noodles</strong> received <strong>64/100</strong> (Moderate Risk) mainly because:
                    </p>
                    <ul className="space-y-0.5 text-[11px] text-slate-300">
                      <li>• <strong>Sodium:</strong> 860mg per serving (high concentration).</li>
                      <li>• <strong>Cooking Medium:</strong> Refined palmolein oil (saturated fat).</li>
                      <li>• <strong>Flavor Enhancers:</strong> Contains INS 635.</li>
                    </ul>
                    <p className="text-[11px] text-emerald-400 font-semibold pt-1">
                      ✓ Positive: No prohibited chemical dyes (Metanil Yellow) detected. Conforms to FSSAI Regulation 2.4.6.
                    </p>
                  </div>
                </div>

                {/* Follow-up Chips */}
                <div className="flex flex-wrap gap-1.5 pt-1 text-[10px]">
                  <span className="px-2 py-0.5 rounded-lg bg-white/5 border border-white/10 text-slate-300">Is sodium level high?</span>
                  <span className="px-2 py-0.5 rounded-lg bg-white/5 border border-white/10 text-slate-300">What is INS 635?</span>
                  <span className="px-2 py-0.5 rounded-lg bg-white/5 border border-white/10 text-emerald-400 font-semibold">FSSAI standards →</span>
                </div>

              </div>
            </div>

          </div>
        </div>
      </section>

      {/* ── 8C. The Four Pillars of FoodGuard AI ── */}
      <section className="py-20 px-4 sm:px-6 lg:px-12 max-w-7xl mx-auto space-y-12">
        <div className="max-w-2xl space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
            Platform Architecture
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Built on Four Interlocking Pillars.
          </h2>
          <p className="text-xs sm:text-sm text-slate-300">
            A multi-criteria decision framework that evaluates your food beyond simple binary labels.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          
          <div className="glass-panel rounded-3xl p-6 space-y-3 border border-emerald-500/25 bg-emerald-500/5">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold">
              01
            </div>
            <h3 className="text-base font-bold text-white">Adulteration Screening</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Screens for banned toxic industrial colorants (Metanil Yellow, Sudan I–IV), heavy metals (Lead Chromate), and counterfeit milk markers.
            </p>
          </div>

          <div className="glass-panel rounded-3xl p-6 space-y-3 border border-amber-500/25 bg-amber-500/5">
            <div className="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold">
              02
            </div>
            <h3 className="text-base font-bold text-white">Health Risk Assessment</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Multi-dimensional risk scores combining ingredient toxicity profiles, bad fat indices, sugar-to-fiber ratios, and additive densities.
            </p>
          </div>

          <div className="glass-panel rounded-3xl p-6 space-y-3 border border-blue-500/25 bg-blue-500/5">
            <div className="w-10 h-10 rounded-xl bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold">
              03
            </div>
            <h3 className="text-base font-bold text-white">Global Regulatory Engine</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Cross-compares legality and limits across India (FSSAI), USA (FDA), EU (EFSA), Germany (BVL), and the UK (FSA).
            </p>
          </div>

          <div className="glass-panel rounded-3xl p-6 space-y-3 border border-teal-500/25 bg-teal-500/5">
            <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-400 flex items-center justify-center font-bold">
              04
            </div>
            <h3 className="text-base font-bold text-white">Consumer Intelligence</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Personalized dietary profiling for Low Sugar, Low Sodium, Vegan, Vegetarian, Gluten Awareness, and Clean Label preferences.
            </p>
          </div>

        </div>
      </section>

      {/* ── 8D. Global Competitive Landscape Table ── */}
      <section className="py-16 px-4 sm:px-6 lg:px-12 max-w-7xl mx-auto space-y-8">
        <div className="space-y-2 text-center max-w-3xl mx-auto">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
            Market Positioning
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            How FoodGuard Compares Globally
          </h2>
          <p className="text-xs sm:text-sm text-slate-300">
            Consumer-oriented food safety intelligence combining ingredient screening, adulteration assessment, risk assessment, country-specific regulatory comparison, and personalized consumer guidance.
          </p>
        </div>

        <div className="glass-panel rounded-3xl p-6 border border-white/10 overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-slate-400 font-bold uppercase tracking-wider text-[10px]">
                <th className="py-2.5 px-3">Company / System</th>
                <th className="py-2.5 px-3">Reach</th>
                <th className="py-2.5 px-3">Main Technology</th>
                <th className="py-2.5 px-2 text-center">Adulteration Screening</th>
                <th className="py-2.5 px-2 text-center">Risk Assessment</th>
                <th className="py-2.5 px-2 text-center">Global Regulatory</th>
                <th className="py-2.5 px-2 text-center">Personalized Rules</th>
                <th className="py-2.5 px-3 text-right">Similarity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              
              <tr className="bg-emerald-500/10 font-bold text-emerald-400">
                <td className="py-3 px-3 flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  <span>FoodGuard AI</span>
                </td>
                <td className="py-3 px-3">India / Global</td>
                <td className="py-3 px-3">Multi-Layer AI + Vision + Rules</td>
                <td className="py-3 px-2 text-center font-bold text-emerald-400">✓ ML + Chemical</td>
                <td className="py-3 px-2 text-center font-bold text-emerald-400">✓ Multi-Tier</td>
                <td className="py-3 px-2 text-center font-bold text-emerald-400">✓ 5 Nations</td>
                <td className="py-3 px-2 text-center font-bold text-emerald-400">✓ Configurable</td>
                <td className="py-3 px-3 text-right text-emerald-400">Benchmark</td>
              </tr>

              <tr className="text-slate-300">
                <td className="py-2.5 px-3 font-semibold text-white">Yuka</td>
                <td className="py-2.5 px-3 text-slate-400">Europe / USA</td>
                <td className="py-2.5 px-3 text-slate-400">Barcode Lookup + Nutri-Score</td>
                <td className="py-2.5 px-2 text-center text-slate-500">✕ No ML Screening</td>
                <td className="py-2.5 px-2 text-center text-emerald-400">✓ Additive Matrix</td>
                <td className="py-2.5 px-2 text-center text-slate-500">✕ Single Region</td>
                <td className="py-2.5 px-2 text-center text-slate-500">✕ Fixed Rules</td>
                <td className="py-2.5 px-3 text-right text-slate-400">Moderate</td>
              </tr>

              <tr className="text-slate-300">
                <td className="py-2.5 px-3 font-semibold text-white">Open Food Facts</td>
                <td className="py-2.5 px-3 text-slate-400">Worldwide</td>
                <td className="py-2.5 px-3 text-slate-400">Open-source crowdsourced DB</td>
                <td className="py-2.5 px-2 text-center text-slate-500">✕ No Adulteration</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✓ Nutri-Score / NOVA</td>
                <td className="py-2.5 px-2 text-center text-slate-500">✕ No Comparative</td>
                <td className="py-2.5 px-2 text-center text-slate-500">✕ Basic Filters</td>
                <td className="py-2.5 px-3 text-right text-slate-400">Data Source</td>
              </tr>

              <tr className="text-slate-300">
                <td className="py-2.5 px-3 font-semibold text-white">Genesis R&D / Trustwell</td>
                <td className="py-2.5 px-3 text-slate-400">Enterprise B2B</td>
                <td className="py-2.5 px-3 text-slate-400">Enterprise Formulation Software</td>
                <td className="py-2.5 px-2 text-center text-slate-500">✕ Enterprise Spec</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✓ Formulation B2B</td>
                <td className="py-2.5 px-2 text-center text-emerald-400">✓ Heavy B2B</td>
                <td className="py-2.5 px-2 text-center text-slate-500">✕ Enterprise Only</td>
                <td className="py-2.5 px-3 text-right text-slate-400">Low (B2B Tool)</td>
              </tr>

            </tbody>
          </table>
        </div>
      </section>

      {/* ── 9. Statistics Section ── */}
      <section id="about" className="py-16 px-4 sm:px-6 lg:px-12 max-w-7xl mx-auto border-t border-white/10">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          
          <div className="space-y-1">
            <div className="text-3xl sm:text-4xl font-black text-white font-mono">3,500+</div>
            <p className="text-xs text-slate-400 font-medium">Products Evaluated</p>
          </div>

          <div className="space-y-1">
            <div className="text-3xl sm:text-4xl font-black text-emerald-400 font-mono">5 Nations</div>
            <p className="text-xs text-slate-400 font-medium">Regulatory Frameworks</p>
          </div>

          <div className="space-y-1">
            <div className="text-3xl sm:text-4xl font-black text-cyan-400 font-mono">99.86%</div>
            <p className="text-xs text-slate-400 font-medium">Model F1-Score</p>
          </div>

          <div className="space-y-1">
            <div className="text-3xl sm:text-4xl font-black text-purple-400 font-mono">4 Pillars</div>
            <p className="text-xs text-slate-400 font-medium">Multi-Criteria AI</p>
          </div>

        </div>
      </section>

      {/* ── 10. Final Call To Action ── */}
      <section className="py-20 px-4 sm:px-6 lg:px-12 max-w-5xl mx-auto">
        <div className="rounded-3xl glass-panel p-8 sm:p-14 border border-emerald-500/30 text-center space-y-6 relative overflow-hidden bg-gradient-to-b from-emerald-950/30 to-slate-950/80 shadow-2xl">
          
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-40 bg-emerald-500/20 rounded-full blur-3xl pointer-events-none" />

          <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 relative z-10 block">
            Start Verifying Today
          </span>

          <h2 className="text-3xl sm:text-5xl font-black text-white tracking-tight relative z-10 leading-tight">
            Make your next food choice <br />
            an informed one.
          </h2>

          <p className="text-sm sm:text-base text-slate-300 max-w-md mx-auto relative z-10">
            Scan. Analyze. Understand.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2 relative z-10">
            <button
              onClick={handlePrimaryAction}
              className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-sm sm:text-base transition-all shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40 cursor-pointer"
            >
              {isAuthenticated ? 'Open Dashboard' : 'Get Started — It\'s Free'}
            </button>
            <button
              onClick={() => scrollToSection('features')}
              className="w-full sm:w-auto px-6 py-3.5 rounded-2xl glass-panel hover:bg-white/10 text-white font-bold text-sm sm:text-base border border-white/10 transition-colors cursor-pointer"
            >
              Explore the Platform
            </button>
          </div>

        </div>
      </section>

      {/* ── 11. Footer ── */}
      <footer className="border-t border-white/10 py-12 px-4 sm:px-6 lg:px-12 bg-black/40 text-xs text-slate-400">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center text-emerald-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <span className="text-sm font-bold text-white block">FoodGuard AI</span>
              <span className="text-[10px] text-slate-500">AI Food Safety Platform</span>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-6 text-slate-300 font-medium">
            <button onClick={() => scrollToSection('problem')} className="hover:text-white">Product</button>
            <button onClick={() => scrollToSection('features')} className="hover:text-white">Features</button>
            <button onClick={() => scrollToSection('how-it-works')} className="hover:text-white">How It Works</button>
            <button onClick={() => scrollToSection('technology')} className="hover:text-white">Technology</button>
            <button onClick={() => scrollToSection('about')} className="hover:text-white">About</button>
          </div>

          <div className="text-slate-500 text-center md:text-right">
            © {new Date().getFullYear()} FoodGuard AI. All rights reserved.
          </div>

        </div>
      </footer>

    </div>
  );
}
