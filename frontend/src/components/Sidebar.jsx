import React from 'react';
import { 
  LayoutDashboard, 
  Barcode, 
  FileText, 
  History, 
  Cpu, 
  Sparkles, 
  Settings, 
  HelpCircle, 
  ShieldCheck, 
  Crown, 
  LogOut,
  X,
  User,
  Globe,
  UserCheck
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Sidebar({ 
  activeTab, 
  setActiveTab, 
  hasAnalysis, 
  sidebarOpen, 
  setSidebarOpen,
  onOpenSettings,
  onOpenHelp,
  onGoToLanding
}) {
  const { user, logout, triggerOpeningSplash } = useAuth();

  const navItems = [
    { id: 'home', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'barcode', label: 'Barcode Scanner', icon: Barcode },
    { id: 'ingredient', label: 'Ingredient OCR', icon: FileText },
    ...(hasAnalysis ? [{ id: 'analysis', label: 'Product Safety Report', icon: Sparkles, badge: 'Live' }] : []),
    { id: 'regulatory', label: 'Global Regulatory', icon: Globe, badge: '5 Countries' },
    { id: 'consumer', label: 'Consumer Profile', icon: UserCheck },
    { id: 'history', label: 'Scan History', icon: History },
    { id: 'models', label: 'ML Benchmarks', icon: Cpu },
  ];

  const handleNavClick = (tabId) => {
    setActiveTab(tabId);
    if (window.innerWidth < 1024) {
      setSidebarOpen(false);
    }
  };

  const handleLogoClick = () => {
    triggerOpeningSplash(() => {
      handleNavClick('home');
    });
  };

  return (
    <>
      {/* Mobile Backdrop Overlay */}
      {sidebarOpen && (
        <div 
          onClick={() => setSidebarOpen(false)}
          className="fixed inset-0 z-20 bg-black/70 backdrop-blur-xs lg:hidden"
        />
      )}

      {/* Sidebar Container */}
      <aside className={`
        fixed top-0 bottom-0 left-0 z-30 w-64 transition-transform duration-300 ease-in-out
        glass-panel border-r flex flex-col justify-between
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        
        {/* Top: Logo & Navigation */}
        <div className="p-4 space-y-6 overflow-y-auto">
          
          {/* Logo & Brand */}
          <div className="flex items-center justify-between px-2 pt-1">
            <div 
              onClick={handleLogoClick}
              className="flex items-center gap-3 cursor-pointer group"
              title="Click to replay opening animation"
            >
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500/20 to-teal-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 group-hover:scale-105 transition-transform shadow-xs">
                <ShieldCheck className="w-5 h-5 stroke-[2.2]" />
              </div>
              <div className="flex flex-col">
                <span className="text-base font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-1.5">
                  FoodGuard <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">AI</span>
                </span>
                <span className="text-[10px] font-medium text-slate-500 dark:text-slate-400 -mt-0.5">
                  Food Safety Platform
                </span>
              </div>
            </div>

            {/* Mobile close button */}
            <button
              onClick={() => setSidebarOpen(false)}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 lg:hidden cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation Links */}
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`
                    w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all cursor-pointer
                    ${isActive
                      ? 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 font-bold shadow-xs'
                      : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/50'
                    }
                  `}
                >
                  <div className="flex items-center gap-3">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-500' : 'text-slate-400'}`} />
                    <span>{item.label}</span>
                  </div>

                  {item.badge && (
                    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500 text-slate-950">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>

        </div>

        {/* Bottom: User Card, Settings, Help & Upgrade Banner */}
        <div className="p-4 space-y-3.5 border-t border-slate-200 dark:border-white/5 bg-slate-50/50 dark:bg-black/15">
          
          {/* User Quick Info */}
          {user && (
            <div className="p-2.5 rounded-xl bg-slate-100/60 dark:bg-slate-800/40 border border-slate-200 dark:border-white/5 flex items-center justify-between">
              <div className="flex items-center gap-2.5 overflow-hidden">
                <div className="w-7 h-7 rounded-lg bg-emerald-500/20 text-emerald-400 font-bold text-xs flex items-center justify-center shrink-0 border border-emerald-500/30">
                  {user.avatar || 'AS'}
                </div>
                <div className="truncate">
                  <p className="text-xs font-bold text-slate-900 dark:text-white truncate">{user.name}</p>
                  <p className="text-[10px] text-slate-400 truncate">{user.role || 'Inspector'}</p>
                </div>
              </div>
              <button
                onClick={logout}
                className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors cursor-pointer"
                title="Log Out"
              >
                <LogOut className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

          {/* Quick Settings & Help */}
          <div className="space-y-0.5">
            <button
              onClick={() => { onOpenSettings(); if (window.innerWidth < 1024) setSidebarOpen(false); }}
              className="w-full flex items-center gap-3 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/40 transition-colors cursor-pointer"
            >
              <Settings className="w-4 h-4 text-slate-400" />
              <span>Settings</span>
            </button>

            <button
              onClick={() => { onOpenHelp(); if (window.innerWidth < 1024) setSidebarOpen(false); }}
              className="w-full flex items-center gap-3 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/40 transition-colors cursor-pointer"
            >
              <HelpCircle className="w-4 h-4 text-slate-400" />
              <span>Help & Support</span>
            </button>
          </div>

          {/* Upgrade to Pro Card */}
          <div className="p-3.5 rounded-2xl bg-gradient-to-b from-emerald-500/15 to-teal-500/5 border border-emerald-500/25 space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-lg bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                <Crown className="w-3.5 h-3.5" />
              </div>
              <span className="text-xs font-bold text-slate-900 dark:text-white">Upgrade to Pro</span>
            </div>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-tight">
              Unlock global export certifications, batch regulatory screening, and NABL lab integration.
            </p>
            <button 
              onClick={() => onOpenSettings()}
              className="w-full py-1.5 px-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition-colors shadow-sm cursor-pointer"
            >
              Upgrade Now
            </button>
          </div>

        </div>

      </aside>
    </>
  );
}
