"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Navigation, Atom, Zap, Orbit, ArrowRight, FlaskConical, BookOpen, TestTube } from "lucide-react";

const modules = [
  {
    href: "/alcubierre",
    title: "Alcubierre Warp Drive",
    subtitle: "Exotic matter & spacetime bubbles",
    icon: Navigation,
    color: "from-cyan-500/20 to-blue-600/20",
    borderColor: "border-cyan-500/20 hover:border-cyan-500/40",
    glowColor: "group-hover:shadow-[0_0_40px_rgba(6,182,212,0.1)]",
    iconColor: "text-cyan-400",
    metrics: [
      { label: "Metric", value: "ADM 3+1" },
      { label: "Equations", value: "12" },
    ],
    equation: "ds² = -c²dt² + (dx - v_s f dt)²",
  },
  {
    href: "/gravitomagnetic",
    title: "Gravitoelectromagnetism",
    subtitle: "Linearized GR & frame dragging",
    icon: Atom,
    color: "from-violet-500/20 to-purple-600/20",
    borderColor: "border-violet-500/20 hover:border-violet-500/40",
    glowColor: "group-hover:shadow-[0_0_40px_rgba(139,92,246,0.1)]",
    iconColor: "text-violet-400",
    metrics: [
      { label: "Fields", value: "E_g, B_g" },
      { label: "Confirmed", value: "GP-B 2011" },
    ],
    equation: "F = m(E_g + v × B_g)",
  },
  {
    href: "/zpe",
    title: "Zero-Point Energy",
    subtitle: "Casimir effect & quantum vacuum",
    icon: Zap,
    color: "from-amber-500/20 to-orange-600/20",
    borderColor: "border-amber-500/20 hover:border-amber-500/40",
    glowColor: "group-hover:shadow-[0_0_40px_rgba(245,158,11,0.1)]",
    iconColor: "text-amber-400",
    metrics: [
      { label: "Discrepancy", value: "10¹²⁰" },
      { label: "Verified", value: "1997" },
    ],
    equation: "F/A = -π²ℏc / (240 d⁴)",
  },
  {
    href: "/geodesic",
    title: "Geodesic Motion",
    subtitle: "Schwarzschild & Kerr orbits",
    icon: Orbit,
    color: "from-emerald-500/20 to-teal-600/20",
    borderColor: "border-emerald-500/20 hover:border-emerald-500/40",
    glowColor: "group-hover:shadow-[0_0_40px_rgba(16,185,129,0.1)]",
    iconColor: "text-emerald-400",
    metrics: [
      { label: "Spacetimes", value: "2" },
      { label: "Solver", value: "DOP853" },
    ],
    equation: "d²xᵘ/dτ² + Γᵘₐᵦ dxᵃ/dτ dxᵦ/dτ = 0",
  },
];

const stats = [
  { label: "Physics Modules", value: "4", icon: FlaskConical },
  { label: "Equations Implemented", value: "30+", icon: BookOpen },
  { label: "Tests Passing", value: "56", icon: TestTube },
];

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.08 } },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

export default function Home() {
  return (
    <div>
      {/* Hero */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-10"
      >
        <div className="flex items-center gap-4 mb-4">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-[0_0_30px_rgba(6,182,212,0.25)]">
            <span className="text-white font-bold text-lg">G</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-white tracking-tight">GRAVITON</h1>
            <p className="text-sm text-white/40">Exotic Propulsion & Spacetime Engineering Simulator</p>
          </div>
        </div>
        <div className="glow-line max-w-md" />
        <p className="text-sm text-white/30 mt-4 max-w-2xl leading-relaxed">
          Production-grade simulations grounded entirely in peer-reviewed physics from General Relativity,
          quantum field theory, and gravitoelectromagnetism. Every equation is citable.
        </p>
      </motion.div>

      {/* Stats Row */}
      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="grid grid-cols-3 gap-4 mb-8"
      >
        {stats.map((s) => {
          const Icon = s.icon;
          return (
            <motion.div key={s.label} variants={item} className="glass-panel p-4 flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-white/[0.03] flex items-center justify-center">
                <Icon className="w-5 h-5 text-cyan-400/60" />
              </div>
              <div>
                <p className="text-2xl font-bold font-mono text-white">{s.value}</p>
                <p className="text-xs text-white/30 uppercase tracking-wider">{s.label}</p>
              </div>
            </motion.div>
          );
        })}
      </motion.div>

      {/* Module Cards */}
      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="grid grid-cols-2 gap-5"
      >
        {modules.map((mod) => {
          const Icon = mod.icon;
          return (
            <motion.div key={mod.href} variants={item}>
              <Link href={mod.href} className="block group">
                <div className={`glass-panel glass-panel-hover p-6 transition-all duration-300 ${mod.glowColor}`}>
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${mod.color} flex items-center justify-center`}>
                        <Icon className={`w-5 h-5 ${mod.iconColor}`} />
                      </div>
                      <div>
                        <h3 className="text-base font-semibold text-white group-hover:text-cyan-300 transition-colors">{mod.title}</h3>
                        <p className="text-xs text-white/30">{mod.subtitle}</p>
                      </div>
                    </div>
                    <ArrowRight className="w-4 h-4 text-white/20 group-hover:text-white/50 group-hover:translate-x-1 transition-all" />
                  </div>

                  <div className="mb-4 px-3 py-1.5 rounded-lg bg-white/[0.02] border border-white/[0.04] inline-block">
                    <code className="text-[11px] font-mono text-white/30">{mod.equation}</code>
                  </div>

                  <div className="flex gap-6">
                    {mod.metrics.map((m) => (
                      <div key={m.label}>
                        <p className="text-xs text-white/25 uppercase tracking-wider">{m.label}</p>
                        <p className="text-sm font-mono text-white/60">{m.value}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </Link>
            </motion.div>
          );
        })}
      </motion.div>

      {/* Footer tagline */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6, duration: 0.5 }}
        className="mt-10 text-center"
      >
        <p className="text-xs text-white/15 uppercase tracking-[0.3em]">
          Powered by peer-reviewed physics
        </p>
        <p className="text-[10px] text-white/10 mt-1 font-mono">
          G_μν + Λg_μν = (8πG/c⁴) T_μν
        </p>
      </motion.div>
    </div>
  );
}
