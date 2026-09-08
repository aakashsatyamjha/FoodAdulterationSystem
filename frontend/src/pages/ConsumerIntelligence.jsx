import React, { useState, useEffect } from 'react';
import { 
  UserCheck, 
  Sliders, 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  Info, 
  Save, 
  RotateCcw, 
  Sparkles, 
  Heart, 
  Leaf, 
  Wheat, 
  Activity,
  Layers,
  HelpCircle,
  BookOpen
} from 'lucide-react';

export default function ConsumerIntelligence({ userPreferences, onSavePreferences, onTestScan }) {
  const [preferences, setPreferences] = useState({
    low_sugar: true,
    low_sodium: false,
    high_protein: false,
    vegetarian: true,
    vegan: false,
    gluten_free: false,
    allergen_safe: false,
    low_additives: true,
    low_processed: true,
    ...(userPreferences || {})
  });

  const [thresholds, setThresholds] = useState({
    sugar_max: 5.0,
    sodium_max: 140.0,
    protein_min: 8.0,
    additives_max: 3
  });

  const [savedSuccess, setSavedSuccess] = useState(false);
  const [consumerRules, setConsumerRules] = useState([]);

  // Mock product simulator state
  const [simProduct, setSimProduct] = useState({
    name: "Custom Snack Formulation",
    sugar_g: 14.5,
    sodium_mg: 520.0,
    protein_g: 4.2,
    ingredients: "Wheat flour, Palm Oil, Sugar, Salt, Tartrazine (INS 102), Soy Lecithin, Milk solids, TBHQ"
  });
  const [simResult, setSimResult] = useState(null);
  const [simLoading, setSimLoading] = useState(false);

  useEffect(() => {
    fetchRules();
    runSimulator();
  }, []);

  const fetchRules = async () => {
    try {
      const res = await fetch('/api/consumer/rules');
      if (res.ok) {
        const data = await res.json();
        setConsumerRules(data);
      }
    } catch (err) {
      console.error("Failed to load consumer rules:", err);
    }
  };

  const handleToggle = (key) => {
    setPreferences(prev => {
      const updated = { ...prev, [key]: !prev[key] };
      return updated;
    });
  };

  const handleSave = () => {
    if (onSavePreferences) {
      onSavePreferences(preferences, thresholds);
    }
    localStorage.setItem('foodguard_user_preferences', JSON.stringify(preferences));
    localStorage.setItem('foodguard_user_thresholds', JSON.stringify(thresholds));
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2500);
    runSimulator();
  };

  const runSimulator = async () => {
    setSimLoading(true);
    try {
      const res = await fetch('/api/consumer/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ingredients: simProduct.ingredients,
          nutrition: {
            sugar_g: parseFloat(simProduct.sugar_g) || 0,
            sodium_mg: parseFloat(simProduct.sodium_mg) || 0,
            protein_g: parseFloat(simProduct.protein_g) || 0
          },
          preferences: preferences,
          custom_thresholds: thresholds
        })
      });
      if (res.ok) {
        const data = await res.json();
        setSimResult(data);
      }
    } catch (err) {
      console.error("Simulator error:", err);
    } finally {
      setSimLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6 pb-12 animate-fade-in">
      
      {/* ── Page Header ── */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-bold uppercase tracking-wider">
            <UserCheck className="w-3.5 h-3.5" />
            <span>Consumer Food Intelligence</span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Your Personal Food Profile & Dietary Preferences
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400 max-w-3xl">
            Configure nutritional ceilings, dietary restrictions, and clean-label preferences. FoodGuard will automatically evaluate every scanned product against your active profile.
          </p>
        </div>

        <button
          onClick={handleSave}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition-colors shadow-sm cursor-pointer shrink-0"
        >
          <Save className="w-4 h-4" />
          <span>{savedSuccess ? "Saved to Profile!" : "Save Preferences"}</span>
        </button>
      </div>

      {/* ── Grid Layout: Profile Configurator vs Live Simulator ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Preferences Toggles & Threshold Controls (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          
          {/* Dietary Restrictions Toggles Card */}
          <div className="glass-card rounded-2xl p-6 border space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Leaf className="w-4 h-4 text-emerald-500" />
                <span>Dietary Frameworks & Sensitivities</span>
              </h2>
              <span className="text-xs text-slate-500 dark:text-slate-400">Toggle active rules</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              
              {/* Vegetarian */}
              <div 
                onClick={() => handleToggle('vegetarian')}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-start justify-between gap-3 ${
                  preferences.vegetarian 
                    ? 'bg-emerald-500/15 border-emerald-500/40 text-slate-900 dark:text-white' 
                    : 'glass-card border-slate-200 dark:border-white/5 opacity-60'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-1.5 font-bold text-xs">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                    <span>Vegetarian</span>
                  </div>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400">
                    Flag animal gelatin, carmine (E120), lard, and meat enzymes.
                  </p>
                </div>
                <input 
                  type="checkbox" 
                  checked={preferences.vegetarian} 
                  onChange={() => {}} 
                  className="accent-emerald-500 mt-0.5"
                />
              </div>

              {/* Vegan */}
              <div 
                onClick={() => handleToggle('vegan')}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-start justify-between gap-3 ${
                  preferences.vegan 
                    ? 'bg-emerald-500/15 border-emerald-500/40 text-slate-900 dark:text-white' 
                    : 'glass-card border-slate-200 dark:border-white/5 opacity-60'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-1.5 font-bold text-xs">
                    <span className="w-2.5 h-2.5 rounded-full bg-teal-500"></span>
                    <span>Vegan (100% Plant-Based)</span>
                  </div>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400">
                    Flag dairy solids, casein, whey, honey, beeswax, and shellac.
                  </p>
                </div>
                <input 
                  type="checkbox" 
                  checked={preferences.vegan} 
                  onChange={() => {}} 
                  className="accent-emerald-500 mt-0.5"
                />
              </div>

              {/* Gluten Awareness */}
              <div 
                onClick={() => handleToggle('gluten_free')}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-start justify-between gap-3 ${
                  preferences.gluten_free 
                    ? 'bg-emerald-500/15 border-emerald-500/40 text-slate-900 dark:text-white' 
                    : 'glass-card border-slate-200 dark:border-white/5 opacity-60'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-1.5 font-bold text-xs">
                    <Wheat className="w-3.5 h-3.5 text-amber-500" />
                    <span>Gluten Awareness</span>
                  </div>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400">
                    Flag wheat flour, maida, barley malt, rye, and vital gluten.
                  </p>
                </div>
                <input 
                  type="checkbox" 
                  checked={preferences.gluten_free} 
                  onChange={() => {}} 
                  className="accent-emerald-500 mt-0.5"
                />
              </div>

              {/* Allergen Awareness */}
              <div 
                onClick={() => handleToggle('allergen_safe')}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-start justify-between gap-3 ${
                  preferences.allergen_safe 
                    ? 'bg-emerald-500/15 border-emerald-500/40 text-slate-900 dark:text-white' 
                    : 'glass-card border-slate-200 dark:border-white/5 opacity-60'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-1.5 font-bold text-xs">
                    <AlertTriangle className="w-3.5 h-3.5 text-orange-500" />
                    <span>Priority Allergen Alerts</span>
                  </div>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400">
                    Screen for peanuts, tree nuts, soy, shellfish, and sulfites.
                  </p>
                </div>
                <input 
                  type="checkbox" 
                  checked={preferences.allergen_safe} 
                  onChange={() => {}} 
                  className="accent-emerald-500 mt-0.5"
                />
              </div>

            </div>
          </div>

          {/* Nutritional Ceilings & Additive Limits */}
          <div className="glass-card rounded-2xl p-6 border space-y-5">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Sliders className="w-4 h-4 text-emerald-500" />
                <span>Nutritional Threshold Guidelines</span>
              </h2>
              <span className="text-[11px] font-semibold text-emerald-500">Configurable Limits</span>
            </div>

            <div className="space-y-4">
              
              {/* Low Sugar */}
              <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-white/5 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <input 
                      type="checkbox" 
                      id="pref_low_sugar" 
                      checked={preferences.low_sugar} 
                      onChange={() => handleToggle('low_sugar')} 
                      className="accent-emerald-500"
                    />
                    <label htmlFor="pref_low_sugar" className="text-xs font-bold text-slate-900 dark:text-white cursor-pointer">
                      Low Sugar Preference (Max {thresholds.sugar_max}g / 100g)
                    </label>
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-500 border border-emerald-500/30">
                    Source-backed threshold
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">
                  Based on WHO Guidelines & UK Front-of-pack green traffic light criteria. Flags foods with elevated free sugars.
                </p>
              </div>

              {/* Low Sodium */}
              <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-white/5 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <input 
                      type="checkbox" 
                      id="pref_low_sodium" 
                      checked={preferences.low_sodium} 
                      onChange={() => handleToggle('low_sodium')} 
                      className="accent-emerald-500"
                    />
                    <label htmlFor="pref_low_sodium" className="text-xs font-bold text-slate-900 dark:text-white cursor-pointer">
                      Low Sodium Preference (Max {thresholds.sodium_max}mg / 100g)
                    </label>
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-500 border border-emerald-500/30">
                    Source-backed threshold
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">
                  Derived from US FDA 21 CFR §101.61 & ICMR-NIN 2024 Dietary Guidelines for hypertension management.
                </p>
              </div>

              {/* High Protein */}
              <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-white/5 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <input 
                      type="checkbox" 
                      id="pref_high_protein" 
                      checked={preferences.high_protein} 
                      onChange={() => handleToggle('high_protein')} 
                      className="accent-emerald-500"
                    />
                    <label htmlFor="pref_high_protein" className="text-xs font-bold text-slate-900 dark:text-white cursor-pointer">
                      High Protein Density (Min {thresholds.protein_min}g / 100g)
                    </label>
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-500 border border-emerald-500/30">
                    Source-backed threshold
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">
                  FSSAI & EU 'Source of Protein' benchmark criteria for fitness and muscle preservation.
                </p>
              </div>

              {/* Clean Label / Low Additives */}
              <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-white/5 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <input 
                      type="checkbox" 
                      id="pref_low_additives" 
                      checked={preferences.low_additives} 
                      onChange={() => handleToggle('low_additives')} 
                      className="accent-emerald-500"
                    />
                    <label htmlFor="pref_low_additives" className="text-xs font-bold text-slate-900 dark:text-white cursor-pointer">
                      Clean Label & Low Additives (Max {thresholds.additives_max} synthetic additives)
                    </label>
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-500/20 text-slate-400 border border-slate-500/30">
                    Project-defined consumer guideline
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">
                  Flags products containing multiple synthetic colors (INS 102/110), artificial sweeteners, or synthetic antioxidants.
                </p>
              </div>

            </div>
          </div>

        </div>

        {/* Right Column: Live Formulation Simulator (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          
          <div className="glass-card rounded-2xl p-6 border space-y-5 sticky top-24">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-emerald-400" />
                <h2 className="text-base font-bold text-slate-900 dark:text-white">
                  Formulation Suitability Simulator
                </h2>
              </div>
              <button 
                onClick={runSimulator}
                disabled={simLoading}
                className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline cursor-pointer"
              >
                {simLoading ? "Evaluating..." : "Re-evaluate"}
              </button>
            </div>

            <p className="text-xs text-slate-500 dark:text-slate-400">
              Test how custom ingredient and nutritional profiles match against your selected preferences in real time.
            </p>

            {/* Test Inputs */}
            <div className="space-y-3">
              <div>
                <label className="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase">
                  Test Ingredients
                </label>
                <textarea
                  value={simProduct.ingredients}
                  onChange={(e) => setSimProduct({ ...simProduct, ingredients: e.target.value })}
                  rows={3}
                  className="w-full p-2.5 mt-1 rounded-xl glass-card text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-emerald-500/50 font-mono"
                />
              </div>

              <div className="grid grid-cols-3 gap-2">
                <div>
                  <label className="text-[10px] font-bold text-slate-400">Sugar (g/100g)</label>
                  <input
                    type="number"
                    value={simProduct.sugar_g}
                    onChange={(e) => setSimProduct({ ...simProduct, sugar_g: e.target.value })}
                    className="w-full p-2 mt-0.5 rounded-lg glass-card text-xs font-semibold text-slate-900 dark:text-white"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-bold text-slate-400">Sodium (mg/100g)</label>
                  <input
                    type="number"
                    value={simProduct.sodium_mg}
                    onChange={(e) => setSimProduct({ ...simProduct, sodium_mg: e.target.value })}
                    className="w-full p-2 mt-0.5 rounded-lg glass-card text-xs font-semibold text-slate-900 dark:text-white"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-bold text-slate-400">Protein (g/100g)</label>
                  <input
                    type="number"
                    value={simProduct.protein_g}
                    onChange={(e) => setSimProduct({ ...simProduct, protein_g: e.target.value })}
                    className="w-full p-2 mt-0.5 rounded-lg glass-card text-xs font-semibold text-slate-900 dark:text-white"
                  />
                </div>
              </div>
            </div>

            {/* Live Result Output */}
            {simResult && (
              <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-white/5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 dark:text-slate-400">
                    Suitability Verdict:
                  </span>
                  <span className={`text-xs font-bold px-2.5 py-1 rounded-lg ${
                    simResult.verdict === 'SUITABLE' ? 'bg-emerald-500/20 text-emerald-500 border border-emerald-500/30' :
                    'bg-amber-500/20 text-amber-500 border border-amber-500/30'
                  }`}>
                    {simResult.verdict === 'SUITABLE' ? '✓ Suitable for Profile' : '⚠ Preference Concerns'}
                  </span>
                </div>

                <p className="text-xs text-slate-600 dark:text-slate-300">
                  {simResult.summary}
                </p>

                {simResult.concerns && simResult.concerns.length > 0 && (
                  <div className="space-y-1.5 pt-2 border-t border-slate-200 dark:border-white/5">
                    <span className="text-[10px] font-bold text-rose-500 uppercase tracking-wider">
                      Flagged Concerns ({simResult.concerns.length}):
                    </span>
                    <ul className="space-y-1">
                      {simResult.concerns.map((c, i) => (
                        <li key={i} className="text-xs text-slate-700 dark:text-slate-300 flex items-start gap-1.5">
                          <span className="text-amber-500 shrink-0">•</span>
                          <span>{c}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            <div className="p-3 rounded-xl bg-slate-100 dark:bg-slate-800/40 text-[11px] text-slate-500 dark:text-slate-400 flex items-start gap-2">
              <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
              <span>
                Personalized consumer evaluation is purely educational. No individual medical claims or diagnosis are made.
              </span>
            </div>

          </div>

        </div>

      </div>

    </div>
  );
}
