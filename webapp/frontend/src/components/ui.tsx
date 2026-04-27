"use client";

import React from "react";

interface MetricCardProps {
    label: string;
    value: string;
    unit?: string;
    icon?: React.ReactNode;
    accent?: "cyan" | "amber" | "red" | "green";
}

const accentColors = {
    cyan: "text-cyan-400 border-cyan-500/20",
    amber: "text-amber-400 border-amber-500/20",
    red: "text-red-400 border-red-500/20",
    green: "text-emerald-400 border-emerald-500/20",
};

export function MetricCard({ label, value, unit, icon, accent = "cyan" }: MetricCardProps) {
    return (
        <div className="metric-card group">
            <div className="flex items-center gap-2 mb-2">
                {icon && <span className={`${accentColors[accent].split(" ")[0]} opacity-60`}>{icon}</span>}
                <span className="text-xs font-medium uppercase tracking-wider text-white/40">{label}</span>
            </div>
            <div className="flex items-baseline gap-1.5">
                <span className={`text-xl font-semibold font-mono ${accentColors[accent].split(" ")[0]}`}>
                    {value}
                </span>
                {unit && <span className="text-xs text-white/30">{unit}</span>}
            </div>
        </div>
    );
}

interface SliderProps {
    label: string;
    value: number;
    min: number;
    max: number;
    step: number;
    onChange: (v: number) => void;
    unit?: string;
    formatValue?: (v: number) => string;
}

export function ParamSlider({ label, value, min, max, step, onChange, unit, formatValue }: SliderProps) {
    const display = formatValue ? formatValue(value) : value.toFixed(step < 1 ? 2 : 0);
    return (
        <div className="space-y-2">
            <div className="flex items-center justify-between">
                <label className="text-xs font-medium uppercase tracking-wider text-white/50">{label}</label>
                <span className="text-sm font-mono text-cyan-400">
                    {display}
                    {unit && <span className="text-white/30 ml-1">{unit}</span>}
                </span>
            </div>
            <input
                type="range"
                min={min}
                max={max}
                step={step}
                value={value}
                onChange={(e) => onChange(parseFloat(e.target.value))}
                className="w-full"
            />
        </div>
    );
}

export function GlassPanel({ children, className = "" }: { children: React.ReactNode; className?: string }) {
    return <div className={`glass-panel p-5 ${className}`}>{children}</div>;
}

export function PageHeader({ title, subtitle, equation }: { title: string; subtitle: string; equation?: string }) {
    return (
        <div className="mb-8">
            <h1 className="text-2xl font-bold text-white tracking-tight">{title}</h1>
            <p className="text-sm text-white/40 mt-1">{subtitle}</p>
            {equation && (
                <div className="mt-3 inline-block px-3 py-1.5 rounded-lg bg-white/[0.03] border border-white/[0.06]">
                    <code className="text-xs font-mono text-cyan-400/80">{equation}</code>
                </div>
            )}
        </div>
    );
}

export function LoadingOverlay() {
    return (
        <div className="absolute inset-0 flex items-center justify-center bg-black/30 backdrop-blur-sm rounded-2xl z-10">
            <div className="flex items-center gap-3">
                <div className="w-5 h-5 border-2 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin" />
                <span className="text-sm text-white/60">Computing...</span>
            </div>
        </div>
    );
}

export function StatusBadge({ active, label }: { active: boolean; label: string }) {
    return (
        <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${active ? "bg-emerald-400 shadow-[0_0_6px_rgba(16,185,129,0.5)]" : "bg-white/20"}`} />
            <span className="text-xs text-white/50">{label}</span>
        </div>
    );
}
