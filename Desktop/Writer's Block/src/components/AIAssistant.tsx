import { Bot, Send, Sparkles } from "lucide-react";
import { useState } from "react";

interface AIAssistantProps {
  currentKey: string;
}

export function AIAssistant({ currentKey }: AIAssistantProps) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hi! I'm your songwriting partner. I can help with lyrics, melody ideas, chord progressions, and song structure. What would you like to work on?",
    },
    {
      role: "user",
      content: "Help me write a chorus about hope",
    },
    {
      role: "assistant",
      content: `In ${currentKey} major, try this:\n\n"Light breaks through the darkest night\nHope's alive and burning bright\nWe'll rise above, we'll find our way\nTomorrow starts with today"\n\nSuggest a I-V-vi-IV progression for emotional impact.`,
    },
  ]);
  const [input, setInput] = useState("");

  return (
    <div className="relative group">
      {/* Outer glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-500/20 to-orange-500/20 rounded-3xl blur-2xl group-hover:blur-3xl transition-all duration-700"></div>
      
      <div className="relative bg-gradient-to-br from-stone-800/30 via-amber-900/20 to-stone-800/30 backdrop-blur-2xl rounded-3xl border border-amber-500/30 shadow-2xl flex flex-col h-[600px] overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-64 h-64 bg-gradient-to-br from-amber-500 to-orange-500 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '6s' }}></div>
          <div className="absolute bottom-0 right-0 w-48 h-48 bg-gradient-to-br from-orange-500 to-amber-600 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '8s', animationDelay: '2s' }}></div>
        </div>
        
        <div className="flex items-center gap-2 p-6 border-b border-amber-500/20 relative z-10">
          <div className="relative w-8 h-8 rounded-xl bg-gradient-to-br from-amber-500 via-orange-600 to-amber-700 flex items-center justify-center shadow-xl">
            <div className="absolute inset-0 bg-gradient-to-br from-amber-400/50 to-orange-500/50 rounded-xl blur-lg animate-pulse" style={{ animationDuration: '3s' }}></div>
            <Bot className="w-5 h-5 text-white relative z-10" />
          </div>
          <div>
            <h2 className="text-lg text-amber-100">AI Assistant</h2>
            <div className="flex items-center gap-1 text-xs text-emerald-400">
              <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse"></div>
              Online
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-4 relative z-10">
          {messages.map((message, idx) => (
            <div
              key={idx}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"} animate-fadeIn`}
            >
              <div
                className={`max-w-[85%] rounded-2xl p-4 shadow-lg relative overflow-hidden ${
                  message.role === "user"
                    ? "bg-gradient-to-r from-amber-500 via-orange-600 to-amber-500 text-white"
                    : "bg-gradient-to-br from-stone-900/60 via-amber-950/40 to-stone-900/60 backdrop-blur-xl border border-amber-500/20 text-amber-100"
                }`}
              >
                {message.role === "user" && (
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent translate-x-[-100%] animate-shimmer"></div>
                )}
                {message.role === "assistant" && (
                  <div className="flex items-center gap-2 mb-2">
                    <Sparkles className="w-3 h-3 text-amber-500 animate-pulse" />
                    <span className="text-xs text-amber-500">AI Suggestion</span>
                  </div>
                )}
                <p className="text-sm whitespace-pre-line leading-relaxed relative z-10">
                  {message.content}
                </p>
              </div>
            </div>
          ))}
        </div>

        <div className="p-4 border-t border-amber-500/20 relative z-10 bg-gradient-to-r from-stone-900/40 via-amber-950/30 to-stone-900/40 backdrop-blur-xl">
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask for help..."
              className="flex-1 px-4 py-2.5 bg-gradient-to-r from-stone-900/60 via-amber-950/40 to-stone-900/60 backdrop-blur-xl border border-amber-500/20 rounded-2xl outline-none text-amber-100 placeholder:text-stone-600 focus:border-amber-500/40 transition-all shadow-inner"
            />
            <button className="relative p-2.5 rounded-2xl bg-gradient-to-r from-amber-500 via-orange-600 to-amber-500 text-white hover:from-amber-400 hover:via-orange-500 hover:to-amber-400 transition-all shadow-xl shadow-amber-500/30 overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
              <Send className="w-5 h-5 relative z-10" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}