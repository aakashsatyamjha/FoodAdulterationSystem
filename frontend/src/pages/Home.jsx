import React, { useState, useEffect } from 'react';
import { 
  Barcode, 
  FileText, 
  ShieldCheck, 
  ShieldAlert, 
  AlertTriangle, 
  ArrowRight, 
  Database, 
  Cpu, 
  Upload,
  Download,
  CheckCircle2,
  TrendingUp,
  TrendingDown,
  ChevronRight,
  Sparkles,
  Camera,
  Activity,
  Layers,
  Scale,
  Globe,
  UserCheck,
  Sliders,
  HelpCircle,
  ExternalLink
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const RECENT_SCANS = [
  {
    barcode: "8901058852813",
    name: "Maggi 2-Minute Noodles",
    brand: "Nestlé",
    time: "2 min ago",
    method: "Barcode Scan",
    score: 88,
    risk: "Conditional / Country Dependent",
    riskType: "moderate",
    image: "https://images.unsplash.com/photo-1612927601601-6638404737ce?w=120&auto=format&fit=crop&q=60"
  },
  {
    barcode: "7622210817014",
    name: "Oreo Vanilla Cookies",
    brand: "Mondelez",
    time: "15 min ago",
    method: "Barcode Scan",
    score: 48,
    risk: "Moderate Risk",
    riskType: "moderate",
    image: "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?w=120&auto=format&fit=crop&q=60"
  },
  {
    barcode: "8901262010047",
    name: "Amul Pure Cow Ghee 1L",
    brand: "Amul",
    time: "1 hr ago",
    method: "Barcode Scan",
    score: 98,
    risk: "Safe / Low Risk",
    riskType: "low",
    image: "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=120&auto=format&fit=crop&q=60"
  },
  {
    barcode: "9990000000001",
    name: "Adulterated Turmeric Powder",
    brand: "Local Brand",
    time: "2 hrs ago",
    method: "Ingredient OCR",
    score: 12,
    risk: "High Concern (Lead/Metanil)",
    riskType: "high",
    image: "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=120&auto=format&fit=crop&q=60"
  }
];

export default function Home({ setActiveTab, onSelectSample, onOpenChat }) {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    products_scanned_count: 36,
    adulteration_alerts_count: 4,
    high_risk_products_count: 5,
    regulatory_conflicts_count: 39,
    consumer_alerts_count: 14,
    countries_compared_count: 5,
    total_database_ingredients: 39,
    active_ml_model: "Gradient Boosting (99.86% F1)"
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await fetch('/api/dashboard/stats');
      if (res.ok) {
        const data = await res.json();
        setStats(prev => ({ ...prev, ...data }));
      }
    } catch (err) {
      console.log("Stats note:", err);
    }
  };

  const statCards = [
    {
      title: "Products Scanned",
      value: stats.products_scanned_count,
      change: "+12% today",
      isPositive: true,
      icon: Database,
      color: "text-emerald-500",
      bg: "bg-emerald-500/10"
    },
    {
      title: "Adulteration Alerts",
      value: stats.adulteration_alerts_count,
      change: "Chemical & Dye Flags",
      isPositive: false,
      icon: ShieldAlert,
      color: "text-rose-500",
      bg: "bg-rose-500/10"
    },
    {
      title: "High Risk Products",
      value: stats.high_risk_products_count,
      change: "Nutritional & Risk Flags",
      isPositive: false,
      icon: AlertTriangle,
      color: "text-amber-500",
      bg: "bg-amber-500/10"
    },
    {
      title: "Regulatory Conflicts",
      value: stats.regulatory_conflicts_count,
      change: "5 Jurisdictions Tracked",
      isPositive: true,
      icon: Globe,
      color: "text-blue-500",
      bg: "bg-blue-500/10"
    },
    {
      title: "Consumer Alerts",
      value: stats.consumer_alerts_count,
      change: "Profile Preference Matches",
      isPositive: true,
      icon: UserCheck,
      color: "text-teal-500",
      bg: "bg-teal-500/10"
    },
    {
      title: "Countries Compared",
      value: `${stats.countries_compared_count} Nations`,
      change: "IN, US, EU, DE, UK",
      isPositive: true,
      icon: Scale,
      color: "text-purple-500",
      bg: "bg-purple-500/10"
    }
  ];

  return (
    <div className="space-y-6 pb-12 animate-fade-in max-w-7xl mx-auto">
      
      {/* ── Welcome Banner ── */}
      <div className="relative overflow-hidden rounded-3xl glass-card p-6 md:p-8 border border-slate-200/80 dark:border-white/5">
        <div className="absolute -right-16 -top-16 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -left-16 -bottom-16 w-64 h-64 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-bold uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5" />
              <span>FoodGuard 4-Pillar Platform v2.0</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
              Welcome back, {user?.name || "Inspector"}
            </h1>
            <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              Global food safety intelligence combining <strong>Adulteration Screening</strong>, <strong>Risk Assessment</strong>, <strong>Cross-Country Regulatory Compliance</strong> (India, USA, EU, Germany, UK), and <strong>Personalized Consumer Guidance</strong>.
            </p>
          </div>

          <div className="flex flex-wrap gap-3 shrink-0">
            <button
              onClick={() => setActiveTab('barcode')}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition-colors shadow-sm cursor-pointer"
            >
              <Barcode className="w-4 h-4" />
              <span>Scan Barcode</span>
            </button>
            <button
              onClick={() => setActiveTab('ingredient')}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl glass-card hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-900 dark:text-white font-semibold text-xs transition-colors cursor-pointer"
            >
              <FileText className="w-4 h-4 text-emerald-500" />
              <span>Ingredient OCR</span>
            </button>
            <button
              onClick={() => setActiveTab('regulatory')}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl glass-card hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-900 dark:text-white font-semibold text-xs transition-colors cursor-pointer"
            >
              <Globe className="w-4 h-4 text-blue-400" />
              <span>Global Regulatory</span>
            </button>
          </div>
        </div>
      </div>

      {/* ── KPI Metric Cards Grid ── */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
        {statCards.map((card, i) => {
          const Icon = card.icon;
          return (
            <div 
              key={i} 
              className="glass-card rounded-2xl p-4 border border-slate-200/60 dark:border-white/5 space-y-2 hover:translate-y-[-2px] transition-transform duration-200"
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider line-clamp-1">
                  {card.title}
                </span>
                <div className={`p-1.5 rounded-lg ${card.bg} ${card.color}`}>
                  <Icon className="w-3.5 h-3.5" />
                </div>
              </div>
              <div className="text-xl font-extrabold text-slate-900 dark:text-white">
                {card.value}
              </div>
              <p className="text-[10px] text-slate-400 truncate">
                {card.change}
              </p>
            </div>
          );
        })}
      </div>

      {/* ── Global Regulatory Insights Widget ── */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-blue-500/10 via-emerald-500/5 to-teal-500/10 border border-blue-500/25 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-blue-500/20 text-blue-400">
              <Globe className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-white">
                Global Regulatory Intelligence & Cross-Border Insights
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Comparing standards across FSSAI (India), FDA (USA), EFSA (EU), BVL (Germany), and FSA (UK).
              </p>
            </div>
          </div>

          <button
            onClick={() => setActiveTab('regulatory')}
            className="text-xs font-bold text-emerald-600 dark:text-emerald-400 hover:underline flex items-center gap-1 cursor-pointer shrink-0"
          >
            <span>Explore Ingredient Database</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1">
          <div className="p-3 rounded-xl bg-slate-50/80 dark:bg-slate-900/60 border border-slate-200 dark:border-white/5 space-y-0.5">
            <span className="text-[10px] text-slate-400 font-bold uppercase">Indexed Ingredients</span>
            <div className="text-lg font-extrabold text-slate-900 dark:text-white">{stats.total_database_ingredients} Items</div>
            <span className="text-[10px] text-emerald-500">Centralized Seed Dataset</span>
          </div>

          <div className="p-3 rounded-xl bg-slate-50/80 dark:bg-slate-900/60 border border-slate-200 dark:border-white/5 space-y-0.5">
            <span className="text-[10px] text-slate-400 font-bold uppercase">Cross-Border Divergences</span>
            <div className="text-lg font-extrabold text-amber-500">{stats.regulatory_conflicts_count} Additives</div>
            <span className="text-[10px] text-amber-400">Different Legal Limits</span>
          </div>

          <div className="p-3 rounded-xl bg-slate-50/80 dark:bg-slate-900/60 border border-slate-200 dark:border-white/5 space-y-0.5">
            <span className="text-[10px] text-slate-400 font-bold uppercase">Active Machine Learning</span>
            <div className="text-lg font-extrabold text-emerald-500">99.86% F1</div>
            <span className="text-[10px] text-slate-400">Gradient Boosting Top</span>
          </div>

          <div className="p-3 rounded-xl bg-slate-50/80 dark:bg-slate-900/60 border border-slate-200 dark:border-white/5 space-y-0.5">
            <span className="text-[10px] text-slate-400 font-bold uppercase">Consumer Profiles</span>
            <div className="text-lg font-extrabold text-teal-400">9 Parameters</div>
            <span className="text-[10px] text-teal-400">Configurable Guidelines</span>
          </div>
        </div>
      </div>

      {/* ── Recent Scans & Quick Test Samples ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Recent Scans Table (7 cols) */}
        <div className="lg:col-span-7 glass-card rounded-2xl p-6 border border-slate-200/60 dark:border-white/5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-500" />
              <span>Recent Scan Audit Trail</span>
            </h3>
            <button
              onClick={() => setActiveTab('history')}
              className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline cursor-pointer"
            >
              View All History
            </button>
          </div>

          <div className="space-y-2.5">
            {RECENT_SCANS.map((scan, idx) => (
              <div
                key={idx}
                onClick={() => onSelectSample(scan.barcode)}
                className="p-3 rounded-xl bg-slate-50/60 dark:bg-slate-900/40 border border-slate-200/60 dark:border-white/5 hover:border-emerald-500/30 transition-all cursor-pointer flex items-center justify-between gap-3 group"
              >
                <div className="flex items-center gap-3">
                  <img 
                    src={scan.image} 
                    alt={scan.name} 
                    className="w-10 h-10 rounded-lg object-cover shrink-0 border border-slate-200 dark:border-white/10" 
                  />
                  <div>
                    <h4 className="text-xs font-bold text-slate-900 dark:text-white group-hover:text-emerald-500 transition-colors">
                      {scan.name}
                    </h4>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400">
                      {scan.brand} • {scan.time}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                    scan.riskType === 'high' ? 'bg-rose-500/20 text-rose-500 border border-rose-500/30' :
                    scan.riskType === 'moderate' ? 'bg-amber-500/20 text-amber-500 border border-amber-500/30' :
                    'bg-emerald-500/20 text-emerald-500 border border-emerald-500/30'
                  }`}>
                    {scan.risk}
                  </span>
                  <span className="text-xs font-black text-slate-900 dark:text-white">
                    {scan.score}/100
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Launch & Testing Samples (5 cols) */}
        <div className="lg:col-span-5 glass-card rounded-2xl p-6 border border-slate-200/60 dark:border-white/5 space-y-4">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-emerald-400" />
            <span>One-Click Verification Samples</span>
          </h3>

          <p className="text-xs text-slate-500 dark:text-slate-400">
            Click any test sample to trigger the full 4-pillar analysis pipeline:
          </p>

          <div className="space-y-2">
            
            <button
              onClick={() => onSelectSample("8901058852813")}
              className="w-full p-3 rounded-xl bg-slate-50/60 dark:bg-slate-900/40 border border-slate-200/60 dark:border-white/5 hover:border-emerald-500/40 text-left transition-all cursor-pointer flex items-center justify-between"
            >
              <div>
                <div className="text-xs font-bold text-slate-900 dark:text-white">Maggi 2-Minute Noodles</div>
                <div className="text-[11px] text-slate-400">Tests TBHQ, MSG, and palm oil screening</div>
              </div>
              <ArrowRight className="w-4 h-4 text-emerald-500" />
            </button>

            <button
              onClick={() => onSelectSample("9990000000001")}
              className="w-full p-3 rounded-xl bg-rose-500/10 border border-rose-500/25 hover:border-rose-500/50 text-left transition-all cursor-pointer flex items-center justify-between"
            >
              <div>
                <div className="text-xs font-bold text-rose-600 dark:text-rose-400">Adulterated Turmeric Test Case</div>
                <div className="text-[11px] text-rose-500/80">Screens for Lead Chromate & Metanil Yellow</div>
              </div>
              <ArrowRight className="w-4 h-4 text-rose-500" />
            </button>

            <button
              onClick={() => onSelectSample("8901262010047")}
              className="w-full p-3 rounded-xl bg-slate-50/60 dark:bg-slate-900/40 border border-slate-200/60 dark:border-white/5 hover:border-emerald-500/40 text-left transition-all cursor-pointer flex items-center justify-between"
            >
              <div>
                <div className="text-xs font-bold text-slate-900 dark:text-white">Amul Pure Cow Ghee</div>
                <div className="text-[11px] text-slate-400">Clean single-ingredient benchmark (Score: 98/100)</div>
              </div>
              <ArrowRight className="w-4 h-4 text-emerald-500" />
            </button>

            <button
              onClick={() => onSelectSample("7622210817014")}
              className="w-full p-3 rounded-xl bg-slate-50/60 dark:bg-slate-900/40 border border-slate-200/60 dark:border-white/5 hover:border-emerald-500/40 text-left transition-all cursor-pointer flex items-center justify-between"
            >
              <div>
                <div className="text-xs font-bold text-slate-900 dark:text-white">Oreo Vanilla Cream Biscuits</div>
                <div className="text-[11px] text-slate-400">Tests high sugar and emulsifier density</div>
              </div>
              <ArrowRight className="w-4 h-4 text-emerald-500" />
            </button>

          </div>
        </div>

      </div>

      {/* ── Updated Competitive Landscape Matrix ── */}
      <div className="glass-card rounded-2xl p-6 border border-slate-200/60 dark:border-white/5 space-y-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Scale className="w-4 h-4 text-emerald-500" />
            <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
              Competitive Landscape & Market Positioning
            </h3>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            FoodGuard positions uniquely as a <strong>consumer-oriented food safety intelligence platform</strong> connecting ingredient screening, chemical adulteration detection, multi-tier risk assessment, global regulatory comparison (India, US, EU, Germany, UK), and personalized dietary rules.
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-white/10 text-slate-500 dark:text-slate-400 font-bold uppercase tracking-wider text-[10px]">
                <th className="py-2.5 px-3">Platform / System</th>
                <th className="py-2.5 px-3">Reach</th>
                <th className="py-2.5 px-3">Core Focus</th>
                <th className="py-2.5 px-2 text-center">Adulteration</th>
                <th className="py-2.5 px-2 text-center">Risk Scores</th>
                <th className="py-2.5 px-2 text-center">Global Regulatory</th>
                <th className="py-2.5 px-2 text-center">Consumer Rules</th>
                <th className="py-2.5 px-3 text-right">Similarity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-white/5">
              
              {/* FoodGuard AI */}
              <tr className="bg-emerald-500/10 font-bold text-emerald-600 dark:text-emerald-400">
                <td className="py-3 px-3 flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4 text-emerald-500" />
                  <span>FoodGuard AI (This Platform)</span>
                </td>
                <td className="py-3 px-3">India / Global</td>
                <td className="py-3 px-3">4-Pillar Safety + Multi-Criteria AI</td>
                <td className="py-3 px-2 text-center text-emerald-500 font-bold">✓ Dual ML+Rules</td>
                <td className="py-3 px-2 text-center text-emerald-500 font-bold">✓ Multi-Tier</td>
                <td className="py-3 px-2 text-center text-emerald-500 font-bold">✓ 5 Jurisdictions</td>
                <td className="py-3 px-2 text-center text-emerald-500 font-bold">✓ Configurable</td>
                <td className="py-3 px-3 text-right text-emerald-500">Benchmark</td>
              </tr>

              {/* Yuka */}
              <tr className="hover:bg-slate-50/50 dark:hover:bg-slate-800/40">
                <td className="py-2.5 px-3 font-semibold text-slate-900 dark:text-white">Yuka</td>
                <td className="py-2.5 px-3 text-slate-400">Europe / US</td>
                <td className="py-2.5 px-3 text-slate-400">Consumer Additives & Nutri-Score</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✕ No ML Screen</td>
                <td className="py-2.5 px-2 text-center text-emerald-500 font-bold">✓ Additive Matrix</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✕ Single Region</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✕ Fixed Rules</td>
                <td className="py-2.5 px-3 text-right text-slate-400">Moderate</td>
              </tr>

              {/* Open Food Facts */}
              <tr className="hover:bg-slate-50/50 dark:hover:bg-slate-800/40">
                <td className="py-2.5 px-3 font-semibold text-slate-900 dark:text-white">Open Food Facts</td>
                <td className="py-2.5 px-3 text-slate-400">Global Open DB</td>
                <td className="py-2.5 px-3 text-slate-400">Crowdsourced Nutritional DB</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✕ No Adulteration</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✓ Nutri-Score/NOVA</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✕ No Comparative</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✕ Basic Filters</td>
                <td className="py-2.5 px-3 text-right text-slate-400">Data Source</td>
              </tr>

              {/* Inextrac / Trustwell */}
              <tr className="hover:bg-slate-50/50 dark:hover:bg-slate-800/40">
                <td className="py-2.5 px-3 font-semibold text-slate-900 dark:text-white">Genesis R&D / Trustwell</td>
                <td className="py-2.5 px-3 text-slate-400">Enterprise B2B</td>
                <td className="py-2.5 px-3 text-slate-400">B2B Regulatory Label Compliance</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✕ Enterprise Spec</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✓ Formulation B2B</td>
                <td className="py-2.5 px-2 text-center text-emerald-500 font-bold">✓ Heavy B2B</td>
                <td className="py-2.5 px-2 text-center text-slate-400">✕ Enterprise Only</td>
                <td className="py-2.5 px-3 text-right text-slate-400">Low (B2B Tool)</td>
              </tr>

            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
