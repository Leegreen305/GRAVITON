"use client";

import { useState, useEffect, useRef } from "react";
import Plot from "@/components/PlotWrapper";
import { darkLayout } from "@/components/PlotWrapper";
import { PageHeader, ParamSlider, MetricCard, Panel, LoadingOverlay, Divider } from "@/components/ui";
import { fetchAPI, formatScientific } from "@/lib/api";

export default function GeodesicPage() {
    const [mass, setMass] = useState(10);
    const [spin, setSpin] = useState(0.0);
    const [r0, setR0] = useState(12);
    const [orbits, setOrbits] = useState(5);
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

    useEffect(() => {
        if (timer.current) clearTimeout(timer.current);
        timer.current = setTimeout(async () => {
            setLoading(true);
            try {
                const res = await fetchAPI("/api/geodesic", {
                    mass_solar: mass, spin_parameter: spin, initial_r_over_rs: r0, num_orbits: orbits,
                });
                setData(res);
            } catch { }
            setLoading(false);
        }, 500);
        return () => { if (timer.current) clearTimeout(timer.current); };
    }, [mass, spin, r0, orbits]);

    return (
        <div className="max-w-[1100px] animate-in">
            <PageHeader
                title="Geodesic Motion"
                subtitle="Schwarzschild & Kerr black hole orbits"
                equation="d\u00b2x\u1d58/d\u03c4\u00b2 + \u0393\u1d58\u2090\u1d66 dx\u1d43dx\u1d47/d\u03c4\u00b2 = 0"
            />

            <div className="grid grid-cols-[240px_1fr] gap-5">
                {/* Controls */}
                <div className="space-y-4">
                    <Panel>
                        <p className="section-label mb-3">Parameters</p>
                        <div className="space-y-4">
                            <ParamSlider label="Mass" value={mass} min={1} max={100} step={1} unit="M\u2609" onChange={setMass} />
                            <ParamSlider label="Spin a/M" value={spin} min={0} max={0.99} step={0.01} onChange={setSpin} />
                            <ParamSlider label="Initial r/r\u209b" value={r0} min={4} max={30} step={0.5} onChange={setR0} />
                            <ParamSlider label="Orbits" value={orbits} min={1} max={20} step={1} onChange={setOrbits} />
                        </div>
                    </Panel>

                    {data && (
                        <Panel>
                            <p className="section-label mb-2">Results</p>
                            <MetricCard label="Metric" value={data.metrics.metric_type} />
                            <Divider />
                            <MetricCard label="ISCO" value={formatScientific(data.metrics.isco_radius)} unit="m" />
                            <Divider />
                            <MetricCard label="Schwarzschild r\u209b" value={formatScientific(data.metrics.schwarzschild_radius)} unit="m" />
                            {data.metrics.horizons && (
                                <>
                                    <Divider />
                                    <MetricCard label="r+" value={formatScientific(data.metrics.horizons.r_plus)} unit="m" />
                                    <Divider />
                                    <MetricCard label="r\u2013" value={formatScientific(data.metrics.horizons.r_minus)} unit="m" />
                                </>
                            )}
                        </Panel>
                    )}
                </div>

                {/* Plots */}
                <div className="space-y-4">
                    <Panel className="relative">
                        {loading && <LoadingOverlay />}
                        <p className="section-label mb-2">Orbit Trajectory</p>
                        {data && (
                            <Plot
                                data={[
                                    {
                                        type: "scatter",
                                        x: data.orbit_x,
                                        y: data.orbit_y,
                                        mode: "lines",
                                        line: { color: "#3b82f6", width: 1 },
                                        name: "Orbit",
                                    },
                                    {
                                        type: "scatter",
                                        x: [0], y: [0],
                                        mode: "markers",
                                        marker: { color: "#ffffff", size: 6, symbol: "circle" },
                                        name: "BH",
                                        showlegend: false,
                                    },
                                ]}
                                layout={{
                                    ...darkLayout,
                                    height: 360,
                                    xaxis: { ...darkLayout.xaxis, scaleanchor: "y", title: { text: "x (m)", font: { size: 9, color: "rgba(255,255,255,0.2)" } } },
                                    yaxis: { ...darkLayout.yaxis, title: { text: "y (m)", font: { size: 9, color: "rgba(255,255,255,0.2)" } } },
                                    showlegend: false,
                                }}
                                config={{ displayModeBar: false, responsive: true }}
                                style={{ width: "100%", height: "360px" }}
                            />
                        )}
                    </Panel>

                    <Panel className="relative">
                        <p className="section-label mb-2">Effective Potential</p>
                        {data && (
                            <Plot
                                data={[
                                    {
                                        type: "scatter",
                                        x: data.potential_r,
                                        y: data.potential_V,
                                        mode: "lines",
                                        line: { color: "#a855f7", width: 1.5 },
                                        name: "V_eff",
                                    },
                                    ...(data.isco_line ? [{
                                        type: "scatter" as const,
                                        x: [data.isco_line, data.isco_line],
                                        y: [Math.min(...data.potential_V), Math.max(...data.potential_V)],
                                        mode: "lines" as const,
                                        line: { color: "rgba(255,255,255,0.12)", width: 1, dash: "dot" as const },
                                        name: "ISCO",
                                        showlegend: false,
                                    }] : []),
                                ]}
                                layout={{
                                    ...darkLayout,
                                    height: 240,
                                    xaxis: { ...darkLayout.xaxis, title: { text: "r (m)", font: { size: 9, color: "rgba(255,255,255,0.2)" } } },
                                    yaxis: { ...darkLayout.yaxis, title: { text: "V_eff", font: { size: 9, color: "rgba(255,255,255,0.2)" } } },
                                    showlegend: false,
                                }}
                                config={{ displayModeBar: false, responsive: true }}
                                style={{ width: "100%", height: "240px" }}
                            />
                        )}
                    </Panel>
                </div>
            </div>
        </div>
    );
}
