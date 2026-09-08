import React, { useState, useEffect, useRef } from 'react';
import {
  Barcode,
  Camera,
  Search,
  AlertCircle,
  Loader2,
  StopCircle,
  HelpCircle,
  Zap,
  CheckCircle2,
  X,
  ScanLine,
  Package,
  ArrowRight,
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  RefreshCw
} from 'lucide-react';
import { Html5Qrcode } from 'html5-qrcode';

const READER_ID = 'qr-reader-container';

const SAMPLE_PRODUCTS = [
  { barcode: '8901058852813', name: 'Maggi 2-Minute Masala Noodles', brand: 'Nestlé', category: 'Instant Noodles', risk: 'Moderate' },
  { barcode: '7622210817014', name: 'Oreo Vanilla Cookies', brand: 'Cadbury', category: 'Biscuits', risk: 'Moderate' },
  { barcode: '8901262010047', name: 'Amul Pure Cow Ghee 1L', brand: 'Amul', category: 'Dairy', risk: 'Safe' },
  { barcode: '9990000000001', name: 'Adulterated Turmeric Powder', brand: 'Suspect Brand', category: 'Spices', risk: 'High Risk' },
  { barcode: '8901491101837', name: 'Tata Salt Vacuum Evaporated', brand: 'Tata', category: 'Salt', risk: 'Safe' },
  { barcode: '8901063151053', name: 'Amul Pasteurised Butter 500g', brand: 'Amul', category: 'Dairy', risk: 'Safe' },
];

