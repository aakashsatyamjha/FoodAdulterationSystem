import React, { useState, useRef, useEffect } from 'react';
import { 
  Sparkles, 
  Send, 
  X, 
  Minus, 
  RotateCcw, 
  ShieldCheck, 
  ChevronRight, 
  ExternalLink, 
  Info, 
  AlertTriangle, 
  CheckCircle2, 
  Tag, 
  ArrowRight,
  Bot,
  User,
  Loader2,
  BookOpen,
  HelpCircle,
  Layers,
  FlaskConical,
  Scale,
  Apple,
  Globe,
  UserCheck
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

const QUESTION_CATEGORIES = [
  {
    id: 'regulatory',
    label: '🌐 Global Regulatory & Bans',
    icon: Globe,
    questions: [
      "Why is Titanium Dioxide banned in the EU but permitted in the US?",
      "Why do food regulations differ between India, USA, and Germany?",
      "Is Potassium Bromate allowed in bakery products?",
      "Why are azo dyes labeled with child warnings in Europe?",
      "What is the status of BVO (Brominated Vegetable Oil)?"
    ]
  },
  {
    id: 'adulterants',
    label: '🚨 Adulterants & Dyes',
    icon: FlaskConical,
    questions: [
      "How do I detect turmeric adulteration?",
      "What is Metanil Yellow industrial dye?",
      "What is Lead Chromate in spices?",
      "How do I detect adulteration in milk?",
      "What are Sudan Red dyes in chilli powder?",
      "How is honey adulterated with C4 sugar syrup?",
      "What is Argemone oil in mustard oil?",
      "What is FSSAI DART home testing guide?"
    ]
  },
  {
    id: 'additives',
    label: '🧪 Additives & INS Codes',
    icon: Tag,
    questions: [
      "What is MSG (INS 621) and is it safe?",
      "What is INS 635 in instant noodles?",
      "What is Sodium Benzoate (INS 211)?",
      "What is TBHQ (INS 319) in cooking oils?",
      "What is Potassium Sorbate (INS 202)?",
      "What is Maltodextrin in packaged food?",
      "What are banned food dyes in India?"
    ]
  },
  {
    id: 'consumer',
    label: '🥗 Consumer Profiles & Diet',
    icon: UserCheck,
    questions: [
      "Is this product suitable for a vegan diet?",
      "How does FoodGuard detect hidden animal ingredients?",
      "What are the high-sugar and low-sugar thresholds?",
      "Why is high sodium risky for blood pressure?",
      "What are the health risks of refined palm oil?"
    ]
  }
];

export default function Chatbot({ 
  isOpen, 
  onToggle, 
  currentAnalysis, 
  activeTab,
  onNavigateToAnalysis,
  initialQuery,
  userPreferences
}) {
  const { user } = useAuth();
  const { resolvedTheme } = useTheme();

  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'ai',
      text: "Hello! I am **FoodGuard AI**, your dedicated Food Safety Assistant. Ask me about ingredients, nutritional risks, why a product received its score, or FSSAI regulatory rules.",
      followups: [
        "How do I detect turmeric adulteration?",
        "What is Metanil Yellow?",
        "Why are some FSSAI-approved foods low score?",
        "What is MSG (INS 621) and is it safe?"
      ]
    }
  ]);

  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [minimized, setMinimized] = useState(false);
  const [showQuestionLibrary, setShowQuestionLibrary] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('adulterants');

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    if (isOpen && !minimized) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading, isOpen, minimized]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen && !minimized) {
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [isOpen, minimized]);

  // If initialQuery is passed (e.g. from Product Analysis "Ask AI" buttons)
  useEffect(() => {
    if (initialQuery && isOpen) {
      handleSendMessage(initialQuery);
    }
  }, [initialQuery]);

  const handleSendMessage = async (textToSend) => {
    const query = (textToSend || input).trim();
    if (!query || loading) return;

    setShowQuestionLibrary(false);
    const userMessageId = Date.now().toString();
    const newUserMessage = {
      id: userMessageId,
      sender: 'user',
      text: query
    };

    setMessages((prev) => [...prev, newUserMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: query,
          context: {
            activeTab,
            currentAnalysis: currentAnalysis || null,
            userPreferences: userPreferences || null
          },
          history: messages.map(m => ({ sender: m.sender, text: m.text }))
        })
      });

      if (!response.ok) {
        throw new Error('FoodGuard AI is temporarily unavailable.');
      }

      const data = await response.json();
      
      const newAiMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: data.response_text || 'No detailed analysis found.',
        productCard: data.product_card || null,
        ingredientCard: data.ingredient_card || null,
        followups: data.followup_suggestions || []
      };

      setMessages((prev) => [...prev, newAiMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'ai',
          isError: true,
          text: "FoodGuard AI is temporarily unavailable. Please try again or rephrase your question.",
          followups: [
            "How do I detect turmeric adulteration?",
            "What is Metanil Yellow?",
            "Is 20g sugar considered high?"
          ]
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: 'welcome',
        sender: 'ai',
        text: "Conversation refreshed. How can I assist you with food safety, ingredient analysis, or FSSAI standards?",
        followups: [
          "How do I detect turmeric adulteration?",
          "What is Metanil Yellow?",
          "What is FSSAI standard for milk?",
          "What is MSG (INS 621)?"
        ]
      }
    ]);
  };

  const renderFormattedText = (text) => {
    if (!text) return null;
    const lines = text.split('\n');
    return lines.map((line, idx) => {
      let formatted = line;
      const boldParts = line.split(/(\*\*.*?\*\*)/g);

      if (line.startsWith('• ') || line.startsWith('- ')) {
        return (
          <div key={idx} className="flex items-start gap-1.5 ml-1 my-0.5">
            <span className="text-emerald-400 font-bold shrink-0">•</span>
            <span>
              {boldParts.map((part, i) => {
                if (part.startsWith('**') && part.endsWith('**')) {
                  return <strong key={i} className="text-white font-bold">{part.slice(2, -2)}</strong>;
                }
                return part;
              })}
            </span>
          </div>
        );
      }

      if (line.match(/^\d+\.\s/)) {
        return (
          <div key={idx} className="flex items-start gap-1.5 ml-1 my-0.5">
            <span className="text-cyan-400 font-bold shrink-0 font-mono">{line.match(/^\d+\./)[0]}</span>
            <span>
              {line.replace(/^\d+\.\s*/, '').split(/(\*\*.*?\*\*)/g).map((part, i) => {
                if (part.startsWith('**') && part.endsWith('**')) {
                  return <strong key={i} className="text-white font-bold">{part.slice(2, -2)}</strong>;
                }
                return part;
              })}
            </span>
          </div>
        );
      }

      if (!line.trim()) {
        return <div key={idx} className="h-2" />;
      }

      return (
        <p key={idx} className="my-0.5">
          {boldParts.map((part, i) => {
            if (part.startsWith('**') && part.endsWith('**')) {
              return <strong key={i} className="text-white font-bold">{part.slice(2, -2)}</strong>;
            }
            if (part.startsWith('*') && part.endsWith('*')) {
              return <em key={i} className="text-slate-400 text-[11px]">{part.slice(1, -1)}</em>;
            }
            return part;
          })}
        </p>
      );
    });
  };

  const activeCategoryData = QUESTION_CATEGORIES.find(c => c.id === selectedCategory) || QUESTION_CATEGORIES[0];

  return (
    <>
      {/* ── Floating Trigger Button (Bottom-Right) ── */}
      {!isOpen && (
        <button
          onClick={onToggle}
          className="fixed bottom-6 right-6 z-40 flex items-center gap-2.5 px-4 py-3 rounded-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs sm:text-sm shadow-xl shadow-emerald-500/30 hover:shadow-emerald-500/50 hover:scale-105 transition-all cursor-pointer group"
          title="Open FoodGuard AI Assistant"
        >
          <div className="w-5 h-5 rounded-full bg-slate-950/20 flex items-center justify-center">
            <Sparkles className="w-3.5 h-3.5 text-slate-950 animate-pulse" />
          </div>
          <span className="hidden sm:inline">FoodGuard AI</span>
          <span className="sm:hidden font-bold">AI</span>
          {currentAnalysis && (
            <span className="w-2 h-2 rounded-full bg-slate-950"></span>
          )}
        </button>
      )}

      {/* ── Chat Window (Desktop Floating Glass / Mobile Drawer) ── */}
      {isOpen && (
        <div className={`
          fixed z-50 transition-all duration-300 ease-out
          ${minimized 
            ? 'bottom-6 right-6 w-72 h-14' 
            : 'bottom-0 right-0 sm:bottom-6 sm:right-6 w-full sm:w-[440px] h-[94vh] sm:h-[640px]'
          }
          glass-panel sm:rounded-3xl border border-white/15 shadow-2xl flex flex-col overflow-hidden bg-[#0a0f1d]/95 backdrop-blur-xl
        `}>
          
          {/* Header */}
          <div className="p-3.5 sm:p-4 bg-gradient-to-r from-emerald-950/60 via-slate-900/80 to-slate-950/80 border-b border-white/10 flex items-center justify-between shrink-0">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shadow-xs">
                <ShieldCheck className="w-4 h-4 stroke-[2.2]" />
              </div>
              <div>
                <div className="flex items-center gap-1.5">
                  <h3 className="text-xs sm:text-sm font-bold text-white tracking-tight">
                    FoodGuard AI
                  </h3>
                  <span className="text-[9px] font-bold px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    Online
                  </span>
                </div>
                <p className="text-[10px] text-slate-400 font-medium">
                  Your Food Safety Assistant
                </p>
              </div>
            </div>

            {/* Header Actions */}
            <div className="flex items-center gap-1">
              <button
                onClick={() => setShowQuestionLibrary(!showQuestionLibrary)}
                className={`px-2.5 py-1 rounded-lg text-[10px] font-bold transition-colors cursor-pointer border ${
                  showQuestionLibrary 
                    ? 'bg-emerald-500 text-slate-950 border-emerald-500' 
                    : 'bg-white/5 hover:bg-white/10 text-slate-300 border-white/10'
                }`}
                title="Explore 30+ curated questions"
              >
                Topics ({QUESTION_CATEGORIES.reduce((acc, c) => acc + c.questions.length, 0)})
              </button>

              <button
                onClick={clearChat}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors cursor-pointer"
                title="Clear conversation"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>

              <button
                onClick={() => setMinimized(!minimized)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors hidden sm:block cursor-pointer"
                title={minimized ? "Restore" : "Minimize"}
              >
                <Minus className="w-3.5 h-3.5" />
              </button>

              <button
                onClick={onToggle}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors cursor-pointer"
                title="Close"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Active Context Banner */}
          {!minimized && currentAnalysis && (
            <div className="px-3.5 py-1.5 bg-emerald-500/10 border-b border-emerald-500/20 flex items-center justify-between text-[11px] text-emerald-300 shrink-0">
              <span className="truncate flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                Active: <strong className="text-white truncate">{currentAnalysis.product_name}</strong>
              </span>
              <span className="font-mono text-[10px] font-bold bg-emerald-500/20 px-1.5 py-0.2 rounded shrink-0">
                {currentAnalysis.quality_score}/100
              </span>
            </div>
          )}

          {/* ── Topic / Question Library Drawer (Interactive) ── */}
          {!minimized && showQuestionLibrary && (
            <div className="p-3 bg-slate-900/95 border-b border-white/10 space-y-2.5 max-h-60 overflow-y-auto shrink-0 transition-all">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold text-white uppercase tracking-wider flex items-center gap-1">
                  <BookOpen className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Curated Question Library</span>
                </span>
                <span className="text-[10px] text-slate-400">Click any question to ask:</span>
              </div>

              {/* Category Filter Pills */}
              <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
                {QUESTION_CATEGORIES.map((cat) => (
                  <button
                    key={cat.id}
                    onClick={() => setSelectedCategory(cat.id)}
                    className={`px-2 py-1 rounded-lg text-[10px] font-bold whitespace-nowrap transition-colors cursor-pointer ${
                      selectedCategory === cat.id
                        ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        : 'bg-white/5 text-slate-400 hover:text-white border border-white/5'
                    }`}
                  >
                    {cat.label}
                  </button>
                ))}
              </div>

              {/* Category Questions Grid */}
              <div className="grid grid-cols-1 gap-1.5 pt-1">
                {activeCategoryData.questions.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(q)}
                    className="p-2 rounded-xl bg-white/5 hover:bg-emerald-500/15 border border-white/10 hover:border-emerald-500/30 text-left text-[11px] text-slate-200 hover:text-emerald-300 transition-colors flex items-center justify-between group cursor-pointer"
                  >
                    <span>{q}</span>
                    <ArrowRight className="w-3 h-3 opacity-40 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all text-emerald-400 shrink-0 ml-2" />
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Chat Messages Stream */}
          {!minimized && (
            <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs">
              
              {messages.map((msg) => (
                <div key={msg.id} className="space-y-2">
                  
                  {/* Message Bubble */}
                  <div className={`flex items-start gap-2.5 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                    
                    {msg.sender === 'ai' && (
                      <div className="w-7 h-7 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shrink-0 mt-0.5">
                        <Bot className="w-4 h-4" />
                      </div>
                    )}

                    <div className={`
                      max-w-[85%] rounded-2xl p-3.5 text-xs leading-relaxed space-y-1
                      ${msg.sender === 'user' 
                        ? 'bg-emerald-600 text-slate-950 font-medium rounded-tr-xs shadow-md shadow-emerald-600/10' 
                        : msg.isError
                        ? 'bg-rose-500/15 border border-rose-500/30 text-rose-300 rounded-tl-xs'
                        : 'glass-card border border-white/10 text-slate-200 rounded-tl-xs shadow-xs'
                      }
                    `}>
                      {renderFormattedText(msg.text)}
                    </div>

                    {msg.sender === 'user' && (
                      <div className="w-7 h-7 rounded-lg bg-slate-800 border border-white/10 flex items-center justify-center text-slate-300 shrink-0 mt-0.5 text-[10px] font-bold">
                        {user?.avatar || 'U'}
                      </div>
                    )}

                  </div>

                  {/* Compact Product Card (if provided) */}
                  {msg.productCard && (
                    <div className="ml-9 p-3 rounded-2xl bg-white/5 border border-white/10 space-y-2 max-w-[85%]">
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <span className="text-[10px] font-bold text-slate-400 uppercase">{msg.productCard.brand}</span>
                          <h4 className="font-bold text-xs text-white leading-tight">{msg.productCard.name}</h4>
                        </div>
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          msg.productCard.score >= 75 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'
                        }`}>
                          {msg.productCard.score}/100
                        </span>
                      </div>

                      <div className="flex items-center justify-between pt-1 border-t border-white/5 text-[11px]">
                        <span className="text-slate-400">{msg.productCard.risk}</span>
                        {onNavigateToAnalysis && (
                          <button
                            onClick={onNavigateToAnalysis}
                            className="text-emerald-400 hover:text-emerald-300 font-bold flex items-center gap-1 cursor-pointer"
                          >
                            <span>View Full Report</span>
                            <ArrowRight className="w-3 h-3" />
                          </button>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Compact Ingredient Card (if provided) */}
                  {msg.ingredientCard && (
                    <div className="ml-9 p-3 rounded-2xl bg-white/5 border border-white/10 space-y-1.5 max-w-[85%]">
                      <div className="flex items-center justify-between">
                        <h4 className="font-bold text-xs text-white">{msg.ingredientCard.name}</h4>
                        <span className="px-2 py-0.5 rounded text-[9px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">
                          {msg.ingredientCard.category}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-300 leading-tight">
                        <strong className="text-slate-400 font-medium">Purpose: </strong>
                        {msg.ingredientCard.purpose}
                      </p>
                    </div>
                  )}

                  {/* Follow-up Suggestion Chips */}
                  {msg.followups && msg.followups.length > 0 && (
                    <div className="ml-9 flex flex-wrap gap-1.5 pt-1">
                      {msg.followups.map((sug, i) => (
                        <button
                          key={i}
                          onClick={() => handleSendMessage(sug)}
                          className="px-2.5 py-1 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-emerald-500/40 text-[11px] text-slate-300 hover:text-emerald-400 transition-colors text-left cursor-pointer"
                        >
                          {sug}
                        </button>
                      ))}
                    </div>
                  )}

                </div>
              ))}

              {/* Typing State Indicator */}
              {loading && (
                <div className="flex items-center gap-2.5">
                  <div className="w-7 h-7 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shrink-0">
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  </div>
                  <div className="p-3 rounded-2xl bg-white/5 border border-white/10 text-slate-400 flex items-center gap-1.5 text-xs">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-bounce"></span>
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.2s]"></span>
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.4s]"></span>
                    <span className="ml-1 text-[11px] text-slate-400">Analyzing food formulation...</span>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}

          {/* Chat Input Bar */}
          {!minimized && (
            <div className="p-3 sm:p-3.5 border-t border-white/10 bg-slate-950/80 shrink-0">
              <form
                onSubmit={(e) => { e.preventDefault(); handleSendMessage(input); }}
                className="flex items-center gap-2"
              >
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder={currentAnalysis ? `Ask about ${currentAnalysis.product_name}...` : "Ask about ingredients, nutrition, FSSAI..."}
                  className="flex-1 px-3.5 py-2.5 rounded-xl bg-slate-900 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors"
                />
                
                <button
                  type="submit"
                  disabled={!input.trim() || loading}
                  className="p-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold disabled:opacity-30 disabled:cursor-not-allowed transition-all shadow-xs cursor-pointer shrink-0"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </div>
          )}

        </div>
      )}
    </>
  );
}
