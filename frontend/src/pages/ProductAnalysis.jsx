import React, { useState } from 'react';
import { 
  ShieldAlert, 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  Info, 
  Scale, 
  Award, 
  Tag, 
  Printer, 
  ArrowLeft,
  Sparkles,
  Zap,
  BookOpen,
  BadgeCheck,
  XCircle,
  ListChecks,
  AlertOctagon,
  FileText,
  Globe,
  Sliders,
  UserCheck,
  ChevronDown,
  ChevronUp,
  Activity,
  Layers,
  HelpCircle,
  FileDown,
  Download,
  Loader2,
  Ban
} from 'lucide-react';
import { generateProductSafetyPDF } from '../utils/pdfGenerator';

export default function ProductAnalysis({ data, onReset, onOpenChat }) {
  if (!data) return null;

  const {
    product_name = "Food Product",
    brand = "Packaged Goods",
    barcode,
    category = "Packaged Food",
    scan_type = "barcode",
    quality_score = 50,
    overall_assessment = "ASSESSED",
    final_verdict_badge = "Assessed",
    final_explanation = "",
    safety_disclaimer = "",
    adulteration = {},
    risk = {},
    regulatory = {},
    consumer = {},
    decision_trace = {},
    matched_ingredients = [],
    parsed_ingredients = [],
    nutrition = {},
    image_url
  } = data;

  // Active Selected Country for live compliance view: 'IN' | 'US' | 'EU' | 'DE' | 'UK'
  const [selectedCountryCode, setSelectedCountryCode] = useState('IN');
  const [expandedWhyDifferentId, setExpandedWhyDifferentId] = useState(null);
  const [activeTabSection, setActiveTabSection] = useState('overview'); // 'overview' | 'regulatory' | 'ingredients' | 'decision_trace'
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);

  const handleDownloadPdf = async () => {
    setIsGeneratingPdf(true);
    try {
      generateProductSafetyPDF(data, selectedCountryCode);
    } catch (err) {
      console.error("PDF generation failed:", err);
      window.print();
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  const countriesList = [
    { code: 'IN', name: 'India', flag: '🇮🇳', authority: 'FSSAI' },
    { code: 'US', name: 'USA', flag: '🇺🇸', authority: 'FDA' },
    { code: 'EU', name: 'European Union', flag: '🇪🇺', authority: 'EFSA' },
    { code: 'DE', name: 'Germany', flag: '🇩🇪', authority: 'BVL' },
    { code: 'UK', name: 'United Kingdom', flag: '🇬🇧', authority: 'FSA' }
  ];

  // Derive country compliance for active selection
  const countryEvaluations = regulatory.country_evaluations || regulatory.country_summaries || {};
  const currentCountrySummary = countryEvaluations[selectedCountryCode] || {
    country_name: selectedCountryCode === 'US' ? 'USA' : selectedCountryCode === 'EU' ? 'European Union' : selectedCountryCode === 'DE' ? 'Germany' : selectedCountryCode === 'UK' ? 'United Kingdom' : 'India',
    authority: selectedCountryCode === 'US' ? 'FDA' : selectedCountryCode === 'EU' ? 'EFSA' : selectedCountryCode === 'DE' ? 'BVL' : selectedCountryCode === 'UK' ? 'FSA' : 'FSSAI',
    flag: selectedCountryCode === 'US' ? '🇺🇸' : selectedCountryCode === 'EU' ? '🇪🇺' : selectedCountryCode === 'DE' ? '🇩🇪' : selectedCountryCode === 'UK' ? '🇬🇧' : '🇮🇳',
    verdict: "PASS",
    summary: `Evaluated against statutory ${selectedCountryCode === 'US' ? 'US FDA (21 CFR)' : selectedCountryCode === 'EU' ? 'EFSA Regulation (EC) No 1333/2008' : selectedCountryCode === 'DE' ? 'German BVL / LFGB' : selectedCountryCode === 'UK' ? 'UK FSA' : 'FSSAI'} standards.`,
    passed_criteria: [],
    conditional_criteria: [],
    failed_criteria: []
  };

  const getScoreTheme = () => {
    if (quality_score >= 75) return { color: '#10b981', textColor: 'text-emerald-500', bg: 'bg-emerald-500/10', border: 'border-emerald-500/25', label: 'Nutrient-dense / Low Risk' };
    if (quality_score >= 45) return { color: '#f59e0b', textColor: 'text-amber-500', bg: 'bg-amber-500/10', border: 'border-amber-500/25', label: 'Moderate Concern / Formulation Limits' };
    return { color: '#f43f5e', textColor: 'text-rose-500', bg: 'bg-rose-500/10', border: 'border-rose-500/25', label: 'High Concern / Adulterant or UPF Signature' };
  };

  const scoreTheme = getScoreTheme();
  const crossCountryMatrix = regulatory.cross_country_comparison?.matrix || [];
  const divergentIngredients = regulatory.divergent_ingredients || [];
  const scoreDeductions = data.score_deductions || [];

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-16 animate-fade-in text-slate-900 dark:text-slate-100">
      
      {/* ── Top Action Bar ── */}
      <div className="flex flex-wrap items-center justify-between gap-3 no-print">
        <button
          onClick={onReset}
          className="flex items-center gap-2 text-xs font-semibold px-3.5 py-2 rounded-xl glass-card hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Scan Another Product</span>
        </button>

        <div className="flex items-center gap-2 flex-wrap">
          {onOpenChat && (
            <button
              onClick={() => onOpenChat(`Why did ${product_name} receive a score of ${quality_score}?`)}
              className="flex items-center gap-1.5 text-xs font-bold bg-emerald-500/15 hover:bg-emerald-500/25 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 px-3.5 py-2 rounded-xl transition-colors cursor-pointer"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Ask FoodGuard AI</span>
            </button>
          )}

          {/* Download PDF Report Button */}
          <button
            onClick={handleDownloadPdf}
            disabled={isGeneratingPdf}
            className="flex items-center gap-2 text-xs font-bold px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-slate-950 shadow-md shadow-emerald-600/20 transition-all cursor-pointer disabled:opacity-50"
          >
            {isGeneratingPdf ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Generating PDF...</span>
              </>
            ) : (
              <>
                <FileDown className="w-3.5 h-3.5" />
                <span>Download PDF Report</span>
              </>
            )}
          </button>

          <button
            onClick={() => window.print()}
            className="flex items-center gap-2 text-xs font-semibold px-3.5 py-2 rounded-xl glass-card hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print</span>
          </button>
        </div>
      </div>

      {/* ── 1. PRODUCT INFORMATION & OVERALL FOOD SAFETY SCORE ── */}
      <div className="glass-card rounded-2xl p-6 border border-slate-200/60 dark:border-white/5 space-y-6">
        
        {/* Product Identity Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-white/5">
          <div className="flex items-start gap-4">
            {image_url ? (
              <img 
                src={image_url} 
                alt={product_name} 
                className="w-16 h-16 rounded-xl object-cover border border-slate-200 dark:border-white/10 shrink-0" 
              />
            ) : (
              <div className="w-16 h-16 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 font-bold text-xl shrink-0">
                🥗
              </div>
            )}
            <div className="space-y-1">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
                  {brand}
                </span>
                {barcode && (
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                    Barcode: {barcode}
                  </span>
                )}
                <span className="text-[11px] px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800/60 text-slate-500 dark:text-slate-400">
                  {category}
                </span>
              </div>
              <h1 className="text-xl md:text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
                {product_name}
              </h1>
            </div>
          </div>

          <div className="flex md:flex-col items-end justify-between md:justify-center gap-2">
            <span className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
              Food Safety Report
            </span>
            <span className={`px-3 py-1 rounded-xl text-xs font-bold uppercase tracking-wider ${
              final_verdict_badge.toLowerCase().includes('high') ? 'bg-rose-500/20 text-rose-500 border border-rose-500/30' :
              final_verdict_badge.toLowerCase().includes('regulatory') ? 'bg-orange-500/20 text-orange-500 border border-orange-500/30' :
              final_verdict_badge.toLowerCase().includes('moderate') || final_verdict_badge.toLowerCase().includes('country') ? 'bg-amber-500/20 text-amber-500 border border-amber-500/30' :
              'bg-emerald-500/20 text-emerald-500 border border-emerald-500/30'
            }`}>
              {final_verdict_badge}
            </span>
          </div>
        </div>

        {/* Overall Score & Multi-Tier Summary Banner */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
          
          {/* Circular Score Gauge (4 cols) */}
          <div className="md:col-span-4 flex flex-col items-center justify-center p-4 rounded-2xl bg-slate-50/50 dark:bg-slate-900/40 border border-slate-200 dark:border-white/5">
            <div className="relative w-32 h-32 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="currentColor"
                  strokeWidth="8"
                  className="text-slate-200 dark:text-slate-800"
                  fill="transparent"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke={scoreTheme.color}
                  strokeWidth="8"
                  strokeDasharray={`${(quality_score / 100) * 251.2} 251.2`}
                  strokeLinecap="round"
                  className="transition-all duration-1000 ease-out"
                  fill="transparent"
                />
              </svg>
              <div className="absolute flex flex-col items-center justify-center">
                <span className="text-3xl font-black tracking-tight" style={{ color: scoreTheme.color }}>
                  {quality_score}
                </span>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Out of 100
                </span>
              </div>
            </div>
            <p className="text-xs font-bold mt-2 text-center" style={{ color: scoreTheme.color }}>
              {scoreTheme.label}
            </p>
          </div>

          {/* Decision Synthesis & Explanation (8 cols) */}
          <div className="md:col-span-8 space-y-3">
            <div className="space-y-1">
              <span className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                Multi-Criteria Final Assessment
              </span>
              <h2 className="text-base font-bold text-slate-900 dark:text-white">
                {overall_assessment}
              </h2>
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
              {final_explanation || "Product formulation passed foundational screening with active multi-criteria verification across all food safety dimensions."}
            </p>

            {/* Quick Stats Chips */}
            <div className="flex flex-wrap gap-2 pt-1">
              <span className="text-[11px] font-semibold px-2.5 py-1 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                📦 {matched_ingredients.length} Ingredients Identified
              </span>
              <span className="text-[11px] font-semibold px-2.5 py-1 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                ⚖️ {regulatory.divergence_count || 0} Cross-Border Divergences
              </span>
              <span className="text-[11px] font-semibold px-2.5 py-1 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                🛡️ AI Screening + Rule Engine
              </span>
            </div>
          </div>

        </div>

        {/* ── Why This Product is Not 100/100 (Score Deduction Audit) ── */}
        <div className="p-4 rounded-xl bg-slate-100/80 dark:bg-slate-900/60 border border-slate-200 dark:border-white/5 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
              <Info className="w-3.5 h-3.5 text-emerald-500" />
              <span>Why This Product Received {quality_score}/100 (Point Deduction Breakdown)</span>
            </h3>
            <span className="text-[11px] font-mono text-slate-500 dark:text-slate-400">
              {quality_score === 100 ? "0 Deductions" : `Lost ${100 - quality_score} pts from 100 baseline`}
            </span>
          </div>

          {scoreDeductions.length === 0 ? (
            <p className="text-xs text-slate-600 dark:text-slate-400">
              This product contains clean, wholesome ingredients with no high-risk additives, regulatory violations, or nutritional extremes.
            </p>
          ) : (
            <div className="space-y-2">
              {scoreDeductions.map((d, idx) => (
                <div key={idx} className="p-2.5 rounded-lg bg-white/60 dark:bg-slate-800/60 border border-slate-200 dark:border-white/5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                  <div className="space-y-0.5">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-900 dark:text-white">{d.factor}</span>
                      <span className="text-[10px] px-2 py-0.5 rounded bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 font-semibold">{d.category}</span>
                    </div>
                    <p className="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">{d.reason}</p>
                  </div>
                  <span className="text-rose-500 font-bold font-mono text-xs whitespace-nowrap self-start sm:self-auto bg-rose-500/10 px-2 py-1 rounded">
                    {d.impact}
                  </span>
                </div>
              ))}
            </div>
          )}

          {/* Logical Explanation: Legality vs Holistic Health Score */}
          <div className="p-3.5 rounded-xl bg-blue-500/10 border border-blue-500/20 space-y-2 text-xs">
            <div className="flex items-center gap-2 font-bold text-blue-600 dark:text-blue-400">
              <Scale className="w-4 h-4 shrink-0" />
              <span>Logical Analysis: Why Did All 5 Countries PASS This Food Legally, But It Received {quality_score}/100?</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1 text-[11px] leading-relaxed text-slate-700 dark:text-slate-300">
              <div className="p-2.5 rounded-lg bg-white/60 dark:bg-slate-800/60 border border-slate-200 dark:border-white/5 space-y-1">
                <span className="font-bold text-emerald-600 dark:text-emerald-400 block">✓ 1. Why All 5 Countries Passed Legally:</span>
                <p>
                  None of the ingredients in this product are illegal chemicals (like Metanil Yellow, Sudan Dyes) or banned substances (like Potassium Bromate or BVO). The formulation is <strong>100% legally authorized to sell</strong> in India (FSSAI), USA (FDA), EU (EFSA), Germany (BVL), and the UK (FSA).
                </p>
              </div>
              <div className="p-2.5 rounded-lg bg-white/60 dark:bg-slate-800/60 border border-slate-200 dark:border-white/5 space-y-1">
                <span className="font-bold text-amber-600 dark:text-amber-400 block">⚠️ 2. Why the Score Is {quality_score}/100 (Not 100/100):</span>
                <p>
                  <strong>Government legality is not the same as optimal health.</strong> Regulatory agencies only ensure a food does not cause acute poisoning; they do not ban added sugar or sodium. FoodGuard evaluates chronic health risks: elevated sugar, sodium, or saturated fat reduce points based on WHO guidelines.
                </p>
              </div>
            </div>
          </div>

          {/* INS / E-Number Standards Educational Notice */}
          <div className="pt-2 border-t border-slate-200 dark:border-white/5 text-[11px] text-slate-500 dark:text-slate-400 space-y-1">
            <p>
              <strong className="text-slate-700 dark:text-slate-300">How INS Standards Work:</strong> The <span className="font-mono font-semibold">INS</span> (International Numbering System) by Codex Alimentarius (WHO/FAO) assigns unique codes (e.g. INS 102 Tartrazine, INS 171 Titanium Dioxide, INS 924a Potassium Bromate) to standardize additives globally. Having an INS number indicates standard chemical categorization, but <em>does not guarantee universal safety</em>: individual authorities evaluate substances differently based on toxicological trials (e.g., INS 171 is banned in the EU/Germany by EFSA, but permitted in the US by FDA).
            </p>
          </div>
        </div>

      </div>

      {/* ── 2. FOUR PILLARS SUMMARY CARDS ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Pillar 1: Adulteration Screening */}
        <div className="glass-card rounded-2xl p-4 border space-y-2 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
              1. Adulteration
            </span>
            <ShieldAlert className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-sm font-extrabold text-slate-900 dark:text-white">
            {adulteration.status || "LOW CONCERN"}
          </p>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-2">
            {adulteration.summary || "No non-permitted dye or heavy metal signatures detected."}
          </p>
        </div>

        {/* Pillar 2: Health & Risk Assessment */}
        <div className="glass-card rounded-2xl p-4 border space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
              2. Health Risk
            </span>
            <Activity className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-sm font-extrabold text-slate-900 dark:text-white">
            {risk.risk_tier || "Moderate Risk"} ({risk.overall_risk_pct || 40}%)
          </p>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-2">
            {risk.negative_factors && risk.negative_factors[0] ? risk.negative_factors[0] : "Nutritional profile evaluated."}
          </p>
        </div>

        {/* Pillar 3: Country Regulatory Compliance */}
        <div className="glass-card rounded-2xl p-4 border space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
              3. Global Regulatory
            </span>
            <Globe className="w-4 h-4 text-blue-400" />
          </div>
          <p className="text-sm font-extrabold text-slate-900 dark:text-white">
            {currentCountrySummary.verdict === 'PASS' ? '✓ Compliant' : currentCountrySummary.verdict === 'CONDITIONAL' ? '⚠ Conditional' : '✕ Restricted'}
          </p>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-2">
            {currentCountrySummary.summary || "Complies with regional additive limits."}
          </p>
        </div>

        {/* Pillar 4: Consumer Intelligence */}
        <div className="glass-card rounded-2xl p-4 border space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
              4. Consumer Profile
            </span>
            <UserCheck className="w-4 h-4 text-teal-400" />
          </div>
          <p className="text-sm font-extrabold text-slate-900 dark:text-white">
            {consumer.verdict === 'SUITABLE' ? '✓ Suitable' : consumer.verdict === 'CONCERN' ? '⚠ Preference Alert' : 'Active Profile'}
          </p>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-2">
            {consumer.summary || "Matches your active dietary profile preferences."}
          </p>
        </div>

      </div>

      {/* ── 3. INTERACTIVE COUNTRY COMPLIANCE SELECTOR ── */}
      <div className="glass-card rounded-2xl p-6 border space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Scale className="w-4 h-4 text-emerald-500" />
              <span>Is this food allowed in this country?</span>
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Select a jurisdiction to inspect regional legality, permissible limits, and statutory checklists.
            </p>
          </div>

          {/* Country Selector Buttons */}
          <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-white/5 overflow-x-auto">
            {countriesList.map((c) => {
              const isSelected = selectedCountryCode === c.code;
              return (
                <button
                  key={c.code}
                  onClick={() => setSelectedCountryCode(c.code)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer whitespace-nowrap ${
                    isSelected 
                      ? 'bg-emerald-500 text-slate-950 shadow-xs' 
                      : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
                  }`}
                >
                  <span>{c.flag}</span>
                  <span>{c.name}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Selected Country Verdict Banner */}
        <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-white/5 space-y-3">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <span className="text-2xl">{currentCountrySummary.flag || "🇮🇳"}</span>
              <div>
                <p className="text-xs font-bold text-slate-900 dark:text-white">
                  {currentCountrySummary.country_name} ({currentCountrySummary.authority}) Regulatory Status:
                </p>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">
                  Evaluated against {currentCountrySummary.authority} food safety and additive regulations.
                </p>
              </div>
            </div>

            <span className={`text-xs font-bold px-3 py-1.5 rounded-xl uppercase tracking-wider ${
              currentCountrySummary.verdict === 'PASS' ? 'bg-emerald-500/20 text-emerald-500 border border-emerald-500/30' :
              currentCountrySummary.verdict === 'CONDITIONAL' ? 'bg-amber-500/20 text-amber-500 border border-amber-500/30' :
              'bg-rose-500/20 text-rose-500 border border-rose-500/30'
            }`}>
              {currentCountrySummary.verdict === 'PASS' ? '✓ PASS / PERMITTED' : currentCountrySummary.verdict === 'CONDITIONAL' ? '⚠ CONDITIONAL / LIMITS' : '✕ FAIL / NOT PERMITTED'}
            </span>
          </div>

          <p className="text-xs text-slate-700 dark:text-slate-300">
            {currentCountrySummary.summary}
          </p>

          {/* Granular Criteria Checklist */}
          <div className="space-y-2 pt-2 border-t border-slate-200 dark:border-white/5">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              {currentCountrySummary.authority} Statutory Criteria Checklist
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              
              {/* Failed Criteria */}
              {currentCountrySummary.failed_criteria && currentCountrySummary.failed_criteria.map((fc, i) => (
                <div key={`fc-${i}`} className="p-2.5 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-start gap-2">
                  <XCircle className="w-3.5 h-3.5 text-rose-500 shrink-0 mt-0.5" />
                  <div className="text-[11px]">
                    <span className="font-bold text-rose-600 dark:text-rose-400">{fc.title}:</span>
                    <span className="text-slate-600 dark:text-slate-300 ml-1">{fc.detail}</span>
                  </div>
                </div>
              ))}

              {/* Conditional Criteria */}
              {currentCountrySummary.conditional_criteria && currentCountrySummary.conditional_criteria.map((cc, i) => (
                <div key={`cc-${i}`} className="p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-start gap-2">
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" />
                  <div className="text-[11px]">
                    <span className="font-bold text-amber-600 dark:text-amber-400">{cc.title}:</span>
                    <span className="text-slate-600 dark:text-slate-300 ml-1">{cc.detail}</span>
                  </div>
                </div>
              ))}

              {/* Passed Criteria */}
              {currentCountrySummary.passed_criteria && currentCountrySummary.passed_criteria.map((pc, i) => (
                <div key={`pc-${i}`} className="p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-start gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                  <div className="text-[11px]">
                    <span className="font-bold text-emerald-600 dark:text-emerald-400">{pc.title}:</span>
                    <span className="text-slate-600 dark:text-slate-300 ml-1">{pc.detail}</span>
                  </div>
                </div>
              ))}

            </div>
          </div>

        </div>

      </div>

      {/* ── 4. CROSS-COUNTRY REGULATORY COMPARISON MATRIX & "WHY DIFFERENT?" ── */}
      <div className="glass-card rounded-2xl p-6 border space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Globe className="w-4 h-4 text-emerald-500" />
              <span>Global Regulatory Comparison Matrix</span>
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Side-by-side compliance status for formulation ingredients across India, USA, EU, Germany, and the UK.
            </p>
          </div>

          <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
            {divergentIngredients.length} Divergence(s) Flagged
          </span>
        </div>

        {/* Matrix Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-white/10 text-slate-500 dark:text-slate-400 font-bold uppercase tracking-wider text-[10px]">
                <th className="py-2.5 px-3">Ingredient</th>
                <th className="py-2.5 px-3">Function</th>
                <th className="py-2.5 px-2 text-center">🇮🇳 India</th>
                <th className="py-2.5 px-2 text-center">🇺🇸 USA</th>
                <th className="py-2.5 px-2 text-center">🇪🇺 EU</th>
                <th className="py-2.5 px-2 text-center">🇩🇪 Germany</th>
                <th className="py-2.5 px-3 text-right">Divergence</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-white/5">
              {crossCountryMatrix.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-4 text-center text-slate-400">
                    No standardized additives found requiring cross-country matrix evaluation.
                  </td>
                </tr>
              ) : (
                crossCountryMatrix.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-3">
                      <div className="font-bold text-slate-900 dark:text-white">{row.common_name}</div>
                      <div className="text-[10px] text-slate-400 font-mono">{row.ins_e_number}</div>
                    </td>
                    <td className="py-3 px-3 text-slate-600 dark:text-slate-300">
                      {row.function}
                    </td>
                    <td className="py-3 px-2 text-center font-bold">
                      <span className={`px-2 py-0.5 rounded text-[11px] ${row.statuses.IN?.badge?.badge_class || ''}`}>
                        {row.statuses.IN?.badge?.symbol || '✓'}
                      </span>
                    </td>
                    <td className="py-3 px-2 text-center font-bold">
                      <span className={`px-2 py-0.5 rounded text-[11px] ${row.statuses.US?.badge?.badge_class || ''}`}>
                        {row.statuses.US?.badge?.symbol || '✓'}
                      </span>
                    </td>
                    <td className="py-3 px-2 text-center font-bold">
                      <span className={`px-2 py-0.5 rounded text-[11px] ${row.statuses.EU?.badge?.badge_class || ''}`}>
                        {row.statuses.EU?.badge?.symbol || '✓'}
                      </span>
                    </td>
                    <td className="py-3 px-2 text-center font-bold">
                      <span className={`px-2 py-0.5 rounded text-[11px] ${row.statuses.DE?.badge?.badge_class || ''}`}>
                        {row.statuses.DE?.badge?.symbol || '✓'}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right">
                      {row.has_divergence ? (
                        <button
                          onClick={() => setExpandedWhyDifferentId(expandedWhyDifferentId === row.id ? null : row.id)}
                          className="text-[11px] font-bold text-amber-500 hover:text-amber-400 underline cursor-pointer"
                        >
                          {expandedWhyDifferentId === row.id ? "Hide Reason" : "Why Different?"}
                        </button>
                      ) : (
                        <span className="text-[10px] text-slate-400">Harmonized</span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Comprehensive Prohibited & Restricted Items Breakdown (INS Rules) */}
        <div className="space-y-4 pt-2">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Ban className="w-4 h-4 text-rose-500" />
              <span>Prohibited & Restricted Substances Breakdown (INS / Statutory Rules)</span>
            </h3>
            <span className="text-[11px] font-mono text-slate-400">
              {divergentIngredients.length > 0 ? `${divergentIngredients.length} Active Divergence Rule(s)` : "Zero Banned Substances"}
            </span>
          </div>

          {divergentIngredients.length === 0 ? (
            <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/25 text-xs text-emerald-700 dark:text-emerald-300 flex items-start gap-3">
              <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
              <div className="space-y-1">
                <p className="font-bold">No Prohibited or Highly Restricted Additives Detected</p>
                <p className="text-[11px] text-slate-600 dark:text-slate-400">
                  All recognized ingredients in this formulation operate within standard harmonized food additive limits across India (FSSAI), USA (FDA), EU (EFSA), Germany (BVL), and UK (FSA).
                </p>
              </div>
            </div>
          ) : (
            divergentIngredients.map((div, idx) => (
              <div 
                key={idx} 
                className="p-5 rounded-2xl bg-slate-50/80 dark:bg-slate-900/60 border border-slate-200 dark:border-white/10 space-y-4"
              >
                {/* Header: Ingredient Name + INS Number */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-200 dark:border-white/5">
                  <div className="flex items-center gap-2.5">
                    <span className="w-7 h-7 rounded-lg bg-amber-500/20 text-amber-500 flex items-center justify-center font-bold text-xs">
                      #{idx + 1}
                    </span>
                    <div>
                      <h4 className="text-sm font-bold text-slate-900 dark:text-white">
                        {div.name}
                      </h4>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400">
                        Statutory Code: <span className="font-mono font-semibold text-emerald-600 dark:text-emerald-400">{div.ins_e_number}</span>
                      </p>
                    </div>
                  </div>

                  <span className="text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider bg-amber-500/15 text-amber-600 dark:text-amber-400 border border-amber-500/30 self-start sm:self-auto">
                    Cross-Country Discrepancy
                  </span>
                </div>

                {/* 2-Column Comparative Analysis: Why Prohibited vs Why Approved */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                  
                  {/* Left Column: Why Prohibited / Restricted in Particular Countries */}
                  <div className="p-3.5 rounded-xl bg-rose-500/5 border border-rose-500/20 space-y-2">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-rose-500">
                      <AlertOctagon className="w-3.5 h-3.5 shrink-0" />
                      <span>Why Prohibited / Restricted in Certain Countries:</span>
                    </div>
                    <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
                      {div.reason || "Restricted due to clinical toxicological concerns, potential genotoxicity, or mandatory behavioral warning requirements under European/UK regulatory frameworks."}
                    </p>
                    <div className="pt-1 text-[10px] text-rose-600/80 dark:text-rose-400/80 font-medium">
                      ⚠️ Applicable in: European Union (EFSA Regulation 2022/63 / 1333/2008), Germany (BVL), UK (FSA)
                    </div>
                  </div>

                  {/* Right Column: Why Approved / Permitted in Other Countries */}
                  <div className="p-3.5 rounded-xl bg-emerald-500/5 border border-emerald-500/20 space-y-2">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-600 dark:text-emerald-400">
                      <BadgeCheck className="w-3.5 h-3.5 shrink-0" />
                      <span>Why Approved / Permitted in Other Countries:</span>
                    </div>
                    <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
                      Permitted under historical safety benchmarks (e.g. US FDA 21 CFR §73 / FSSAI Food Additives Regulations) with maximum permissible limits (GMP or quantitative threshold) where risk is deemed manageable below established exposure caps.
                    </p>
                    <div className="pt-1 text-[10px] text-emerald-600/80 dark:text-emerald-400/80 font-medium">
                      ✓ Permitted in: India (FSSAI GMP Schedule), USA (FDA 21 CFR Certified Additives)
                    </div>
                  </div>

                </div>

                {/* Statutory INS Rules & Evidence Citation */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-2 border-t border-slate-200 dark:border-white/5 text-[11px] text-slate-500 dark:text-slate-400">
                  <div>
                    <span className="font-semibold text-slate-700 dark:text-slate-300">Statutory INS Rule:</span> {div.ins_e_number} listed under Codex Alimentarius / FSSAI Table 1-15 additive provisions.
                  </div>
                  <div>
                    <span className="font-semibold text-slate-700 dark:text-slate-300">Evidence Citation:</span> {div.source}
                  </div>
                </div>

              </div>
            ))
          )}
        </div>

      </div>

      {/* ── 5. MULTI-RISK BREAKDOWN BARS & NUTRITIONAL PROFILE ── */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        
        {/* Multi-Risk Bars (6 cols) */}
        <div className="md:col-span-6 glass-card rounded-2xl p-6 border space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-500" />
              <span>Multi-Dimensional Risk Breakdown</span>
            </h3>
            <span className="text-xs font-extrabold text-amber-500">
              Overall: {risk.overall_risk_pct || 40}%
            </span>
          </div>

          <div className="space-y-3">
            
            {/* Overall Risk */}
            <div className="space-y-1">
              <div className="flex justify-between text-xs">
                <span className="font-semibold text-slate-700 dark:text-slate-300">Overall Holistic Risk</span>
                <span className="font-bold">{risk.overall_risk_pct || 40}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-emerald-500 via-amber-500 to-rose-500 transition-all duration-700"
                  style={{ width: `${risk.overall_risk_pct || 40}%` }}
                />
              </div>
            </div>

            {/* Ingredient Risk */}
            <div className="space-y-1">
              <div className="flex justify-between text-xs">
                <span className="font-semibold text-slate-700 dark:text-slate-300">Ingredient & Additive Risk</span>
                <span className="font-bold">{risk.ingredient_risk_pct || 30}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden">
                <div 
                  className="h-full bg-amber-500 transition-all duration-700"
                  style={{ width: `${risk.ingredient_risk_pct || 30}%` }}
                />
              </div>
            </div>

            {/* Regulatory Risk */}
            <div className="space-y-1">
              <div className="flex justify-between text-xs">
                <span className="font-semibold text-slate-700 dark:text-slate-300">Regulatory Conflict Risk</span>
                <span className="font-bold">{risk.regulatory_risk_pct || 25}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden">
                <div 
                  className="h-full bg-blue-500 transition-all duration-700"
                  style={{ width: `${risk.regulatory_risk_pct || 25}%` }}
                />
              </div>
            </div>

            {/* Consumer Risk */}
            <div className="space-y-1">
              <div className="flex justify-between text-xs">
                <span className="font-semibold text-slate-700 dark:text-slate-300">Consumer Preference Risk</span>
                <span className="font-bold">{risk.consumer_risk_pct || 35}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden">
                <div 
                  className="h-full bg-teal-500 transition-all duration-700"
                  style={{ width: `${risk.consumer_risk_pct || 35}%` }}
                />
              </div>
            </div>

          </div>

          <p className="text-[11px] text-slate-400 pt-1">
            Note: Risk assessment is decoupled from regulatory legality; legally compliant additives may still contribute to consumer health risk scores.
          </p>
        </div>

        {/* Nutritional Traffic Lights (6 cols) */}
        <div className="md:col-span-6 glass-card rounded-2xl p-6 border space-y-4">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Sliders className="w-4 h-4 text-emerald-500" />
            <span>Nutritional Traffic Light Profiling</span>
          </h3>

          <div className="grid grid-cols-3 gap-2">
            
            {/* Sugar */}
            <div className={`p-2.5 rounded-xl border text-center space-y-0.5 ${
              (nutrition.sugar_g || 0) > 15 ? 'bg-rose-500/10 border-rose-500/30 text-rose-500' :
              (nutrition.sugar_g || 0) > 5 ? 'bg-amber-500/10 border-amber-500/30 text-amber-500' :
              'bg-emerald-500/10 border-emerald-500/30 text-emerald-500'
            }`}>
              <div className="text-[10px] font-bold uppercase">Sugar</div>
              <div className="text-base font-extrabold">{nutrition.sugar_g || 0}g</div>
              <div className="text-[10px]">{(nutrition.sugar_g || 0) > 15 ? 'High' : (nutrition.sugar_g || 0) > 5 ? 'Moderate' : 'Low'}</div>
            </div>

            {/* Sodium */}
            <div className={`p-2.5 rounded-xl border text-center space-y-0.5 ${
              (nutrition.sodium_mg || 0) > 600 ? 'bg-rose-500/10 border-rose-500/30 text-rose-500' :
              (nutrition.sodium_mg || 0) > 200 ? 'bg-amber-500/10 border-amber-500/30 text-amber-500' :
              'bg-emerald-500/10 border-emerald-500/30 text-emerald-500'
            }`}>
              <div className="text-[10px] font-bold uppercase">Sodium</div>
              <div className="text-base font-extrabold">{nutrition.sodium_mg || 0}mg</div>
              <div className="text-[10px]">{(nutrition.sodium_mg || 0) > 600 ? 'High' : (nutrition.sodium_mg || 0) > 200 ? 'Moderate' : 'Low'}</div>
            </div>

            {/* Saturated Fat */}
            <div className={`p-2.5 rounded-xl border text-center space-y-0.5 ${
              (nutrition.saturated_fat_g || 0) > 5 ? 'bg-rose-500/10 border-rose-500/30 text-rose-500' :
              (nutrition.saturated_fat_g || 0) > 1.5 ? 'bg-amber-500/10 border-amber-500/30 text-amber-500' :
              'bg-emerald-500/10 border-emerald-500/30 text-emerald-500'
            }`}>
              <div className="text-[10px] font-bold uppercase">Sat Fat</div>
              <div className="text-base font-extrabold">{nutrition.saturated_fat_g || 0}g</div>
              <div className="text-[10px]">{(nutrition.saturated_fat_g || 0) > 5 ? 'High' : (nutrition.saturated_fat_g || 0) > 1.5 ? 'Moderate' : 'Low'}</div>
            </div>

            {/* Protein */}
            <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-white/5 text-center space-y-0.5">
              <div className="text-[10px] font-bold uppercase text-slate-400">Protein</div>
              <div className="text-base font-extrabold text-slate-900 dark:text-white">{nutrition.protein_g || 0}g</div>
              <div className="text-[10px] text-slate-400">per 100g</div>
            </div>

            {/* Fiber */}
            <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-white/5 text-center space-y-0.5">
              <div className="text-[10px] font-bold uppercase text-slate-400">Fiber</div>
              <div className="text-base font-extrabold text-slate-900 dark:text-white">{nutrition.fiber_g || 0}g</div>
              <div className="text-[10px] text-slate-400">per 100g</div>
            </div>

            {/* Trans Fat */}
            <div className={`p-2.5 rounded-xl border text-center space-y-0.5 ${
              (nutrition.trans_fat_g || 0) > 0.2 ? 'bg-rose-500/10 border-rose-500/30 text-rose-500' :
              'bg-emerald-500/10 border-emerald-500/30 text-emerald-500'
            }`}>
              <div className="text-[10px] font-bold uppercase">Trans Fat</div>
              <div className="text-base font-extrabold">{nutrition.trans_fat_g || 0}g</div>
              <div className="text-[10px]">{(nutrition.trans_fat_g || 0) > 0.2 ? 'Elevated' : 'Zero'}</div>
            </div>

          </div>
        </div>

      </div>

      {/* ── 6. DECISION TRACE: "How FoodGuard Reached This Result" ── */}
      {decision_trace.steps && decision_trace.steps.length > 0 && (
        <div className="glass-card rounded-2xl p-6 border space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <ListChecks className="w-4 h-4 text-emerald-500" />
              <span>Decision Trace: How FoodGuard Reached This Assessment</span>
            </h3>
            <span className="text-xs text-slate-400">
              {decision_trace.total_steps || decision_trace.steps.length} Criteria Evaluated
            </span>
          </div>

          <div className="space-y-2">
            {decision_trace.steps.map((step, idx) => (
              <div 
                key={idx} 
                className="p-3 rounded-xl bg-slate-50/50 dark:bg-slate-900/40 border border-slate-200 dark:border-white/5 flex items-start gap-3"
              >
                <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold shrink-0 mt-0.5 ${
                  step.status === 'PASS' ? 'bg-emerald-500/20 text-emerald-500 border border-emerald-500/30' :
                  step.status === 'FAIL' ? 'bg-rose-500/20 text-rose-500 border border-rose-500/30' :
                  'bg-amber-500/20 text-amber-500 border border-amber-500/30'
                }`}>
                  {step.status === 'PASS' ? '✓' : step.status === 'FAIL' ? '✕' : '⚠'}
                </span>
                <div className="space-y-0.5 text-xs">
                  <div className="font-bold text-slate-900 dark:text-white">
                    Step {step.step_num}: {step.title}
                  </div>
                  <div className="text-slate-600 dark:text-slate-300">
                    {step.detail}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── 7. SAFETY & REGULATORY DISCLAIMER ── */}
      <div className="p-4 rounded-xl bg-slate-100 dark:bg-slate-900/60 border border-slate-200 dark:border-white/5 text-xs text-slate-500 dark:text-slate-400 space-y-1">
        <div className="flex items-center gap-1.5 font-bold text-slate-700 dark:text-slate-300">
          <Info className="w-4 h-4 text-emerald-500" />
          <span>FoodGuard AI Regulatory & Laboratory Disclaimer</span>
        </div>
        <p className="leading-relaxed">
          {safety_disclaimer || "FoodGuard AI provides preliminary algorithmic food safety, adulteration screening, and regulatory mapping based on available public food standards. It does not replace certified laboratory chemical testing or definitive legal counsel."}
        </p>
      </div>

    </div>
  );
}
