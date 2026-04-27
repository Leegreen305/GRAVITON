"use client";

import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import { Zap, AlertTriangle, FlaskConical, Scale } from "lucide-react";
import Plot from "../../components/PlotWrapper";
import { darkLayout } from "../../components/PlotWrapper";
import { MetricCard, ParamSlider, GlassPanel, PageHeader, LoadingOverlay } from "../../components/ui";
import { fetchAPI, formatScientific } from "../../lib/api";

interface ZPEData {
    casimir_force_pa: number;
    casimir_energy_density: number;
    casimir_total_energy: number;
    sweep_d: number[];
    sweep_force: number[];
    sweep_energy: number[];
    zpe_density: number;
    cosmological_discrepancy: {
        rho_qft_J_per_m3: number;
        rho_observed_J_per_m3: number;
        ratio: number;
        log10_ratio: number;
    };
    qi_bound: number;
    lamoreaux: {
        separation_m: number;
        theory_Pa: number;
        experiment_Pa: number;
        relative_error: number;
    };
    spectral_omega: number[];
    spectral_density: number[];
}

export default function ZPEPage() {
    const [plateSep, setPlateSep] = useState(100); // in nm
    const [data, setData] = useState<ZPEData | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const compute = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await fetchAPI<ZPEData>("/api/zpe", {
                plate_separation: plateSep * 1e-9,
                sweep_points: 200,
            });
            setData(result);
        } catch (e: unknown) {
            setError(e instanceof Error ? e.message : "Computation failed");
        } finally {
            setLoading(false);
        }
    }, [plateSep]);

    useEffect(() => {
        const timer = setTimeout(compute, 400);
        return () => clearTimeout(timer);
    }, [compute]);

    return (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
            <PageHeader
                title="Zero-Point Energy"
                subtitle="Casimir effect, vacuum fluctuations, and exotic matter constraints"
                equation="F/A = -π²ℏc / (240 d⁴)"
            />

            <div className="grid grid-cols-12 gap-5">
                <div className="col-span-3">
                    <GlassPanel className="space-y-6">
                        <h3 className="text-xs font-bold uppercase tracking-widest text-white/30">Parameters</h3>
                        <ParamSlider label="Plate Separation" value={plateSep} min={1} max={1000} step={1} onChange={setPlateSep} unit="nm" />

                        <div className="glow-line" />

                        {data && (
                            <div className="space-y-3">
                                <MetricCard label="Casimir Force" value={formatScientific(data.casimir_force_pa)} unit="Pa" accent="cyan" icon={<Zap className="w-3.5 h-3.5" />} />
                                <MetricCard label="Energy Density" value={formatScientific(data.casimir_energy_density)} unit="J/m³" accent="cyan" icon={<FlaskConical className="w-3.5 h-3.5" />} />
                                <MetricCard label="ZPE Density (Planck)" value={formatScientific(data.zpe_density)} unit="J/m³" accent="amber" icon={<AlertTriangle className="w-3.5 h-3.5" />} />
                                <MetricCard label="Cosmo Discrepancy" value={`10^${data.cosmological_discrepancy.log10_ratio.toFixed(0)}`} accent="red" icon={<Scale className="w-3.5 h-3.5" />} />
                                <MetricCard label="QI Bound (1 fs)" value={formatScientific(data.qi_bound)} unit="J/m³" accent="amber" />

                                <div className="glow-line" />

                                <div className="text-xs text-white/30 space-y-1.5">
                                    <p className="font-bold text-white/50 uppercase tracking-wider">Lamoreaux (1997)</p>
                                    <p>Theory: {formatScientific(data.lamoreaux.theory_Pa)} Pa</p>
                                    <p>Experiment: {formatScientific(data.lamoreaux.experiment_Pa)} Pa</p>
                                    <p>Error: {(data.lamoreaux.relative_error * 100).toFixed(1)}%</p>
                                </div>
                            </div>
                        )}
                    </GlassPanel>
                </div>

                <div className="col-span-9 space-y-5">
                    {error && (
                        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>
                    )}

                    <div className="grid grid-cols-2 gap-5">
                        {/* Casimir Force Sweep */}
                        <GlassPanel className="relative">
                            {loading && <LoadingOverlay />}
                            <h3 className="text-xs font-bold uppercase tracking-widest text-white/30 mb-4">Casimir Force vs Separation</h3>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "scatter" as const,
                                        x: data.sweep_d.map((d) => d * 1e9),
                                        y: data.sweep_force.map((f) => Math.abs(f)),
                                        mode: "lines" as const,
                                        line: { color: "#06b6d4", width: 2 },
                                        fill: "tozeroy" as const,
                                        fillcolor: "rgba(6,182,212,0.06)",
                                    }]}
                                    layout={{
                                        ...darkLayout,
                                        height: 340,
                                        xaxis: { ...darkLayout.xaxis, title: "Separation [nm]", type: "log" as const },
                                        yaxis: { ...darkLayout.yaxis, title: "|F/A| [Pa]", type: "log" as const },
                                    }}
                                    config={{ responsive: true }}
                                    style={{ width: "100%", height: 340 }}
                                />
                            )}
                        </GlassPanel>

                        {/* Casimir Energy Sweep */}
                        <GlassPanel className="relative">
                            {loading && <LoadingOverlay />}
                            <h3 className="text-xs font-bold uppercase tracking-widest text-white/30 mb-4">Vacuum Energy Density vs Separation</h3>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "scatter" as const,
                                        x: data.sweep_d.map((d) => d * 1e9),
                                        y: data.sweep_energy.map((e) => Math.abs(e)),
                                        mode: "lines" as const,
                                        line: { color: "#a855f7", width: 2 },
                                        fill: "tozeroy" as const,
                                        fillcolor: "rgba(168,85,247,0.06)",
                                    }]}
                                    layout={{
                                        ...darkLayout,
                                        height: 340,
                                        xaxis: { ...darkLayout.xaxis, title: "Separation [nm]", type: "log" as const },
                                        yaxis: { ...darkLayout.yaxis, title: "|u| [J/m³]", type: "log" as const },
                                    }}
                                    config={{ responsive: true }}
                                    style={{ width: "100%", height: 340 }}
                                />
                            )}
                        </GlassPanel>
                    </div>

                    {/* Spectral Density */}
                    <GlassPanel className="relative">
                        {loading && <LoadingOverlay />}
                        <h3 className="text-xs font-bold uppercase tracking-widest text-white/30 mb-4">ZPE Spectral Density u(ω)</h3>
                        {data && (
                            <Plot
                                data={[{
                                    type: "scatter" as const,
                                    x: data.spectral_omega,
                                    y: data.spectral_density,
                                    mode: "lines" as const,
                                    line: { color: "#f59e0b", width: 2 },
                                    fill: "tozeroy" as const,
                                    fillcolor: "rgba(245,158,11,0.06)",
                                }]}
                                layout={{
                                    ...darkLayout,
                                    height: 300,
                                    xaxis: { ...darkLayout.xaxis, title: "ω [rad/s]", type: "log" as const },
                                    yaxis: { ...darkLayout.yaxis, title: "u(ω) [J/m³ per rad/s]", type: "log" as const },
                                }}
                                config={{ responsive: true }}
                                style={{ width: "100%", height: 300 }}
                            />
                        )}
                    </GlassPanel>
                </div>
            </div>
        </motion.div>
    );
}
