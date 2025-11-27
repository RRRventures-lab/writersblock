import { StudioHeader } from "./StudioHeader";
import { CircleOfFifths } from "./CircleOfFifths";
import { LyricsEditor } from "./LyricsEditor";
import { ChordSuggestions } from "./ChordSuggestions";
import { RhymeAssistant } from "./RhymeAssistant";
import { SongStructure } from "./SongStructure";
import { AIAssistant } from "./AIAssistant";
import { AudioControls } from "./AudioControls";
import { useState } from "react";

export function SongwritingStudio() {
  const [currentKey, setCurrentKey] = useState("C");
  const [isRecording, setIsRecording] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-stone-900 via-amber-950 to-stone-900 relative overflow-hidden">
      {/* Animated liquid background layers */}
      <div className="fixed inset-0">
        {/* Layer 1 - Slow moving blobs */}
        <div className="absolute top-0 left-0 w-[600px] h-[600px] bg-gradient-to-br from-amber-500/10 to-orange-500/10 rounded-full blur-3xl animate-blob"></div>
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-gradient-to-br from-orange-500/10 to-amber-600/10 rounded-full blur-3xl animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-0 left-1/2 w-[700px] h-[700px] bg-gradient-to-br from-amber-600/10 to-orange-400/10 rounded-full blur-3xl animate-blob animation-delay-4000"></div>
        
        {/* Texture overlay */}
        <div className="absolute inset-0 opacity-20 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZmlsdGVyIGlkPSJub2lzZSI+PGZlVHVyYnVsZW5jZSB0eXBlPSJmcmFjdGFsTm9pc2UiIGJhc2VGcmVxdWVuY3k9IjAuOSIgbnVtT2N0YXZlcz0iNCIvPjwvZmlsdGVyPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbHRlcj0idXJsKCNub2lzZSkiLz48L3N2Zz4=')]"></div>
      </div>
      
      <div className="relative z-10">
        <StudioHeader />
        
        <main className="container mx-auto px-6 py-6">
          <div className="grid grid-cols-12 gap-6">
            {/* Left Column - Circle of Fifths & Audio */}
            <div className="col-span-4 space-y-6">
              <CircleOfFifths currentKey={currentKey} />
              <AudioControls 
                isRecording={isRecording} 
                setIsRecording={setIsRecording}
                onKeyDetected={setCurrentKey}
              />
              <ChordSuggestions currentKey={currentKey} />
            </div>

            {/* Center Column - Lyrics & Structure */}
            <div className="col-span-5 space-y-6">
              <LyricsEditor />
              <SongStructure />
            </div>

            {/* Right Column - AI Assistant & Rhymes */}
            <div className="col-span-3 space-y-6">
              <AIAssistant currentKey={currentKey} />
              <RhymeAssistant />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}