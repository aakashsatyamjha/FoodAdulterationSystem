import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Mail, 
  Lock, 
  User, 
  Eye, 
  EyeOff, 
  ArrowRight, 
  Sparkles, 
  CheckCircle2, 
  AlertCircle, 
  Scale, 
  Database, 
  ScanLine, 
  Loader2,
  Check,
  HelpCircle
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export default function AuthPage({ onAuthSuccess, initialMode = 'login', onBackToHome }) {
  const { login, signup, resetPassword } = useAuth();
  const { resolvedTheme } = useTheme();

  const [mode, setMode] = useState(initialMode); // 'login' | 'signup' | 'forgot'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  // Form Fields
  const [email, setEmail] = useState('akash@foodguard.ai');
  const [password, setPassword] = useState('password123');
  const [confirmPassword, setConfirmPassword] = useState('password123');
  const [fullName, setFullName] = useState('Aakash S.');
  const [rememberMe, setRememberMe] = useState(true);
  const [agreeTerms, setAgreeTerms] = useState(true);
  const [showPassword, setShowPassword] = useState(false);

  // Password strength calculation
  const getPasswordStrength = (pwd) => {
    if (!pwd) return { level: 0, label: 'None', color: 'bg-slate-300 dark:bg-slate-700' };
    if (pwd.length < 6) return { level: 1, label: 'Weak', color: 'bg-rose-500' };
    if (pwd.length < 9) return { level: 2, label: 'Medium', color: 'bg-amber-500' };
    return { level: 3, label: 'Strong', color: 'bg-emerald-500' };
  };

  const pwdStrength = getPasswordStrength(password);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);
    setLoading(true);

    try {
      if (mode === 'login') {
        await login(email, password, rememberMe);
        if (onAuthSuccess) onAuthSuccess();
      } else if (mode === 'signup') {
        if (password !== confirmPassword) {
          throw new Error('Passwords do not match. Please re-check.');
        }
        if (!agreeTerms) {
          throw new Error('Please agree to the Terms of Service & Privacy Policy.');
        }
        await signup(fullName, email, password);
        if (onAuthSuccess) onAuthSuccess();
      } else if (mode === 'forgot') {
        await resetPassword(email);
        setSuccessMessage(`Password reset link has been dispatched to ${email}. Please check your inbox.`);
      }
    } catch (err) {
      setError(err.message || 'Authentication failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center p-4 sm:p-6 lg:p-10 bg-[#0a0f1d] text-slate-100 relative overflow-hidden font-sans select-none">
      
      {/* Ambient background glows */}
      <div className="absolute top-10 left-10 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-10 right-10 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-500/5 rounded-full blur-3xl pointer-events-none" />

      {/* Main Container Card */}
      <div className="w-full max-w-5xl rounded-3xl glass-panel border border-white/10 shadow-2xl overflow-hidden grid grid-cols-1 lg:grid-cols-12 relative z-10">
        
        {/* Left Column (5 cols on lg): Brand Showcase */}
        <div className="lg:col-span-5 p-8 sm:p-10 bg-gradient-to-br from-emerald-950/40 via-slate-900/60 to-slate-950/80 border-b lg:border-b-0 lg:border-r border-white/10 flex flex-col justify-between space-y-8">
          
          {/* Back Button & Logo & Headline */}
          <div className="space-y-6">
            {onBackToHome && (
              <button
                type="button"
                onClick={onBackToHome}
                className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-400 hover:text-emerald-300 transition-colors cursor-pointer"
              >
                <span>← Back to Public Homepage</span>
              </button>
            )}

            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shadow-lg shadow-emerald-500/20">
                <ShieldCheck className="w-6 h-6 stroke-[2.2]" />
              </div>
              <div>
                <span className="text-xl font-bold tracking-tight text-white block">
                  FoodGuard
                </span>
                <span className="text-[10px] uppercase font-semibold tracking-wider text-emerald-400">
                  AI Food Safety Platform
                </span>
              </div>
            </div>

            <div className="space-y-2">
              <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight leading-tight">
                Intelligent Food Safety & Adulteration Screening.
              </h1>
              <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
                Scan packaged food products, audit ingredient formulations, and verify FSSAI regulatory compliance in real time.
              </p>
            </div>
          </div>

          {/* Feature Highlights List */}
          <div className="space-y-3.5 text-xs text-slate-300">
            <div className="flex items-start gap-3 p-3 rounded-2xl bg-white/5 border border-white/5">
              <div className="w-7 h-7 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0 mt-0.5">
                <Sparkles className="w-4 h-4" />
              </div>
              <div>
                <strong className="text-white block text-xs">AI Quality Scorer (0–100)</strong>
                <span className="text-[11px] text-slate-400">Gradient Boosting ML classifier with 99.86% F1 accuracy.</span>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 rounded-2xl bg-white/5 border border-white/5">
              <div className="w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 flex items-center justify-center shrink-0 mt-0.5">
                <Scale className="w-4 h-4" />
              </div>
              <div>
                <strong className="text-white block text-xs">FSSAI 2025 Statutory Audit</strong>
                <span className="text-[11px] text-slate-400">Flags prohibited dyes, trans-fat violations, and heavy metals.</span>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 rounded-2xl bg-white/5 border border-white/5">
              <div className="w-7 h-7 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center shrink-0 mt-0.5">
                <ScanLine className="w-4 h-4" />
              </div>
              <div>
                <strong className="text-white block text-xs">Dual Input Scanner</strong>
                <span className="text-[11px] text-slate-400">Supports live camera EAN-13 barcodes & Tesseract.js OCR.</span>
              </div>
            </div>
          </div>

          {/* Footer Badge */}
          <div className="flex items-center justify-between text-[11px] text-slate-500 pt-2 border-t border-white/5">
            <span>Powered by Open Food Facts & FSSAI</span>
            <span className="font-mono text-emerald-400">v2.4 Live</span>
          </div>

        </div>

        {/* Right Column (7 cols on lg): Auth Forms */}
        <div className="lg:col-span-7 p-8 sm:p-10 flex flex-col justify-center space-y-6">
          
          {/* Form Header */}
          <div className="space-y-1">
            <h2 className="text-2xl font-bold text-white tracking-tight">
              {mode === 'login' && 'Sign in to your account'}
              {mode === 'signup' && 'Create your FoodGuard account'}
              {mode === 'forgot' && 'Reset your password'}
            </h2>
            <p className="text-xs text-slate-400">
              {mode === 'login' && 'Enter your credentials to access the food safety analytics dashboard.'}
              {mode === 'signup' && 'Join thousands of inspectors and consumers verifying food authenticity.'}
              {mode === 'forgot' && 'Enter your registered email address to receive reset instructions.'}
            </p>
          </div>

          {/* Error Alert */}
          {error && (
            <div className="p-3.5 rounded-2xl bg-rose-500/15 border border-rose-500/30 text-xs text-rose-300 flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {/* Success Alert */}
          {successMessage && (
            <div className="p-3.5 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 text-xs text-emerald-300 flex items-start gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>{successMessage}</span>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            
            {/* Full Name (Sign Up only) */}
            {mode === 'signup' && (
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-300 block">
                  Full Name
                </label>
                <div className="relative">
                  <User className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="e.g. Aakash Sharma"
                    className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-900/80 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all"
                  />
                </div>
              </div>
            )}

            {/* Email Address */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300 block">
                Email Address
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@domain.com"
                  className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-900/80 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all"
                />
              </div>
            </div>

            {/* Password (Login & Sign Up) */}
            {mode !== 'forgot' && (
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-semibold text-slate-300">
                    Password
                  </label>
                  {mode === 'login' && (
                    <button
                      type="button"
                      onClick={() => { setMode('forgot'); setError(null); }}
                      className="text-xs text-emerald-400 hover:text-emerald-300 font-medium transition-colors cursor-pointer"
                    >
                      Forgot password?
                    </button>
                  )}
                </div>

                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    className="w-full pl-10 pr-10 py-3 rounded-xl bg-slate-900/80 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 cursor-pointer"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>

                {/* Password Strength Indicator (Sign Up) */}
                {mode === 'signup' && (
                  <div className="space-y-1 pt-1">
                    <div className="flex items-center justify-between text-[10px] text-slate-400">
                      <span>Password Strength: <strong className="text-white">{pwdStrength.label}</strong></span>
                      <span>Min. 6 characters</span>
                    </div>
                    <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden flex gap-1">
                      <div className={`h-full flex-1 rounded-full ${pwdStrength.level >= 1 ? pwdStrength.color : 'bg-slate-700'}`} />
                      <div className={`h-full flex-1 rounded-full ${pwdStrength.level >= 2 ? pwdStrength.color : 'bg-slate-700'}`} />
                      <div className={`h-full flex-1 rounded-full ${pwdStrength.level >= 3 ? pwdStrength.color : 'bg-slate-700'}`} />
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Confirm Password (Sign Up only) */}
            {mode === 'signup' && (
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-300 block">
                  Confirm Password
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter password"
                    className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-900/80 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all"
                  />
                </div>
              </div>
            )}

            {/* Checkboxes: Remember me (Login) / Terms (Sign Up) */}
            {mode === 'login' && (
              <div className="flex items-center justify-between pt-1">
                <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="w-4 h-4 rounded bg-slate-900 border-white/10 text-emerald-500 focus:ring-emerald-500 cursor-pointer"
                  />
                  <span>Remember me on this device</span>
                </label>
              </div>
            )}

            {mode === 'signup' && (
              <div className="pt-1">
                <label className="flex items-start gap-2 text-xs text-slate-300 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={agreeTerms}
                    onChange={(e) => setAgreeTerms(e.target.checked)}
                    className="w-4 h-4 rounded bg-slate-900 border-white/10 text-emerald-500 focus:ring-emerald-500 cursor-pointer shrink-0 mt-0.5"
                  />
                  <span className="text-[11px] text-slate-400">
                    I agree to the <strong className="text-white">Terms of Service</strong> and <strong className="text-white">Privacy Policy</strong>.
                  </span>
                </label>
              </div>
            )}

            {/* Submit CTA Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs sm:text-sm transition-all shadow-lg shadow-emerald-500/20 disabled:opacity-50 flex items-center justify-center gap-2 cursor-pointer mt-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Authenticating...</span>
                </>
              ) : (
                <>
                  <span>
                    {mode === 'login' && 'Sign In to FoodGuard'}
                    {mode === 'signup' && 'Create Free Account'}
                    {mode === 'forgot' && 'Send Reset Link'}
                  </span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>

          </form>

          {/* Mode Switchers */}
          <div className="pt-4 border-t border-white/10 text-center text-xs text-slate-400">
            {mode === 'login' && (
              <p>
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={() => { setMode('signup'); setError(null); }}
                  className="font-bold text-emerald-400 hover:text-emerald-300 transition-colors cursor-pointer"
                >
                  Create Account
                </button>
              </p>
            )}

            {mode === 'signup' && (
              <p>
                Already have an account?{' '}
                <button
                  type="button"
                  onClick={() => { setMode('login'); setError(null); }}
                  className="font-bold text-emerald-400 hover:text-emerald-300 transition-colors cursor-pointer"
                >
                  Sign In
                </button>
              </p>
            )}

            {mode === 'forgot' && (
              <p>
                Remembered your password?{' '}
                <button
                  type="button"
                  onClick={() => { setMode('login'); setError(null); setSuccessMessage(null); }}
                  className="font-bold text-emerald-400 hover:text-emerald-300 transition-colors cursor-pointer"
                >
                  Back to Sign In
                </button>
              </p>
            )}
          </div>

        </div>

      </div>

    </div>
  );
}
