import { Sparkles, Search } from "lucide-react";
import { useState } from "react";

export function RhymeAssistant() {
  const [searchWord, setSearchWord] = useState("");
  const rhymes = [
    { word: "night", syllables: 1, type: "Perfect" },
    { word: "light", syllables: 1, type: "Perfect" },
    { word: "sight", syllables: 1, type: "Perfect" },
    { word: "bright", syllables: 1, type: "Perfect" },
    { word: "flight", syllables: 1, type: "Perfect" },
    { word: "delight", syllables: 2, type: "Perfect" },
  ];

  return (
    <div className="relative group">
      {/* Outer glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-500/10 to-orange-500/10 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-700"></div>
      
      <div className="relative bg-gradient-to-br from-stone-800/30 via-amber-900/20 to-stone-800/30 backdrop-blur-2xl rounded-3xl border border-amber-500/30 p-6 shadow-2xl overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-gradient-to-br from-amber-500 to-orange-500 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '5s' }}></div>
        </div>
        
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-amber-500 animate-pulse" style={{ animationDuration: '3s' }} />
              <h2 className="text-lg text-amber-100">Rhyme Assistant</h2>
            </div>
          </div>

          <div className="relative mb-4">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-stone-500" />
            <input
              type="text"
              value={searchWord}
              onChange={(e) => setSearchWord(e.target.value)}
              placeholder="Find rhymes..."
              className="w-full pl-10 pr-4 py-2.5 bg-gradient-to-r from-stone-900/60 via-amber-950/40 to-stone-900/60 backdrop-blur-xl border border-amber-500/20 rounded-2xl outline-none text-amber-100 placeholder:text-stone-600 focus:border-amber-500/40 transition-all shadow-inner"
            />
          </div>

          <div className="space-y-2 max-h-64 overflow-y-auto">
            {rhymes.map((rhyme) => (
              <button
                key={rhyme.word}
                className="relative w-full p-3 rounded-xl bg-gradient-to-br from-stone-900/60 via-amber-950/40 to-stone-900/60 backdrop-blur-xl border border-amber-500/20 hover:border-amber-500/50 hover:shadow-lg hover:shadow-amber-500/20 transition-all text-left group overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-amber-500/10 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
                <div className="flex items-center justify-between relative z-10">
                  <div>
                    <div className="text-amber-200 mb-1">{rhyme.word}</div>
                    <div className="flex items-center gap-2 text-xs text-stone-500">
                      <span>{rhyme.syllables} syllable{rhyme.syllables > 1 ? "s" : ""}</span>
                      <span>•</span>
                      <span className="text-amber-600">{rhyme.type}</span>
                    </div>
                  </div>
                  <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                    <div className="w-6 h-6 rounded-lg bg-amber-500/20 flex items-center justify-center">
                      <span className="text-amber-500 text-xs">+</span>
                    </div>
                  </div>
                </div>
              </button>
            ))}
          </div>

          <div className="mt-4 pt-4 border-t border-amber-500/20">
            <button className="w-full py-2 rounded-2xl bg-gradient-to-r from-stone-800/40 via-amber-900/20 to-stone-800/40 backdrop-blur-xl border border-amber-500/30 text-amber-300 hover:border-amber-500/50 transition-all text-sm shadow-lg hover:shadow-amber-500/20">
              Show more rhymes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}