import { useEffect, useState } from "react";

interface CircleOfFifthsProps {
  currentKey: string;
}

export function CircleOfFifths({ currentKey }: CircleOfFifthsProps) {
  const [rotation, setRotation] = useState(0);

  const keys = [
    { note: "C", angle: 0, major: true },
    { note: "G", angle: 30, major: true },
    { note: "D", angle: 60, major: true },
    { note: "A", angle: 90, major: true },
    { note: "E", angle: 120, major: true },
    { note: "B", angle: 150, major: true },
    { note: "F♯/G♭", angle: 180, major: true },
    { note: "D♭", angle: 210, major: true },
    { note: "A♭", angle: 240, major: true },
    { note: "E♭", angle: 270, major: true },
    { note: "B♭", angle: 300, major: true },
    { note: "F", angle: 330, major: true },
  ];

  const minorKeys = [
    { note: "Am", angle: 0 },
    { note: "Em", angle: 30 },
    { note: "Bm", angle: 60 },
    { note: "F♯m", angle: 90 },
    { note: "C♯m", angle: 120 },
    { note: "G♯m", angle: 150 },
    { note: "D♯m/E♭m", angle: 180 },
    { note: "B♭m", angle: 210 },
    { note: "Fm", angle: 240 },
    { note: "Cm", angle: 270 },
    { note: "Gm", angle: 300 },
    { note: "Dm", angle: 330 },
  ];

  useEffect(() => {
    const keyIndex = keys.findIndex(k => k.note === currentKey);
    if (keyIndex !== -1) {
      setRotation(-keys[keyIndex].angle);
    }
  }, [currentKey]);

  return (
    <div className="relative group">
      {/* Outer glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-500/20 to-orange-500/20 rounded-3xl blur-2xl group-hover:blur-3xl transition-all duration-700"></div>
      
      <div className="relative bg-gradient-to-br from-stone-800/30 via-amber-900/20 to-stone-800/30 backdrop-blur-2xl rounded-3xl border border-amber-500/30 p-6 shadow-2xl overflow-hidden">
        {/* Animated liquid background */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-gradient-to-br from-amber-500/30 to-orange-500/30 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '4s' }}></div>
        </div>
        
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg text-amber-100">Circle of Fifths</h2>
            <div className="px-3 py-1 rounded-full bg-gradient-to-r from-amber-500/20 via-orange-500/30 to-amber-500/20 border border-amber-500/40 shadow-lg animate-pulse" style={{ animationDuration: '3s' }}>
              <span className="text-sm text-amber-300">Key: {currentKey}</span>
            </div>
          </div>

          <div className="relative w-full aspect-square flex items-center justify-center">
            {/* Outer circle - Major keys */}
            <svg viewBox="0 0 400 400" className="w-full h-full transform transition-transform duration-700 ease-out" style={{ transform: `rotate(${rotation}deg)` }}>
              <defs>
                <filter id="glow">
                  <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                  <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
                <linearGradient id="activeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#d97706" />
                  <stop offset="100%" stopColor="#ea580c" />
                </linearGradient>
              </defs>

              {/* Background circles */}
              <circle cx="200" cy="200" r="180" fill="none" stroke="rgba(217, 119, 6, 0.1)" strokeWidth="2" />
              <circle cx="200" cy="200" r="140" fill="none" stroke="rgba(217, 119, 6, 0.1)" strokeWidth="2" />
              <circle cx="200" cy="200" r="100" fill="none" stroke="rgba(217, 119, 6, 0.1)" strokeWidth="1" />

              {/* Major key segments */}
              {keys.map((key, index) => {
                const angle = (key.angle - 90) * (Math.PI / 180);
                const startAngle = angle - (15 * Math.PI / 180);
                const endAngle = angle + (15 * Math.PI / 180);
                
                const outerRadius = 180;
                const innerRadius = 140;
                
                const x1 = 200 + innerRadius * Math.cos(startAngle);
                const y1 = 200 + innerRadius * Math.sin(startAngle);
                const x2 = 200 + outerRadius * Math.cos(startAngle);
                const y2 = 200 + outerRadius * Math.sin(startAngle);
                const x3 = 200 + outerRadius * Math.cos(endAngle);
                const y3 = 200 + outerRadius * Math.sin(endAngle);
                const x4 = 200 + innerRadius * Math.cos(endAngle);
                const y4 = 200 + innerRadius * Math.sin(endAngle);

                const isActive = key.note === currentKey;
                
                return (
                  <g key={key.note}>
                    <path
                      d={`M ${x1} ${y1} L ${x2} ${y2} A ${outerRadius} ${outerRadius} 0 0 1 ${x3} ${y3} L ${x4} ${y4} A ${innerRadius} ${innerRadius} 0 0 0 ${x1} ${y1}`}
                      fill={isActive ? "url(#activeGradient)" : "rgba(120, 53, 15, 0.3)"}
                      stroke={isActive ? "#f59e0b" : "rgba(217, 119, 6, 0.2)"}
                      strokeWidth={isActive ? "2" : "1"}
                      filter={isActive ? "url(#glow)" : "none"}
                      className="transition-all duration-300 cursor-pointer hover:fill-amber-900/50"
                    />
                    <text
                      x={200 + 160 * Math.cos(angle)}
                      y={200 + 160 * Math.sin(angle)}
                      textAnchor="middle"
                      dominantBaseline="middle"
                      fill={isActive ? "#fef3c7" : "#d6d3d1"}
                      className="text-sm pointer-events-none"
                      style={{ transform: `rotate(${-rotation}deg)`, transformOrigin: `${200 + 160 * Math.cos(angle)}px ${200 + 160 * Math.sin(angle)}px` }}
                    >
                      {key.note}
                    </text>
                  </g>
                );
              })}

              {/* Minor key segments (inner circle) */}
              {minorKeys.map((key, index) => {
                const angle = (key.angle - 90) * (Math.PI / 180);
                const startAngle = angle - (15 * Math.PI / 180);
                const endAngle = angle + (15 * Math.PI / 180);
                
                const outerRadius = 135;
                const innerRadius = 95;
                
                const x1 = 200 + innerRadius * Math.cos(startAngle);
                const y1 = 200 + innerRadius * Math.sin(startAngle);
                const x2 = 200 + outerRadius * Math.cos(startAngle);
                const y2 = 200 + outerRadius * Math.sin(startAngle);
                const x3 = 200 + outerRadius * Math.cos(endAngle);
                const y3 = 200 + outerRadius * Math.sin(endAngle);
                const x4 = 200 + innerRadius * Math.cos(endAngle);
                const y4 = 200 + innerRadius * Math.sin(endAngle);
                
                return (
                  <g key={key.note}>
                    <path
                      d={`M ${x1} ${y1} L ${x2} ${y2} A ${outerRadius} ${outerRadius} 0 0 1 ${x3} ${y3} L ${x4} ${y4} A ${innerRadius} ${innerRadius} 0 0 0 ${x1} ${y1}`}
                      fill="rgba(87, 83, 78, 0.3)"
                      stroke="rgba(168, 162, 158, 0.2)"
                      strokeWidth="1"
                      className="transition-all duration-300 cursor-pointer hover:fill-stone-700/50"
                    />
                    <text
                      x={200 + 115 * Math.cos(angle)}
                      y={200 + 115 * Math.sin(angle)}
                      textAnchor="middle"
                      dominantBaseline="middle"
                      fill="#a8a29e"
                      className="text-xs pointer-events-none"
                      style={{ transform: `rotate(${-rotation}deg)`, transformOrigin: `${200 + 115 * Math.cos(angle)}px ${200 + 115 * Math.sin(angle)}px` }}
                    >
                      {key.note}
                    </text>
                  </g>
                );
              })}

              {/* Center circle */}
              <circle cx="200" cy="200" r="90" fill="rgba(28, 25, 23, 0.8)" stroke="rgba(217, 119, 6, 0.3)" strokeWidth="2" />
              <text x="200" y="195" textAnchor="middle" fill="#fef3c7" className="text-2xl">
                {currentKey}
              </text>
              <text x="200" y="215" textAnchor="middle" fill="#d6d3d1" className="text-xs">
                MAJOR
              </text>
            </svg>
          </div>

          <div className="mt-4 flex items-center justify-center gap-2 text-xs text-stone-400">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-gradient-to-r from-amber-600 to-orange-700"></div>
              <span>Active Key</span>
            </div>
            <div className="w-px h-4 bg-stone-700"></div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-stone-700"></div>
              <span>Related Keys</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}