import { Mic, Square, Play, Volume2, Activity } from "lucide-react";
import { useState } from "react";

interface AudioControlsProps {
  isRecording: boolean;
  setIsRecording: (value: boolean) => void;
  onKeyDetected: (key: string) => void;
}

export function AudioControls({ isRecording, setIsRecording, onKeyDetected }: AudioControlsProps) {
  const [volume, setVolume] = useState(75);

  const handleRecord = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      // Simulate key detection after 2 seconds
      setTimeout(() => {
        const keys = ["C", "G", "D", "A", "E", "F", "B♭"];
        const randomKey = keys[Math.floor(Math.random() * keys.length)];
        onKeyDetected(randomKey);
      }, 2000);
    }
  };

  return (
    <div className="relative group">
      {/* Outer glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-500/10 to-orange-500/10 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-700"></div>
      
      <div className="relative bg-gradient-to-br from-stone-800/30 via-amber-900/20 to-stone-800/30 backdrop-blur-2xl rounded-3xl border border-amber-500/30 p-6 shadow-2xl overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-0 right-0 w-48 h-48 bg-gradient-to-br from-amber-500/40 to-orange-500/40 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '3s' }}></div>
        </div>
        
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg text-amber-100">Audio Input</h2>
            <Activity className="w-5 h-5 text-amber-500 animate-pulse" />
          </div>

          {/* Waveform Visualization */}
          <div className="bg-gradient-to-br from-stone-900/60 via-amber-950/40 to-stone-900/60 backdrop-blur-xl rounded-2xl p-4 mb-6 border border-amber-500/20 shadow-inner">
            <div className="flex items-end justify-center gap-1 h-24">
              {Array.from({ length: 40 }).map((_, i) => (
                <div
                  key={i}
                  className={`flex-1 rounded-t transition-all duration-150 ${
                    isRecording
                      ? "bg-gradient-to-t from-amber-500 via-orange-500 to-amber-400 shadow-lg shadow-amber-500/50"
                      : "bg-stone-700/50"
                  }`}
                  style={{
                    height: isRecording
                      ? `${Math.random() * 80 + 20}%`
                      : "20%",
                  }}
                ></div>
              ))}
            </div>
          </div>

          {/* Controls */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <button
                onClick={handleRecord}
                className={`relative flex-1 py-3 rounded-2xl flex items-center justify-center gap-2 transition-all shadow-xl overflow-hidden group ${
                  isRecording
                    ? "bg-gradient-to-r from-red-600 via-red-500 to-red-600 hover:from-red-500 hover:via-red-400 hover:to-red-500 text-white shadow-red-500/50"
                    : "bg-gradient-to-r from-amber-500 via-orange-600 to-amber-500 hover:from-amber-400 hover:via-orange-500 hover:to-amber-400 text-white shadow-amber-500/50"
                }`}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
                {isRecording ? (
                  <>
                    <Square className="w-5 h-5 relative z-10" />
                    <span className="relative z-10">Stop Recording</span>
                  </>
                ) : (
                  <>
                    <Mic className="w-5 h-5 relative z-10" />
                    <span className="relative z-10">Start Recording</span>
                  </>
                )}
              </button>
              <button className="p-3 rounded-2xl bg-gradient-to-br from-stone-800/40 via-amber-900/20 to-stone-800/40 backdrop-blur-xl border border-amber-500/30 text-amber-200 hover:border-amber-500/50 transition-all shadow-lg">
                <Play className="w-5 h-5" />
              </button>
            </div>

            {/* Volume Control */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2 text-stone-400">
                  <Volume2 className="w-4 h-4" />
                  <span>Input Level</span>
                </div>
                <span className="text-amber-300">{volume}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={volume}
                onChange={(e) => setVolume(Number(e.target.value))}
                className="w-full h-2 bg-stone-800 rounded-lg appearance-none cursor-pointer accent-amber-600"
              />
            </div>

            {/* Status */}
            <div className="flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <div
                  className={`w-2 h-2 rounded-full ${
                    isRecording ? "bg-red-500 animate-pulse" : "bg-stone-600"
                  }`}
                ></div>
                <span className="text-stone-400">
                  {isRecording ? "Recording..." : "Ready"}
                </span>
              </div>
              <span className="text-stone-500">48kHz / 24-bit</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}