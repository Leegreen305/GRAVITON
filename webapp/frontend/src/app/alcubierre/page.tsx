"use client";

import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import { AlertTriangle, Thermometer, Gauge, ShieldAlert } from "lucide-react";
import Plot from "../../components/PlotWrapper";
import { darkLayout, cyanColorscale, energyColorscale } from "../../components/PlotWrapper";
import { MetricCard, ParamSlider, GlassPanel, PageHeader, LoadingOverlay } from "../../components/ui";
import { fetchAPI, formatScientific } from "../../lib/api";

interface AlcubierreData {
    expansion_scalar: number[][];
    energy_density: number[][];
    shape_profile_r: number[];
    shape_profile_f: number[];
    total_exotic_energy: number;
    pfenning_ford_bound: number;
    hawking_temperature: number;
    is_causally_disconnected: boolean;
    energy_comparisons: Record<string, number>;
    x_coords: number[];
    y_coords: number[];
}

export default function AlcubierrePage() {
    const [velocity, setVelocity] = useState(1.0);
    const [radius, setRadius] = useState(100);
    const [sigma, setSigma] = useState(8);
    const [data, setData] = useState<AlcubierreData | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const compute = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await fetchAPI<AlcubierreData>("/api/alcubierre", {
                velocity, radius, sigma, grid_n: 60,
            });
            setData(result);
        } catch (e: unknown) {
            setError(e instanceof Error ? e.message : "Computation failed");
        } finally {
            setLoading(false);
        }
    }, [velocity, radius, sigma]);

    useEffect(() => {
        const timer = setTimeout(compute, 400);
        return () => clearTimeout(timer);
    }, [compute]);

    return (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
            <PageHeader
                title="Alcubierre Warp Drive"
                subtitle="Exotic matter requirements for superluminal spacetime bubbles"
                equation="ds² = -c²dt² + (dx - v_s f(r_s) dt)² + dy² + dz²"
            />

            <div className="grid grid-cols-12 gap-5">
                {/* Parameter Panel */}
                <div className="col-span-3">
                    <GlassPanel className="space-y-6">
                        <h3 className="text-xs font-bold uppercase tracking-widest text-white/30">Parameters</h3>
                        <ParamSlider label="Warp Velocity" value={velocity} min={0.1} max={2.0} step={0.05} onChange={setVelocity} unit="c" />
                        <ParamSlider label="Bubble Radius" value={radius} min={10} max={500} step={10} onChange={setRadius} unit="m" />
                        <ParamSlider label="Wall Thickness σ" value={sigma} min={1} max={30} step={0.5} onChange={setSigma} />

                        <div className="glow-line" />

                        {data && (
                            <div className="space-y-3">
                                <MetricCard label="Total Exotic Energy" value={formatScientific(data.total_exotic_energy)} unit="J" accent="red" icon={<AlertTriangle className="w-3.5 h-3.5" />} />
                                <MetricCard label="Pfenning-Ford Bound" value={formatScientific(data.pfenning_ford_bound)} unit="J" accent="amber" icon={<Gauge className="w-3.5 h-3.5" />} />
                                <MetricCard label="Hawking Temperature" value={formatScientific(data.hawking_temperature)} unit="K" accent="cyan" icon={<Thermometer className="w-3.5 h-3.5" />} />
                                <MetricCard
                                    label="Causal Status"
                                    value={data.is_causally_disconnected ? "Disconnected" : "Connected"}
                                    accent={data.is_causally_disconnected ? "red" : "green"}
                                    icon={<ShieldAlert className="w-3.5 h-3.5" />}
                                />
                            </div>
                        )}
                    </GlassPanel>
                </div>

                {/* Visualizations */}
                <div className="col-span-9 space-y-5">
                    {error && (
                        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>
                    )}

                    {/* Expansion Scalar 3D Surface */}
                    <GlassPanel className="relative">
                        {loading && <LoadingOverlay />}
                        <h3 className="text-xs font-bold uppercase tracking-widest text-white/30 mb-4">Expansion Scalar θ — Z=0 Plane</h3>
                        {data && (
                            <Plot
                                data={[{
                                    type: "surface" as const,
                                    z: data.expansion_scalar,
                                    x: data.x_coords,
                                    y: data.y_coords,
                                    colorscale: cyanColorscale,
                                    showscale: true,
                                    colorbar: { tickfont: { color: "rgba(255,255,255,0.4)", size: 9 }, thickness: 12, len: 0.6 },
                                }]}
                                layout={{
                                    ...darkLayout,
                                    height: 420,
                                    scene: {
                                        xaxis: { title: "x [m]", gridcolor: "rgba(255,255,255,0.04)", color: "rgba(255,255,255,0.4)" },
                                        yaxis: { title: "y [m]", gridcolor: "rgba(255,255,255,0.04)", color: "rgba(255,255,255,0.4)" },
                                        zaxis: { title: "θ", gridcolor: "rgba(255,255,255,0.04)", color: "rgba(255,255,255,0.4)" },
                                        bgcolor: "rgba(0,0,0,0)",
                                        camera: { eye: { x: 1.5, y: 1.5, z: 1.2 } },
                                    },
                                    margin: { l: 0, r: 0, t: 10, b: 0 },
                                }}
                                config={{ displayModeBar: true, responsive: true }}
                                style={{ width: "100%", height: 420 }}
                            />
                        )}
                    </GlassPanel>

                    <div className="grid grid-cols-2 gap-5">
                        {/* Energy Density Heatmap */}
                        <GlassPanel className="relative">
                            {loading && <LoadingOverlay />}
                            <h3 className="text-xs font-bold uppercase tracking-widest text-white/30 mb-4">Energy Density T₀₀</h3>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "heatmap" as const,
                                        z: data.energy_density,
                                        x: data.x_coords,
                                        y: data.y_coords,
                                        colorscale: energyColorscale,
                                        showscale: true,
                                        colorbar: { tickfont: { color: "rgba(255,255,255,0.4)", size: 9 }, thickness: 10 },
                                    }]}
                                    layout={{
                                        ...darkLayout,
                                        height: 340,
                                        xaxis: { ...darkLayout.xaxis, title: "x [m]" },
                                        yaxis: { ...darkLayout.yaxis, title: "y [m]", scaleanchor: "x" },
                                    }}
                                    config={{ responsive: true }}
                                    style={{ width: "100%", height: 340 }}
                                />
                            )}
                        </GlassPanel>

                        {/* Shape Function Profile */}
                        <GlassPanel className="relative">
                            {loading && <LoadingOverlay />}
                            <h3 className="text-xs font-bold uppercase tracking-widest text-white/30 mb-4">Shape Function f(r)</h3>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "scatter" as const,
                                        x: data.shape_profile_r,
                                        y: data.shape_profile_f,
                                        mode: "lines" as const,
                                        line: { color: "#06b6d4", width: 2 },
                                        fill: "tozeroy" as const,
                                        fillcolor: "rgba(6,182,212,0.08)",
                                    }]}
                                    layout={{
                                        ...darkLayout,
                                        height: 340,
                                        xaxis: { ...darkLayout.xaxis, title: "r [m]" },
                                        yaxis: { ...darkLayout.yaxis, title: "f(r)", range: [-0.05, 1.1] },
                                    }}
                                    config={{ responsive: true }}
                                    style={{ width: "100%", height: 340 }}
                                />
                            )}
                        </GlassPanel>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
