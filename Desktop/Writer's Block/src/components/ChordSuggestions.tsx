import { Music2, Plus } from "lucide-react";

interface ChordSuggestionsProps {
  currentKey: string;
}

export function ChordSuggestions({ currentKey }: ChordSuggestionsProps) {
  const getChords = (key: string) => {
    const chordMap: Record<string, string[]> = {
      "C": ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
      "G": ["G", "Am", "Bm", "C", "D", "Em", "F♯dim"],
      "D": ["D", "Em", "F♯m", "G", "A", "Bm", "C♯dim"],
      "A": ["A", "Bm", "C♯m", "D", "E", "F♯m", "G♯dim"],
    };
    return chordMap[key] || chordMap["C"];
  };

  const chords = getChords(currentKey);
  const progressions = [
    { name: "I-V-vi-IV", chords: [chords[0], chords[4], chords[5], chords[3]] },
    { name: "I-IV-V", chords: [chords[0], chords[3], chords[4]] },
    { name: "vi-IV-I-V", chords: [chords[5], chords[3], chords[0], chords[4]] },
  ];

  return (
    <div className="relative group">
      {/* Outer glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-500/10 to-orange-500/10 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-700"></div>
      
      <div className="relative bg-gradient-to-br from-stone-800/30 via-amber-900/20 to-stone-800/30 backdrop-blur-2xl rounded-3xl border border-amber-500/30 p-6 shadow-2xl overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-40 h-40 bg-gradient-to-br from-amber-500 to-orange-500 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '4s' }}></div>
        </div>
        
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <Music2 className="w-5 h-5 text-amber-500" />
              <h2 className="text-lg text-amber-100">Chord Suggestions</h2>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <p className="text-xs text-stone-400 mb-3">Diatonic Chords</p>
              <div className="grid grid-cols-4 gap-2">
                {chords.map((chord, idx) => (
                  <button
                    key={chord}
                    className="relative p-3 rounded-xl bg-gradient-to-br from-stone-900/60 via-amber-950/40 to-stone-900/60 backdrop-blur-xl border border-amber-500/20 text-amber-200 hover:border-amber-500/50 hover:shadow-lg hover:shadow-amber-500/20 transition-all group overflow-hidden"
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-amber-500/10 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
                    <div className="text-center relative z-10">
                      <div className="mb-1">{chord}</div>
                      <div className="text-xs text-stone-500 group-hover:text-amber-600 transition-colors">
                        {["I", "ii", "iii", "IV", "V", "vi", "vii°"][idx]}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <p className="text-xs text-stone-400 mb-3">Popular Progressions</p>
              <div className="space-y-2">
                {progressions.map((prog) => (
                  <div
                    key={prog.name}
                    className="relative p-3 rounded-xl bg-gradient-to-br from-stone-900/60 via-amber-950/40 to-stone-900/60 backdrop-blur-xl border border-amber-500/20 hover:border-amber-500/50 hover:shadow-lg hover:shadow-amber-500/20 transition-all cursor-pointer group overflow-hidden"
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-amber-500/10 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                    <div className="flex items-center justify-between relative z-10">
                      <div>
                        <div className="text-sm text-amber-200 mb-1">{prog.name}</div>
                        <div className="text-xs text-stone-500">
                          {prog.chords.join(" → ")}
                        </div>
                      </div>
                      <button className="p-1.5 rounded-lg bg-amber-500/0 group-hover:bg-amber-500/20 transition-all">
                        <Plus className="w-4 h-4 text-amber-500" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}