export default function BarcodeScanner({ onScanSuccess, loading, error, sampleBarcodes = [] }) {
  const [manualCode, setManualCode] = useState('');
  const [scannerState, setScannerState] = useState('idle'); // 'idle' | 'starting' | 'active' | 'error'
  const [cameraError, setCameraError] = useState(null);
  const [lastScanned, setLastScanned] = useState(null);
  const html5QrRef = useRef(null);

  useEffect(() => {
    return () => {
      forceStop();
    };
  }, []);

  const forceStop = async () => {
    if (!html5QrRef.current) return;
    try {
      const state = html5QrRef.current.getState?.();
      if (state === 2) {
        await html5QrRef.current.stop();
      }
      html5QrRef.current.clear?.();
    } catch (_) {}
    html5QrRef.current = null;
  };

  const startScanner = async () => {
    setCameraError(null);
    setScannerState('starting');
    await forceStop();

    try {
      const instance = new Html5Qrcode(READER_ID, { verbose: false });
      html5QrRef.current = instance;

      await instance.start(
        { facingMode: 'environment' },
        { 
          fps: 10, 
          qrbox: { width: 280, height: 180 }, 
          aspectRatio: 1.5 
        },
        (decodedText) => {
          setLastScanned(decodedText);
          stopScanner().then(() => onScanSuccess(decodedText));
        },
        () => {}
      );
      setScannerState('active');
    } catch (err) {
      html5QrRef.current = null;
      const msg = (err?.message || '').toLowerCase();
      setCameraError(
        msg.includes('permission')
          ? 'Camera access was denied. Please grant camera permission in your browser or use the manual entry form.'
          : msg.includes('not found') || msg.includes('device')
          ? 'No camera device was detected on your system. Please enter the barcode manually.'
          : 'Could not initialize camera scanner. Please use manual entry or select a sample product.'
      );
      setScannerState('error');
    }
  };

  const stopScanner = async () => {
    setScannerState('idle');
    await forceStop();
  };

  const handleManualSubmit = (e) => {
    e.preventDefault();
    const trimmed = manualCode.trim();
    if (!trimmed) return;
    onScanSuccess(trimmed);
  };

  const displaySamples = sampleBarcodes.length > 0 ? sampleBarcodes : SAMPLE_PRODUCTS;

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">

      {/* ── Section Header ── */}
      <div className="glass-card rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-lg border border-emerald-500/20">
              Module 01
            </span>
            <span className="text-xs text-slate-400">•</span>
            <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">Barcode Identification</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            Barcode Scanner & Product Lookup
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            Point your device camera at any packaged food product barcode, or enter the code manually.
          </p>
        </div>

        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-300 text-xs font-mono shrink-0">
          <Barcode className="w-4 h-4 text-emerald-500" />
          <span>EAN-13 / UPC-A Global Registry</span>
        </div>
      </div>

      {/* ── API / Lookup Error Alert ── */}
      {error && (
        <div className="p-4 rounded-2xl bg-rose-500/10 border border-rose-500/25 flex items-start gap-3 text-rose-300 text-sm">
          <AlertCircle className="w-5 h-5 text-rose-500 shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-rose-400">Product Lookup Notice</p>
            <p className="text-xs text-rose-300/80 mt-0.5">{error}</p>
          </div>
        </div>
      )}

      {/* ── 2-Column Main Workspace ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

        {/* Left Column (7 cols): Camera Scanner */}
        <div className="lg:col-span-7 glass-card rounded-2xl p-6 flex flex-col justify-between space-y-4">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Camera className="w-5 h-5 text-emerald-500" />
                <h2 className="font-bold text-slate-900 dark:text-white text-base">Live Camera Scanner</h2>
              </div>
              
              {scannerState === 'active' && (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-semibold animate-pulse">
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                  Active Scanning
                </span>
              )}
            </div>

            {/* Viewfinder Container */}
            <div
              id={READER_ID}
              className="w-full rounded-2xl overflow-hidden bg-slate-950 border border-slate-200 dark:border-white/10 relative min-h-[260px] flex items-center justify-center text-white"
            >
              {(scannerState === 'idle' || scannerState === 'error') && (
                <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center space-y-3 pointer-events-none">
                  <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-500">
                    <ScanLine className="w-6 h-6" />
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm font-semibold text-slate-300">
                      Camera is currently inactive
                    </p>
                    <p className="text-xs text-slate-500 max-w-xs">
                      Click below to grant camera access and align the barcode within the framing guide.
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Error Message */}
            {cameraError && (
              <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/25 text-xs text-amber-400 flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                <span>{cameraError}</span>
              </div>
            )}

            {/* Last Scanned Feedback */}
            {lastScanned && (
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/25 text-xs text-emerald-400 flex items-center gap-2 font-mono">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Barcode detected: <strong>{lastScanned}</strong>. Processing analysis...</span>
              </div>
            )}
          </div>

          {/* Camera Action Toggle */}
          <div className="pt-2">
            {scannerState === 'idle' || scannerState === 'error' ? (
              <button
                onClick={startScanner}
                disabled={loading}
                className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-sm shadow-md shadow-emerald-600/20 transition-all disabled:opacity-50 cursor-pointer"
              >
                <Camera className="w-4 h-4" />
                <span>Start Camera Scanner</span>
              </button>
            ) : scannerState === 'starting' ? (
              <button disabled className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-400 font-semibold text-sm border border-slate-200 dark:border-white/5 cursor-not-allowed">
                <Loader2 className="w-4 h-4 animate-spin text-slate-400" />
                <span>Initializing Camera...</span>
              </button>
            ) : (
              <button
                onClick={stopScanner}
                className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-sm shadow-md transition-all cursor-pointer"
              >
                <StopCircle className="w-4 h-4" />
                <span>Stop Camera Scanner</span>
              </button>
            )}
          </div>
        </div>

        {/* Right Column (5 cols): Manual Entry & Help */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* Manual Entry Form */}
          <div className="glass-card rounded-2xl p-6 space-y-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <Search className="w-5 h-5 text-slate-700 dark:text-slate-300" />
                <h2 className="font-bold text-slate-900 dark:text-white text-base">Manual Barcode Lookup</h2>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Type the barcode digits printed directly beneath the striped lines.
              </p>
            </div>

            <form onSubmit={handleManualSubmit} className="space-y-3">
              <div className="relative">
                <input
                  type="text"
                  value={manualCode}
                  onChange={(e) => setManualCode(e.target.value)}
                  placeholder="e.g. 8901058852813"
                  className="w-full pl-10 pr-9 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-slate-200 dark:border-white/10 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 text-slate-900 dark:text-white placeholder-slate-400 text-sm font-mono transition-colors outline-none"
                />
                <Barcode className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                {manualCode && (
                  <button
                    type="button"
                    onClick={() => setManualCode('')}
                    className="absolute right-3 top-3 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 cursor-pointer"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>

              <button
                type="submit"
                disabled={loading || !manualCode.trim()}
                className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-slate-900 dark:bg-white hover:bg-slate-800 dark:hover:bg-slate-100 text-white dark:text-slate-950 font-bold text-sm shadow-xs transition-colors disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Analyzing Product...</span>
                  </>
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    <span>Lookup & Analyze</span>
                  </>
                )}
              </button>
            </form>

            <div className="p-3 rounded-xl bg-slate-100/70 dark:bg-slate-800/40 border border-slate-200 dark:border-white/5 text-xs text-slate-600 dark:text-slate-400 flex items-start gap-2">
              <HelpCircle className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
              <span>Queries Open Food Facts Global API with offline catalog fallback.</span>
            </div>
          </div>

          {/* Quick-Help Barcode Guide */}
          <div className="glass-card rounded-2xl p-5 space-y-2">
            <h3 className="font-bold text-slate-900 dark:text-white text-xs uppercase tracking-wider flex items-center gap-1.5">
              <Package className="w-4 h-4 text-emerald-500" />
              <span>Barcode Identification Tips</span>
            </h3>
            <ul className="text-xs text-slate-600 dark:text-slate-400 space-y-1.5 pl-4 list-disc">
              <li>EAN-13 barcodes in India typically start with prefix <strong>890</strong>.</li>
              <li>Ensure good lighting when using camera capture to avoid glare reflections.</li>
              <li>Hold package ~15cm from camera lens until automatic focus locks.</li>
            </ul>
          </div>

        </div>

      </div>

      {/* ── Pre-populated Test Samples Grid ── */}
      <div className="glass-card rounded-2xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-bold text-slate-900 dark:text-white text-base flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-500" />
              <span>One-Click Verification Samples</span>
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Click any benchmark product to test the AI evaluation engine immediately.
            </p>
          </div>
          <span className="text-xs font-mono text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded-lg border border-slate-200 dark:border-white/5">
            {displaySamples.length} Samples Ready
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {displaySamples.map((item, idx) => (
            <button
              key={item.barcode || idx}
              onClick={() => {
                setManualCode(item.barcode);
                onScanSuccess(item.barcode);
              }}
              disabled={loading}
              className="p-3.5 rounded-xl bg-slate-100/60 dark:bg-slate-800/40 hover:bg-slate-200/70 dark:hover:bg-slate-800/80 border border-slate-200 dark:border-white/5 text-left transition-colors group disabled:opacity-50 flex flex-col justify-between cursor-pointer"
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <span className="font-semibold text-slate-900 dark:text-white text-xs group-hover:text-emerald-500 transition-colors line-clamp-1">
                  {item.name}
                </span>
                <span className="text-[10px] text-slate-500 dark:text-slate-400 bg-white dark:bg-slate-900 border border-slate-200 dark:border-white/10 px-1.5 py-0.5 rounded shrink-0">
                  {item.brand || item.category}
                </span>
              </div>
              <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-mono">
                <span>{item.barcode}</span>
                <span className="text-emerald-600 dark:text-emerald-400 font-sans font-semibold text-xs group-hover:translate-x-0.5 transition-transform flex items-center gap-0.5">
                  Inspect →
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>

    </div>
  );
}
