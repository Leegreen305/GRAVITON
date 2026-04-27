"use client";

import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import { Atom, Timer, Clock } from "lucide-react";
import Plot from "../../components/PlotWrapper";
import { darkLayout, cyanColorscale } from "../../components/PlotWrapper";
import { MetricCard, ParamSlider, GlassPanel, PageHeader, LoadingOverlay } from "../../components/ui";
import { fetchAPI, formatScientific } from "../../lib/api";

interface GEMData {
    Eg_magnitude: number;
    Bg_magnitude: number;
    lt_precession_rate: number;
    time_dilation: number;
    Eg_field: number[][];
    Bg_field: number[][];
    x_coords: number[];
    y_coords: number[];
}

const presets = [
    { name: "Earth", mass: 5.972e24, radius: 6.371e6, J: 7.07e33 },
    { name: "Neutron Star", mass: 2.8e30, radius: 1e4, J: 1e40 },
    { name: "Black Hole (10 M☉)", mass: 1.989e31, radius: 2.95e4, J: 1e42 },
];

export default function GravitomagneticPage() {
    const [presetIdx, setPresetIdx] = useState(0);
    const [mass, setMass] = useState(presets[0].mass);
    const [radius, setRadius] = useState(presets[0].radius);
    const [angMom, setAngMom] = useState(presets[0].J);
    const [data, setData] = useState<GEMData | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const applyPreset = (idx: number) => {
        setPresetIdx(idx);
        setMass(presets[idx].mass);
        setRadius(presets[idx].radius);
        setAngMom(presets[idx].J);
    };

    const compute = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await fetchAPI<GEMData>("/api/gravitomagnetic", {
                mass, radius, angular_momentum_z: angMom,
            });
            setData(result);
        } catch (e: unknown) {
            setError(e instanceof Error ? e.message : "Computation failed");
        } finally {
            setLoading(false);
        }
    }, [mass, radius, angMom]);

    useEffect(() => {
        const timer = setTimeout(compute, 400);
        return () => clearTimeout(timer);
    }, [compute]);

    return (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
            <PageHeader
                title="Gravitoelectromagnetism"
                subtitle="Linearized GR: Maxwell-like equations for gravity"
                equation="F = m(E_g + v × B_g)"
            />

            <div className="grid grid-cols-12 gap-5">
                <div className="col-span-3">
                    <GlassPanel className="space-y-6">
                        <h3 className="text-xs font-bold uppercase tracking-widest text-white/30">Presets</h3>
                        <div className="flex gap-2 flex-wrap">
                            {presets.map((p, i) => (
                                <button
                                    key={i}
                                    onClick={() => applyPreset(i)}
                                    className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${presetIdx === i
                                            ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                                            : "bg-white/[0.03] text-white/40 border border-white/[0.06] hover:text-white/60"
                                        }`}
                                >
                                    {p.name}
                                </button>
                            ))}
                        </div>

                        <div className="glow-line" />
                        <h3 className="text-xs font-bold uppercase tracking-widest text-white/30">Parameters</h3>
                        <ParamSlider label="Log₁₀ Mass" value={Math.log10(mass)} min={20} max={35} step={0.5} onChange={(v) => setMass(Math.pow(10, v))} formatValue={(v) => `10^${v.toFixed(1)}`} unit="kg" />
                        <ParamSlider label="Log₁₀ Radius" value={Math.log10(radius)} min={3} max={8} step={0.25} onChange={(v) => setRadius(Math.pow(10, v))} formatValue={(v) => `10^${v.toFixed(1)}`} unit="m" />
                        <ParamSlider label="Log₁₀ J_z" value={Math.log10(angMom)} min={30} max={45} step={0.5} onChange={(v) => setAngMom(Math.pow(10, v))} formatValue={(v) => `10^${v.toFixed(1)}`} unit="kg m²/s" />

                        <div className="glow-line" />

                        {data && (
                            <div className="space-y-3">
                                <MetricCard label="Gravitoelectric |E_g|" value={formatScientific(data.Eg_magnitude)} unit="m/s²" accent="cyan" icon={<Atom className="w-3.5 h-3.5" />} />
                                <MetricCard label="Gravitomagnetic |B_g|" value={formatScientific(data.Bg_magnitude)} unit="1/s" accent="cyan" icon={<Atom className="w-3.5 h-3.5" />} />
                                <MetricCard label="LT Precession" value={formatScientific(data.lt_precession_rate)} unit="rad/s" accent="amber" icon={<Timer className="w-3.5 h-3.5" />} />
                                <MetricCard label="Time Dilation dτ/dt" value={data.time_dilation.toFixed(12)} accent="green" icon={<Clock className="w-3.5 h-3.5" />} />
                            </div>
                        )}
                    </GlassPanel>
                </div>

                <div className="col-span-9 space-y-5">
                    {error && (
                        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>
                    )}

                    <div className="grid grid-cols-2 gap-5">
                        <GlassPanel className="relative">
                            {loading && <LoadingOverlay />}
                            <h3 className="text-xs font-bold uppercase tracking-widest text-white/30 mb-4">Gravitoelectric Field |E_g|</h3>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "heatmap" as const,
                                        z: data.Eg_field,
                                        x: data.x_coords,
                                        y: data.y_coords,
                                        colorscale: cyanColorscale,
                                        showscale: true,
                                        colorbar: { tickfont: { color: "rgba(255,255,255,0.4)", size: 9 }, thickness: 10 },
                                    }]}
                                    layout={{
                                        ...darkLayout,
                                        height: 400,
                                        xaxis: { ...darkLayout.xaxis, title: "x [m]" },
                                        yaxis: { ...darkLayout.yaxis, title: "y [m]", scaleanchor: "x" },
                                    }}
                                    config={{ responsive: true }}
                                    style={{ width: "100%", height: 400 }}
                                />
                            )}
                        </GlassPanel>

                        <GlassPanel className="relative">
                            {loading && <LoadingOverlay />}
                            <h3 className="text-xs font-bold uppercase tracking-widest text-white/30 mb-4">Gravitomagnetic Field |B_g|</h3>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "heatmap" as const,
                                        z: data.Bg_field,
                                        x: data.x_coords,
                                        y: data.y_coords,
                                        colorscale: [
                                            [0, "#0a0a14"],
                                            [0.2, "#1a0040"],
                                            [0.4, "#4400aa"],
                                            [0.6, "#8800dd"],
                                            [0.8, "#cc44ff"],
                                            [1, "#ffffff"],
                                        ],
                                        showscale: true,
                                        colorbar: { tickfont: { color: "rgba(255,255,255,0.4)", size: 9 }, thickness: 10 },
                                    }]}
                                    layout={{
                                        ...darkLayout,
                                        height: 400,
                                        xaxis: { ...darkLayout.xaxis, title: "x [m]" },
                                        yaxis: { ...darkLayout.yaxis, title: "y [m]", scaleanchor: "x" },
                                    }}
                                    config={{ responsive: true }}
                                    style={{ width: "100%", height: 400 }}
                                />
                            )}
                        </GlassPanel>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
