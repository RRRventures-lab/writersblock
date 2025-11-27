import { Music, Save, Settings, Share2 } from "lucide-react";

export function StudioHeader() {
  return (
    <header className="border-b border-amber-500/20 bg-gradient-to-r from-stone-900/60 via-amber-900/40 to-stone-900/60 backdrop-blur-2xl relative overflow-hidden">
      {/* Animated liquid background */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-0 left-0 w-96 h-96 bg-amber-500/30 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '4s' }}></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-orange-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '6s', animationDelay: '2s' }}></div>
      </div>
      
      <div className="container mx-auto px-6 py-4 relative z-10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <div className="relative w-10 h-10 bg-gradient-to-br from-amber-500 via-orange-600 to-amber-700 rounded-2xl flex items-center justify-center shadow-2xl animate-pulse" style={{ animationDuration: '3s' }}>
                <div className="absolute inset-0 bg-gradient-to-br from-amber-400/50 to-orange-500/50 rounded-2xl blur-xl"></div>
                <Music className="w-6 h-6 text-white relative z-10" />
              </div>
              <div>
                <h1 className="text-xl text-amber-100 tracking-wide">Writer's Block</h1>
                <p className="text-xs text-amber-600">AI Creative Partner</p>
              </div>
            </div>

            <div className="ml-8 flex items-center gap-2 bg-gradient-to-r from-stone-800/40 via-amber-900/20 to-stone-800/40 backdrop-blur-xl rounded-2xl px-4 py-2 border border-amber-500/20 shadow-xl">
              <input
                type="text"
                placeholder="Untitled Song"
                className="bg-transparent outline-none text-amber-100 placeholder:text-stone-500 w-64"
              />
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button className="px-4 py-2 rounded-2xl bg-gradient-to-r from-stone-800/40 via-stone-700/40 to-stone-800/40 backdrop-blur-xl border border-amber-500/20 text-amber-200 hover:border-amber-500/40 transition-all flex items-center gap-2 shadow-lg hover:shadow-amber-500/20">
              <Save className="w-4 h-4" />
              Save
            </button>
            <button className="px-4 py-2 rounded-2xl bg-gradient-to-r from-amber-500 via-orange-600 to-amber-500 text-white hover:from-amber-400 hover:via-orange-500 hover:to-amber-400 transition-all flex items-center gap-2 shadow-xl shadow-amber-600/30 relative overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
              <Share2 className="w-4 h-4 relative z-10" />
              <span className="relative z-10">Export</span>
            </button>
            <button className="p-2 rounded-2xl bg-gradient-to-r from-stone-800/40 via-stone-700/40 to-stone-800/40 backdrop-blur-xl border border-amber-500/20 text-amber-200 hover:border-amber-500/40 transition-all shadow-lg">
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}