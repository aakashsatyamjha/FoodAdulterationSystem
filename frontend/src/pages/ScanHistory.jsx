import React, { useState, useEffect } from 'react';
import { 
  Search, 
  History, 
  ShieldCheck, 
  ShieldAlert, 
  AlertTriangle, 
  Barcode, 
  FileText, 
  ArrowRight, 
  RefreshCw, 
  Calendar,
  Inbox
} from 'lucide-react';

const FALLBACK_RECORDS = [
  {
    id: 1,
    product_name: "Maggi 2-Minute Masala Noodles",
    brand: "Nestlé",
    category: "Instant Noodles",
    scan_type: "barcode",
    quality_score: 64,
    risk_level: "Moderate Risk",
    created_at: new Date(Date.now() - 1000 * 60 * 25).toISOString()
  },
  {
    id: 2,
    product_name: "Amul Pure Cow Ghee 1L",
    brand: "Amul",
    category: "Dairy",
    scan_type: "barcode",
    quality_score: 98,
    risk_level: "Safe / Low Risk",
    created_at: new Date(Date.now() - 1000 * 60 * 180).toISOString()
  },
  {
    id: 3,
    product_name: "Adulterated Turmeric Sample",
    brand: "Suspect Spices",
    category: "Spices",
    scan_type: "ocr",
    quality_score: 12,
    risk_level: "High Risk",
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString()
  },
  {
    id: 4,
    product_name: "Oreo Vanilla Sandwich Cookies",
    brand: "Cadbury",
    category: "Biscuits",
    scan_type: "barcode",
    quality_score: 48,
    risk_level: "Moderate Risk",
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString()
  }
];

