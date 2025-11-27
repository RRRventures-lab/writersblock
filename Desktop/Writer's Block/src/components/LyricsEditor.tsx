import { FileText, Mic2, Sparkles } from "lucide-react";
import { useState } from "react";

export function LyricsEditor() {
  const [lyrics, setLyrics] = useState(`[Verse 1]
Walking down this empty street
Memories beneath my feet

[Chorus]
And I'm singing to the stars above
`);

  return (
    <div className="relative group">
      {/* Outer glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-500/10 to-orange-500/10 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-700"></div>
      
      <div className="relative bg-gradient-to-br from-stone-800/30 via-amber-900/20 to-stone-800/30 backdrop-blur-2xl rounded-3xl border border-amber-500/30 p-6 shadow-2xl overflow-hidden">
        {/* Animated background particles */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 w-32 h-32 bg-amber-500 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '5s' }}></div>
          <div className="absolute bottom-10 right-10 w-32 h-32 bg-orange-500 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '7s', animationDelay: '2s' }}></div>
        </div>
        
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-amber-500" />
              <h2 className="text-lg text-amber-100">Lyrics</h2>
            </div>
            <div className="flex items-center gap-2">
              <button className="px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-500/20 via-orange-500/30 to-amber-500/20 backdrop-blur-xl border border-amber-500/40 text-amber-300 hover:border-amber-500/60 transition-all text-sm flex items-center gap-2 shadow-lg hover:shadow-amber-500/20 group">
                <Sparkles className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
                AI Suggest
              </button>
              <button className="p-2 rounded-xl bg-gradient-to-br from-stone-800/40 via-amber-900/20 to-stone-800/40 backdrop-blur-xl border border-amber-500/30 text-amber-300 hover:border-amber-500/50 transition-all shadow-lg">
                <Mic2 className="w-4 h-4" />
              </button>
            </div>
          </div>

          <div className="bg-gradient-to-br from-stone-900/60 via-amber-950/40 to-stone-900/60 backdrop-blur-xl rounded-2xl border border-amber-500/20 p-4 shadow-inner">
            <textarea
              value={lyrics}
              onChange={(e) => setLyrics(e.target.value)}
              className="w-full h-96 bg-transparent outline-none text-amber-100 resize-none font-mono leading-relaxed placeholder:text-stone-600"
              placeholder="Start writing your lyrics..."
              style={{ fontFamily: 'ui-monospace, monospace' }}
            />
          </div>

          <div className="mt-4 flex items-center justify-between text-xs text-stone-500">
            <div className="flex items-center gap-4">
              <span>12 lines</span>
              <span>48 words</span>
              <span>~0:45 duration</span>
            </div>
            <button className="text-amber-600 hover:text-amber-500 transition-colors">
              Check rhyme scheme
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}