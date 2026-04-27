"use client";

import React from "react";

/* ── Metric Card ─────────────────────────── */
interface MetricCardProps {
    label: string;
    value: string;
    unit?: string;
    tone?: "default" | "negative" | "caution" | "positive";
}

const toneMap = {
    default: "text-white/90",
    negative: "text-red-400",
    caution: "text-amber-400",
    positive: "text-emerald-400",
};

export function MetricCard({ label, value, unit, tone = "default" }: MetricCardProps) {
    return (
        <div className="py-2.5">
            <p className="section-label mb-1">{label}</p>
            <div className="flex items-baseline gap-1.5">
                <span className={`text-[15px] font-medium metric-value ${toneMap[tone]}`}>{value}</span>
                {unit && <span className="text-[10px] text-white/20">{unit}</span>}
            </div>
        </div>
    );
}

/* ── Parameter Slider ────────────────────── */
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
        <div className="space-y-1.5">
            <div className="flex items-center justify-between">
                <span className="text-[11px] text-white/30 font-medium">{label}</span>
                <span className="text-[11px] font-mono text-white/60">
                    {display}
                    {unit && <span className="text-white/20 ml-0.5">{unit}</span>}
                </span>
            </div>
            <input
                type="range"
                min={min}
                max={max}
                step={step}
                value={value}
                onChange={(e) => onChange(parseFloat(e.target.value))}
            />
        </div>
    );
}

/* ── Panel ────────────────────────────────── */
export function Panel({ children, className = "" }: { children: React.ReactNode; className?: string }) {
    return <div className={`panel p-4 ${className}`}>{children}</div>;
}

/* ── Page Header ─────────────────────────── */
export function PageHeader({ title, subtitle, equation }: { title: string; subtitle: string; equation?: string }) {
    return (
        <div className="mb-6">
            <div className="flex items-baseline gap-3">
                <h1 className="text-[18px] font-semibold text-white/90 tracking-tight">{title}</h1>
                {equation && (
                    <code className="text-[10px] font-mono text-white/15 hidden sm:inline">{equation}</code>
                )}
            </div>
            <p className="text-[12px] text-white/25 mt-0.5">{subtitle}</p>
        </div>
    );
}

/* ── Loading Spinner ─────────────────────── */
export function LoadingOverlay() {
    return (
        <div className="absolute inset-0 flex items-center justify-center bg-[#08090d]/60 rounded-xl z-10">
            <div className="w-4 h-4 border-[1.5px] border-white/10 border-t-blue-500 rounded-full animate-spin" />
        </div>
    );
}

/* ── Section Divider ─────────────────────── */
export function Divider() {
    return <div className="divider my-3" />;
}
