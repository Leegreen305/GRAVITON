"use client";

import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import { Orbit, CircleDot, Target } from "lucide-react";
import Plot from "../../components/PlotWrapper";
import { darkLayout } from "../../components/PlotWrapper";
import { MetricCard, ParamSlider, GlassPanel, PageHeader, LoadingOverlay } from "../../components/ui";
import { fetchAPI, formatScientific } from "../../lib/api";

interface GeodesicData {
    orbit_x: number[];
    orbit_y: number[];
    orbit_r: number[];
    orbit_phi: number[];
    potential_r: number[];
    potential_V: number[];
    isco: number;
    schwarzschild_radius: number;
    metric_type: string;
    outer_horizon?: number;
    inner_horizon?: number;
}

export default function GeodesicPage() {
    const [massSolar, setMassSolar] = useState(10);
    const [spin, setSpin] = useState(0);
    const [rFactor, setRFactor] = useState(10);
    const [nOrbits, setNOrbits] = useState(5);
    const [data, setData] = useState<GeodesicData | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const compute = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await fetchAPI<GeodesicData>("/api/geodesic", {
                mass_solar: massSolar,
                spin,
                r_init_factor: rFactor,
                phi_init: 0,
                n_orbits: nOrbits,
            });
            setData(result);
        } catch (e: unknown) {
            setError(e instanceof Error ? e.message : "Computation failed");
        } finally {
            setLoading(false);
        }
    }, [massSolar, spin, rFactor, nOrbits]);

    useEffect(() => {
        const timer = setTimeout(compute, 500);
        return () => clearTimeout(timer);
    }, [compute]);

    return (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
            <PageHeader
                title="Geodesic Motion"
                subtitle="Schwarzschild and Kerr black hole orbits"
                equation="d²xᵘ/dτ² + Γᵘₐᵦ dxᵃ/dτ dxᵦ/dτ = 0"
            />

            <div className="grid grid-cols-12 gap-5">
                <div className="col-span-3">
                    <GlassPanel className="space-y-6">
                        <h3 className="text-xs font-bold uppercase tracking-widest text-white/30">Parameters</h3>
                        <ParamSlider label="Mass" value={massSolar} min={1} max={100} step={1} onChange={setMassSolar} unit="M☉" />
                        <ParamSlider
                            label="Spin a*"
                            value={spin}
                            min={0}
                            max={0.99}
                            step={0.01}
                            onChange={setSpin}
                            formatValue={(v) => v === 0 ? "0 (Schwarzschild)" : v.toFixed(2)}
                        />
                        <ParamSlider label="Initial r / r_s" value={rFactor} min={4} max={30} step={1} onChange={setRFactor} />
                        <ParamSlider label="Orbits" value={nOrbits} min={1} max={20} step={1} onChange={setNOrbits} />

                        <div className="glow-line" />

                        {data && (
                            <div className="space-y-3">
                                <MetricCard label="Metric" value={data.metric_type} accent="cyan" icon={<Orbit className="w-3.5 h-3.5" />} />
                                <MetricCard label="ISCO" value={formatScientific(data.isco)} unit="m" accent="amber" icon={<Target className="w-3.5 h-3.5" />} />
                                <MetricCard label="Schwarzschild r_s" value={formatScientific(data.schwarzschild_radius)} unit="m" accent="cyan" icon={<CircleDot className="w-3.5 h-3.5" />} />
                                {data.outer_horizon !== undefined && data.outer_horizon !== null && (
                                    <MetricCard label="Outer Horizon r₊" value={formatScientific(data.outer_horizon)} unit="m" accent="red" />
                                )}
                                {data.inner_horizon !== undefined && data.inner_horizon !== null && (
                                    <MetricCard label="Inner Horizon r₋" value={formatScientific(data.inner_horizon)} unit="m" accent="amber" />
                                )}
                            </div>
                        )}
                    </GlassPanel>
                </div>

                <div className="col-span-9 space-y-5">
                    {error && (
                        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>
                    )}

                    {/* Orbit Plot */}
                    <GlassPanel className="relative">
                        {loading && <LoadingOverlay />}
                        <h3 className="text-xs font-bold uppercase tracking-widest text-white/30 mb-4">Equatorial Orbit</h3>
                        {data && (
                            <Plot
                                data={[
                                    {
                                        type: "scatter" as const,
                                        x: data.orbit_x,
                                        y: data.orbit_y,
                                        mode: "lines" as const,
                                        line: { color: "#06b6d4", width: 1.5 },
                                        name: "Orbit",
                                    },
                                    {
                                        type: "scatter" as const,
                                        x: [0],
                                        y: [0],
                                        mode: "markers" as const,
                                        marker: { color: "#ffffff", size: 8, symbol: "circle" },
                                        name: "Black Hole",
                                    },
                                ]}
                                layout={{
                                    ...darkLayout,
                                    height: 450,
                                    xaxis: { ...darkLayout.xaxis, title: "x [m]", scaleanchor: "y" },
                                    yaxis: { ...darkLayout.yaxis, title: "y [m]" },
                                    showlegend: true,
                                }}
                                config={{ responsive: true }}
                                style={{ width: "100%", height: 450 }}
                            />
                        )}
                    </GlassPanel>

                    {/* Effective Potential */}
                    <GlassPanel className="relative">
                        {loading && <LoadingOverlay />}
                        <h3 className="text-xs font-bold uppercase tracking-widest text-white/30 mb-4">Effective Potential V_eff(r)</h3>
                        {data && (
                            <Plot
                                data={[
                                    {
                                        type: "scatter" as const,
                                        x: data.potential_r,
                                        y: data.potential_V,
                                        mode: "lines" as const,
                                        line: { color: "#f59e0b", width: 2 },
                                        name: "V_eff",
                                    },
                                    {
                                        type: "scatter" as const,
                                        x: [data.isco, data.isco],
                                        y: [Math.min(...data.potential_V), Math.max(...data.potential_V)],
                                        mode: "lines" as const,
                                        line: { color: "#ef4444", width: 1, dash: "dash" },
                                        name: "ISCO",
                                    },
                                ]}
                                layout={{
                                    ...darkLayout,
                                    height: 320,
                                    xaxis: { ...darkLayout.xaxis, title: "r [m]" },
                                    yaxis: { ...darkLayout.yaxis, title: "V_eff [J/kg]" },
                                    showlegend: true,
                                }}
                                config={{ responsive: true }}
                                style={{ width: "100%", height: 320 }}
                            />
                        )}
                    </GlassPanel>
                </div>
            </div>
        </motion.div>
    );
}
