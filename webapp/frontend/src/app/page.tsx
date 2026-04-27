"use client";

import Link from "next/link";
import { Navigation, Atom, Zap, Orbit, ArrowUpRight } from "lucide-react";

const modules = [
  {
    href: "/alcubierre",
    title: "Alcubierre Warp Drive",
    description: "Exotic matter requirements for superluminal spacetime bubbles. ADM 3+1 formalism.",
    icon: Navigation,
    equation: "ds\u00b2 = -c\u00b2dt\u00b2 + (dx - v\u209b f dt)\u00b2 + dy\u00b2 + dz\u00b2",
    detail: "12 equations \u00b7 Alcubierre 1994",
  },
  {
    href: "/gravitomagnetic",
    title: "Gravitoelectromagnetism",
    description: "Linearized GR with Maxwell-like field equations. Lense-Thirring frame dragging.",
    icon: Atom,
    equation: "F = m(E\u2091 + v \u00d7 B\u2091)",
    detail: "Confirmed by Gravity Probe B \u00b7 2011",
  },
  {
    href: "/zpe",
    title: "Zero-Point Energy",
    description: "Casimir vacuum fluctuations, quantum inequalities, and exotic matter bounds.",
    icon: Zap,
    equation: "F/A = -\u03c0\u00b2\u0127c / (240 d\u2074)",
    detail: "Lamoreaux 1997 \u00b7 10\u00b9\u00b2\u2070 discrepancy",
  },
  {
    href: "/geodesic",
    title: "Geodesic Motion",
    description: "Schwarzschild and Kerr black hole orbits with effective potential formalism.",
    icon: Orbit,
    equation: "d\u00b2x\u1d58/d\u03c4\u00b2 + \u0393\u1d58\u2090\u1d66 dx\u1d43/d\u03c4 dx\u1d47/d\u03c4 = 0",
    detail: "DOP853 integrator \u00b7 BPT 1972",
  },
];

export default function Home() {
  return (
    <div className="max-w-[860px]">
      {/* Header */}
      <div className="mb-10 animate-in">
        <h1 className="text-[22px] font-semibold text-white/90 tracking-tight">GRAVITON</h1>
        <p className="text-[13px] text-white/25 mt-1 max-w-lg leading-relaxed">
          Spacetime engineering simulator grounded in peer-reviewed physics.
          Every equation is citable, every result is verifiable.
        </p>
      </div>

      {/* Stats */}
      <div className="flex gap-8 mb-8 animate-in" style={{ animationDelay: "0.05s" }}>
        {[
          { value: "4", label: "Modules" },
          { value: "30+", label: "Equations" },
          { value: "56", label: "Tests" },
          { value: "100%", label: "Pass rate" },
        ].map((s) => (
          <div key={s.label}>
            <p className="text-[18px] font-medium metric-value text-white/80">{s.value}</p>
            <p className="text-[10px] text-white/20 mt-0.5">{s.label}</p>
          </div>
        ))}
      </div>

      <div className="divider mb-6" />

      {/* Module List */}
      <div className="space-y-1">
        {modules.map((mod, i) => {
          const Icon = mod.icon;
          return (
            <Link
              key={mod.href}
              href={mod.href}
              className="group block animate-in"
              style={{ animationDelay: `${0.08 + i * 0.04}s` }}
            >
              <div className="flex items-start gap-4 px-4 py-4 -mx-4 rounded-xl transition-colors duration-150 hover:bg-white/[0.02]">
                <div className="w-8 h-8 rounded-lg bg-white/[0.03] border border-white/[0.04] flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Icon className="w-3.5 h-3.5 text-white/25 group-hover:text-white/50 transition-colors" strokeWidth={1.5} />
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h3 className="text-[13px] font-medium text-white/70 group-hover:text-white/90 transition-colors">
                      {mod.title}
                    </h3>
                    <ArrowUpRight className="w-3 h-3 text-white/0 group-hover:text-white/30 transition-all -translate-x-1 group-hover:translate-x-0" />
                  </div>
                  <p className="text-[11.5px] text-white/20 mt-0.5 leading-relaxed">{mod.description}</p>
                  <div className="flex items-center gap-3 mt-2">
                    <code className="text-[9.5px] font-mono text-white/12">{mod.equation}</code>
                    <span className="text-[9px] text-white/10">{mod.detail}</span>
                  </div>
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Footer */}
      <div className="mt-12 animate-in" style={{ animationDelay: "0.3s" }}>
        <p className="text-[9px] text-white/10 font-mono">
          G_\u03bcv + \u039bg_\u03bcv = (8\u03c0G/c\u2074) T_\u03bcv
        </p>
      </div>
    </div>
  );
}