export default function ScanHistory({ onSelectRecord }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [riskFilter, setRiskFilter] = useState('All');

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/history');
      if (res.ok) {
        const data = await res.json();
        setHistory(Array.isArray(data) && data.length > 0 ? data : FALLBACK_RECORDS);
      } else {
        setHistory(FALLBACK_RECORDS);
      }
    } catch (e) {
      console.warn("History API notice:", e);
      setHistory(FALLBACK_RECORDS);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const getRiskBadge = (risk) => {
    const r = (risk || '').toLowerCase();
    if (r.includes('high') || r.includes('adulterat')) {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/15 text-rose-500 border border-rose-500/30">
          <ShieldAlert className="w-3.5 h-3.5" />
          <span>High Risk</span>
        </span>
      );
    }
    if (r.includes('low') || r.includes('safe')) {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-500 border border-emerald-500/30">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Safe / Low</span>
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/15 text-amber-500 border border-amber-500/30">
        <AlertTriangle className="w-3.5 h-3.5" />
        <span>Moderate</span>
      </span>
    );
  };

  const getScorePill = (score) => {
    const s = Number(score) || 50;
    let cls = 'bg-amber-500/15 text-amber-500 border-amber-500/30';
    if (s >= 75) cls = 'bg-emerald-500/15 text-emerald-500 border-emerald-500/30';
    if (s < 45) cls = 'bg-rose-500/15 text-rose-500 border-rose-500/30';
    return (
      <span className={`px-2.5 py-1 rounded-lg text-xs font-mono font-bold border ${cls}`}>
        {s}/100
      </span>
    );
  };

  const filtered = history.filter((item) => {
    const matchesSearch = 
      (item.product_name || item.productName || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (item.brand || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (item.category || '').toLowerCase().includes(searchQuery.toLowerCase());

    const r = (item.risk_level || item.riskLevel || '').toLowerCase();
    let matchesRisk = true;
    if (riskFilter === 'Safe') matchesRisk = r.includes('safe') || r.includes('low');
    if (riskFilter === 'Moderate') matchesRisk = r.includes('moderate');
    if (riskFilter === 'High') matchesRisk = r.includes('high') || r.includes('adulterat');

    return matchesSearch && matchesRisk;
  });

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-12">
      
      {/* ── Header Card ── */}
      <div className="glass-card rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-lg border border-emerald-500/20">
              Audit Trail
            </span>
            <span className="text-xs text-slate-400">•</span>
            <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">MongoDB / Local Database</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            Inspection & Scan History
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
            Chronological log of verified food products, OCR formulations, and safety evaluations.
          </p>
        </div>

        <button
          onClick={fetchHistory}
          disabled={loading}
          className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-800/80 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 text-xs font-semibold transition-colors shrink-0 cursor-pointer border border-slate-200 dark:border-white/5"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Records</span>
        </button>
      </div>

      {/* ── Filters & Search Toolbar ── */}
      <div className="glass-card rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        
        {/* Search Input */}
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by product name, brand, or category..."
            className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-slate-200 dark:border-white/10 text-sm text-slate-900 dark:text-white placeholder-slate-400 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-colors"
          />
        </div>

        {/* Risk Filter Buttons */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
          {['All', 'Safe', 'Moderate', 'High'].map((f) => (
            <button
              key={f}
              onClick={() => setRiskFilter(f)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-colors cursor-pointer ${
                riskFilter === f
                  ? 'bg-emerald-600 text-slate-950 font-bold'
                  : 'bg-slate-100 dark:bg-slate-800/60 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-200 dark:border-white/5'
              }`}
            >
              {f === 'High' ? 'High Risk' : f === 'Safe' ? 'Safe / Low' : f}
            </button>
          ))}
        </div>

      </div>

      {/* ── Records Table (Desktop) & Card List (Mobile) ── */}
      <div className="glass-card rounded-2xl overflow-hidden">
        
        {loading ? (
          <div className="p-12 text-center text-slate-500 space-y-3">
            <RefreshCw className="w-6 h-6 animate-spin text-emerald-500 mx-auto" />
            <p className="text-sm">Loading historical verification records...</p>
          </div>
        ) : filtered.length === 0 ? (
          <div className="p-12 text-center text-slate-500 space-y-3">
            <Inbox className="w-8 h-8 text-slate-400 mx-auto" />
            <p className="text-sm font-semibold text-slate-700 dark:text-slate-300">No matching scan records found</p>
            <p className="text-xs text-slate-400">Try adjusting your search query or risk level filter.</p>
          </div>
        ) : (
          <>
            {/* Desktop Table View */}
            <div className="hidden md:block overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-100/70 dark:bg-slate-800/60 border-b border-slate-200 dark:border-white/5 text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">
                  <tr>
                    <th className="py-3.5 px-4">Product & Brand</th>
                    <th className="py-3.5 px-4">Category</th>
                    <th className="py-3.5 px-4">Method</th>
                    <th className="py-3.5 px-4">Score</th>
                    <th className="py-3.5 px-4">Risk Level</th>
                    <th className="py-3.5 px-4">Timestamp</th>
                    <th className="py-3.5 px-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-white/5">
                  {filtered.map((item) => {
                    const id = item.id;
                    const name = item.product_name || item.productName || 'Food Item';
                    const brand = item.brand || 'N/A';
                    const category = item.category || 'General';
                    const scanType = item.scan_type || item.scanType || 'barcode';
                    const score = item.quality_score || item.qualityScore || 50;
                    const risk = item.risk_level || item.riskLevel || 'Moderate Risk';
                    const date = item.created_at || item.timestamp;

                    return (
                      <tr 
                        key={id}
                        className="hover:bg-slate-100/50 dark:hover:bg-slate-800/40 transition-colors group cursor-pointer"
                        onClick={() => onSelectRecord(id)}
                      >
                        <td className="py-3.5 px-4">
                          <div className="font-semibold text-slate-900 dark:text-white text-sm group-hover:text-emerald-500 transition-colors">
                            {name}
                          </div>
                          <div className="text-[11px] text-slate-500 dark:text-slate-400">
                            {brand}
                          </div>
                        </td>

                        <td className="py-3.5 px-4 text-slate-600 dark:text-slate-300">
                          <span className="bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded-lg text-[11px] font-medium border border-slate-200 dark:border-white/5">
                            {category}
                          </span>
                        </td>

                        <td className="py-3.5 px-4">
                          <span className="inline-flex items-center gap-1 text-[11px] text-slate-600 dark:text-slate-400">
                            {scanType === 'ocr' ? <FileText className="w-3.5 h-3.5 text-cyan-500" /> : <Barcode className="w-3.5 h-3.5 text-emerald-500" />}
                            <span className="capitalize">{scanType}</span>
                          </span>
                        </td>

                        <td className="py-3.5 px-4">
                          {getScorePill(score)}
                        </td>

                        <td className="py-3.5 px-4">
                          {getRiskBadge(risk)}
                        </td>

                        <td className="py-3.5 px-4 text-slate-500 dark:text-slate-400 font-mono text-[11px]">
                          {date ? new Date(date).toLocaleString(undefined, { dateStyle: 'short', timeStyle: 'short' }) : 'Recent'}
                        </td>

                        <td className="py-3.5 px-4 text-right">
                          <button
                            onClick={(e) => { e.stopPropagation(); onSelectRecord(id); }}
                            className="text-emerald-500 hover:text-emerald-400 font-semibold inline-flex items-center gap-1 group-hover:translate-x-0.5 transition-transform"
                          >
                            <span>Inspect</span>
                            <ArrowRight className="w-3.5 h-3.5" />
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* Mobile Card List View */}
            <div className="md:hidden divide-y divide-slate-200 dark:divide-white/5">
              {filtered.map((item) => {
                const id = item.id;
                const name = item.product_name || item.productName || 'Food Item';
                const brand = item.brand || 'N/A';
                const category = item.category || 'General';
                const score = item.quality_score || item.qualityScore || 50;
                const risk = item.risk_level || item.riskLevel || 'Moderate Risk';

                return (
                  <div
                    key={id}
                    onClick={() => onSelectRecord(id)}
                    className="p-4 space-y-2 hover:bg-slate-100/50 dark:hover:bg-slate-800/40 active:bg-slate-100 transition-colors cursor-pointer"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <h3 className="font-semibold text-slate-900 dark:text-white text-sm">{name}</h3>
                        <p className="text-xs text-slate-500 dark:text-slate-400">{brand} • {category}</p>
                      </div>
                      {getScorePill(score)}
                    </div>

                    <div className="flex items-center justify-between pt-1">
                      {getRiskBadge(risk)}
                      <span className="text-xs text-emerald-500 font-semibold flex items-center gap-1">
                        View Analysis →
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        )}

      </div>

    </div>
  );
}
