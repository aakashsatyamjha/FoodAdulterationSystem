import React, { useState, useEffect } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import SettingsModal from './components/SettingsModal';
import HelpModal from './components/HelpModal';
import SplashAnimation from './components/SplashAnimation';
import Chatbot from './components/Chatbot';
import LandingPage from './pages/LandingPage';
import AuthPage from './pages/AuthPage';
import Home from './pages/Home';
import BarcodeScanner from './pages/BarcodeScanner';
import IngredientScanner from './pages/IngredientScanner';
import ProductAnalysis from './pages/ProductAnalysis';
import RegulatoryIntelligence from './pages/RegulatoryIntelligence';
import ConsumerIntelligence from './pages/ConsumerIntelligence';
import ScanHistory from './pages/ScanHistory';
import ModelExplorer from './pages/ModelExplorer';

function AppContent() {
  const { isAuthenticated, isOpeningSplashActive, triggerOpeningSplash } = useAuth();

  // Navigation View: 'landing' | 'auth' | 'app' (Persisted across page refreshes)
  const [currentView, setCurrentView] = useState(() => {
    try {
      const saved = sessionStorage.getItem('foodguard_current_view');
      if (saved) return saved;
      return 'auth';
    } catch {
      return 'auth';
    }
  });
  const [authInitialMode, setAuthInitialMode] = useState('login'); // 'login' | 'signup'

  // Chatbot Assistant State
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatInitialQuery, setChatInitialQuery] = useState(null);

  // Active Tab & Analysis State (Persisted across page refreshes)
  const [activeTab, setActiveTab] = useState(() => {
    try {
      const saved = sessionStorage.getItem('foodguard_active_tab');
      return saved || 'home';
    } catch {
      return 'home';
    }
  });

  const [currentAnalysis, setCurrentAnalysis] = useState(() => {
    try {
      const saved = sessionStorage.getItem('foodguard_current_analysis');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sampleBarcodes, setSampleBarcodes] = useState([]);

  // Auto-sync navigation and report state with sessionStorage
  useEffect(() => {
    try {
      sessionStorage.setItem('foodguard_current_view', currentView);
    } catch (e) {
      console.warn("Storage sync notice:", e);
    }
  }, [currentView]);

  useEffect(() => {
    try {
      sessionStorage.setItem('foodguard_active_tab', activeTab);
    } catch (e) {
      console.warn("Storage sync notice:", e);
    }
  }, [activeTab]);

  useEffect(() => {
    try {
      if (currentAnalysis) {
        sessionStorage.setItem('foodguard_current_analysis', JSON.stringify(currentAnalysis));
      } else {
        sessionStorage.removeItem('foodguard_current_analysis');
      }
    } catch (e) {
      console.warn("Storage sync notice:", e);
    }
  }, [currentAnalysis]);
  
  // Persistent User Preferences & Thresholds
  const [userPreferences, setUserPreferences] = useState(() => {
    try {
      const saved = localStorage.getItem('foodguard_user_preferences');
      return saved ? JSON.parse(saved) : {
        low_sugar: true,
        low_sodium: false,
        high_protein: false,
        vegetarian: true,
        vegan: false,
        gluten_free: false,
        allergen_safe: false,
        low_additives: true,
        low_processed: true
      };
    } catch {
      return { vegetarian: true, low_sugar: true, low_additives: true };
    }
  });

  const [customThresholds, setCustomThresholds] = useState(() => {
    try {
      const saved = localStorage.getItem('foodguard_user_thresholds');
      return saved ? JSON.parse(saved) : {
        sugar_max: 5.0,
        sodium_max: 140.0,
        protein_min: 8.0,
        additives_max: 3
      };
    } catch {
      return { sugar_max: 5.0, sodium_max: 140.0, protein_min: 8.0, additives_max: 3 };
    }
  });

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);

  const openChatWithQuery = (query) => {
    setChatInitialQuery(query);
    setIsChatOpen(true);
  };

  useEffect(() => {
    fetchSamples();
  }, []);

  const fetchSamples = async () => {
    try {
      const res = await fetch('/api/samples');
      if (res.ok) {
        const data = await res.json();
        setSampleBarcodes(data);
      }
    } catch (e) {
      console.log("Samples fetch note:", e);
    }
  };

  const handleBarcodeScan = async (barcode) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/barcode/${barcode}?country=IN`);
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Product with barcode ${barcode} could not be retrieved from the catalog.`);
      }
      const data = await res.json();
      setCurrentAnalysis(data);
      setActiveTab('analysis');
      setCurrentView('app');
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCustomAnalyze = async (payload) => {
    setLoading(true);
    setError(null);
    try {
      const fullPayload = {
        ...payload,
        user_preferences: userPreferences,
        custom_thresholds: customThresholds
      };
      const res = await fetch('/api/analyze/full', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(fullPayload)
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Analysis could not be completed.');
      }
      const data = await res.json();
      setCurrentAnalysis(data);
      setActiveTab('analysis');
      setCurrentView('app');
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectHistoryRecord = async (recordId) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/history/${recordId}`);
      if (res.ok) {
        const data = await res.json();
        setCurrentAnalysis(data);
        setActiveTab('analysis');
        setCurrentView('app');
      }
    } catch (err) {
      console.error("Failed to load history record:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSavePreferences = (newPrefs, newThresholds) => {
    setUserPreferences(newPrefs);
    if (newThresholds) setCustomThresholds(newThresholds);
  };

  const handleHeaderSearch = (query) => {
    if (!query) return;
    if (/^\d{8,14}$/.test(query.trim())) {
      handleBarcodeScan(query.trim());
    } else {
      setActiveTab('history');
      setCurrentView('app');
    }
  };

  // 1. Landing Page View (Public Homepage)
  if (currentView === 'landing') {
    return (
      <LandingPage 
        onGetStarted={() => {
          if (isAuthenticated) {
            triggerOpeningSplash(() => setCurrentView('app'));
          } else {
            setAuthInitialMode('signup');
            setCurrentView('auth');
          }
        }}
        onSignIn={() => {
          if (isAuthenticated) {
            triggerOpeningSplash(() => setCurrentView('app'));
          } else {
            setAuthInitialMode('login');
            setCurrentView('auth');
          }
        }}
        onOpenDashboard={() => {
          triggerOpeningSplash(() => setCurrentView('app'));
        }}
      />
    );
  }

  // 2. Authentication View (Login, Signup, Forgot Password)
  if (currentView === 'auth' || !isAuthenticated) {
    return (
      <AuthPage 
        initialMode={authInitialMode}
        onBackToHome={() => setCurrentView('landing')}
        onAuthSuccess={() => {
          setActiveTab('home');
          setCurrentView('app');
        }} 
      />
    );
  }

  // 3. Authenticated App & Dashboard View
  return (
    <div className="min-h-screen flex text-slate-900 dark:text-slate-100 font-sans selection:bg-emerald-500 selection:text-slate-950 relative">
      
      {/* ── FoodGuard Opening / Splash Screen Animation ── */}
      {isOpeningSplashActive && (
        <SplashAnimation onComplete={() => {}} />
      )}

      {/* ── Sidebar Navigation ── */}
      <Sidebar 
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        hasAnalysis={Boolean(currentAnalysis)}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
        onOpenSettings={() => setSettingsOpen(true)}
        onOpenHelp={() => setHelpOpen(true)}
        onGoToLanding={() => setCurrentView('landing')}
      />

      {/* ── Main Layout Wrapper (offset for fixed sidebar on lg+) ── */}
      <div className="flex-1 flex flex-col min-w-0 lg:pl-64 transition-all duration-300">
        
        {/* Top Header */}
        <Header 
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          onSearchSubmit={handleHeaderSearch}
          onOpenSettings={() => setSettingsOpen(true)}
          onOpenHelp={() => setHelpOpen(true)}
          onGoToLanding={() => setCurrentView('landing')}
        />

        {/* Workspace Canvas */}
        <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
          {activeTab === 'home' && (
            <Home 
              setActiveTab={setActiveTab} 
              onSelectSample={handleBarcodeScan}
              onOpenChat={openChatWithQuery} 
            />
          )}

          {activeTab === 'barcode' && (
            <BarcodeScanner 
              onScanSuccess={handleBarcodeScan}
              loading={loading}
              error={error}
              sampleBarcodes={sampleBarcodes}
            />
          )}

          {activeTab === 'ingredient' && (
            <IngredientScanner 
              onAnalyze={handleCustomAnalyze}
              loading={loading}
            />
          )}

          {activeTab === 'analysis' && currentAnalysis && (
            <ProductAnalysis 
              data={currentAnalysis}
              onReset={() => {
                setCurrentAnalysis(null);
                setActiveTab('barcode');
              }}
              onOpenChat={openChatWithQuery}
            />
          )}

          {activeTab === 'regulatory' && (
            <RegulatoryIntelligence 
              onSelectProductForAnalysis={handleBarcodeScan}
            />
          )}

          {activeTab === 'consumer' && (
            <ConsumerIntelligence 
              userPreferences={userPreferences}
              onSavePreferences={handleSavePreferences}
              onTestScan={handleBarcodeScan}
            />
          )}

          {activeTab === 'history' && (
            <ScanHistory 
              onSelectRecord={handleSelectHistoryRecord}
            />
          )}

          {activeTab === 'models' && (
            <ModelExplorer />
          )}
        </main>

        {/* Clean Dashboard Footer */}
        <footer className="border-t border-slate-200 dark:border-white/5 py-4 px-6 text-center text-xs text-slate-500 dark:text-slate-400 no-print flex flex-col sm:flex-row items-center justify-between gap-2">
          <p>
            FoodGuard AI • Food Safety + Adulteration Screening + Global Regulatory + Consumer Intelligence Platform
          </p>
          <button
            onClick={() => setCurrentView('landing')}
            className="text-emerald-500 hover:text-emerald-400 font-semibold cursor-pointer"
          >
            ← View Public Homepage
          </button>
        </footer>

      </div>

      {/* ── FoodGuard AI Chatbot Assistant (Global) ── */}
      <Chatbot 
        isOpen={isChatOpen}
        onToggle={() => setIsChatOpen(!isChatOpen)}
        currentAnalysis={currentAnalysis}
        activeTab={activeTab}
        initialQuery={chatInitialQuery}
        userPreferences={userPreferences}
        onNavigateToAnalysis={() => {
          setActiveTab('analysis');
          setIsChatOpen(false);
        }}
      />

      {/* Settings Modal */}
      <SettingsModal 
        isOpen={settingsOpen}
        onClose={() => setSettingsOpen(false)}
      />

      {/* Help Modal */}
      <HelpModal 
        isOpen={helpOpen}
        onClose={() => setHelpOpen(false)}
      />

    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ThemeProvider>
  );
}
