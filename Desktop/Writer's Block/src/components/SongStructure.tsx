import { LayoutGrid, Plus } from "lucide-react";

export function SongStructure() {
  const sections = [
    { name: "Intro", duration: "0:08", color: "bg-blue-600" },
    { name: "Verse 1", duration: "0:16", color: "bg-emerald-600" },
    { name: "Chorus", duration: "0:20", color: "bg-amber-600" },
    { name: "Verse 2", duration: "0:16", color: "bg-emerald-600" },
    { name: "Chorus", duration: "0:20", color: "bg-amber-600" },
    { name: "Bridge", duration: "0:12", color: "bg-purple-600" },
    { name: "Chorus", duration: "0:20", color: "bg-amber-600" },
    { name: "Outro", duration: "0:08", color: "bg-blue-600" },
  ];

  return (
    <div className="relative group">
      {/* Outer glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-500/10 to-orange-500/10 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-700"></div>
      
      <div className="relative bg-gradient-to-br from-stone-800/30 via-amber-900/20 to-stone-800/30 backdrop-blur-2xl rounded-3xl border border-amber-500/30 p-6 shadow-2xl overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute bottom-0 left-0 w-56 h-56 bg-gradient-to-br from-amber-500 to-orange-500 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '6s' }}></div>
        </div>
        
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <LayoutGrid className="w-5 h-5 text-amber-500" />
              <h2 className="text-lg text-amber-100">Song Structure</h2>
            </div>
            <button className="p-2 rounded-2xl bg-gradient-to-br from-stone-800/40 via-amber-900/20 to-stone-800/40 backdrop-blur-xl border border-amber-500/30 text-amber-300 hover:border-amber-500/50 transition-all shadow-lg">
              <Plus className="w-4 h-4" />
            </button>
          </div>

          <div className="space-y-3">
            {sections.map((section, idx) => (
              <div
                key={idx}
                className="relative flex items-center gap-3 p-3 rounded-xl bg-gradient-to-br from-stone-900/60 via-amber-950/40 to-stone-900/60 backdrop-blur-xl border border-amber-500/20 hover:border-amber-500/50 hover:shadow-lg hover:shadow-amber-500/20 transition-all cursor-pointer group/item overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-amber-500/5 to-transparent translate-x-[-100%] group-hover/item:translate-x-[100%] transition-transform duration-1000"></div>
                <div className={`w-1 h-12 rounded-full ${section.color} shadow-lg`}></div>
                <div className="flex-1 relative z-10">
                  <div className="text-amber-200 mb-1">{section.name}</div>
                  <div className="text-xs text-stone-500">{section.duration}</div>
                </div>
                <div className="flex items-center gap-2 opacity-0 group-hover/item:opacity-100 transition-opacity relative z-10">
                  <button className="p-1.5 rounded-lg bg-stone-800/60 hover:bg-stone-700/60 transition-all">
                    <svg className="w-4 h-4 text-stone-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </button>
                  <button className="p-1.5 rounded-lg bg-stone-800/60 hover:bg-stone-700/60 transition-all">
                    <svg className="w-4 h-4 text-stone-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-4 p-3 rounded-xl bg-gradient-to-br from-stone-900/60 via-amber-950/40 to-stone-900/60 backdrop-blur-xl border border-dashed border-amber-500/30 text-center cursor-pointer hover:border-amber-500/50 hover:bg-stone-800/40 transition-all">
            <Plus className="w-5 h-5 text-stone-500 mx-auto mb-1" />
            <p className="text-xs text-stone-500">Add Section</p>
          </div>
        </div>
      </div>
    </div>
  );
}