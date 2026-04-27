"use client";

import { useState, useEffect, useRef } from "react";
import Plot from "@/components/PlotWrapper";
import { darkLayout } from "@/components/PlotWrapper";
import { PageHeader, ParamSlider, MetricCard, Panel, LoadingOverlay, Divider } from "@/components/ui";
import { fetchAPI, formatScientific } from "@/lib/api";

export default function ZPEPage() {
    const [separation, setSeparation] = useState(100);
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

    useEffect(() => {
        if (timer.current) clearTimeout(timer.current);
        timer.current = setTimeout(async () => {
            setLoading(true);
            try {
                const res = await fetchAPI("/api/zpe", { plate_separation: separation * 1e-9 });
                setData(res);
            } catch { }
            setLoading(false);
        }, 400);
        return () => { if (timer.current) clearTimeout(timer.current); };
    }, [separation]);

    return (
        <div className="max-w-[1100px] animate-in">
            <PageHeader
                title="Zero-Point Energy"
                subtitle="Casimir vacuum fluctuations and quantum bounds"
                equation="F/A = -\u03c0\u00b2\u0127c / (240 d\u2074)"
            />

            <div className="grid grid-cols-[240px_1fr] gap-5">
                <div className="space-y-4">
                    <Panel>
                        <p className="section-label mb-3">Parameters</p>
                        <ParamSlider label="Plate Separation" value={separation} min={1} max={1000} step={1} unit="nm" onChange={setSeparation} />
                    </Panel>

                    {data && (
                        <Panel>
                            <p className="section-label mb-2">Results</p>
                            <MetricCard label="Casimir Force" value={formatScientific(data.casimir_force_pa)} unit="N/m\u00b2" />
                            <Divider />
                            <MetricCard label="Energy Density" value={formatScientific(data.casimir_energy_density)} unit="J/m\u00b3" tone="negative" />
                            <Divider />
                            <MetricCard label="ZPE Density" value={formatScientific(data.zpe_density)} unit="J/m\u00b3" />
                            <Divider />
                            <MetricCard label="Cosmological \u0394" value={formatScientific(data.cosmological_discrepancy?.discrepancy_factor)} tone="caution" />
                            <Divider />
                            <MetricCard label="QI Bound" value={formatScientific(data.qi_bound)} unit="J/m\u00b3" />
                            <Divider />
                            <MetricCard label="Lamoreaux Ratio" value={data.lamoreaux?.ratio?.toFixed(2) ?? "\u2014"} tone="positive" />
                        </Panel>
                    )}
                </div>

                <div className="space-y-4">
                    <Panel className="relative">
                        {loading && <LoadingOverlay />}
                        <p className="section-label mb-2">Casimir Force vs Separation</p>
                        {data && (
                            <Plot
                                data={[{
                                    type: "scatter",
                                    x: data.sweep_d,
                                    y: data.sweep_force,
                                    mode: "lines",
                                    line: { color: "#3b82f6", width: 1.5 },
                                }]}
                                layout={{
                                    ...darkLayout,
                                    height: 260,
                                    xaxis: { ...darkLayout.xaxis, type: "log", title: { text: "d (m)", font: { size: 9, color: "rgba(255,255,255,0.2)" } } },
                                    yaxis: { ...darkLayout.yaxis, type: "log", title: { text: "F/A (N/m\u00b2)", font: { size: 9, color: "rgba(255,255,255,0.2)" } } },
                                }}
                                config={{ displayModeBar: false, responsive: true }}
                                style={{ width: "100%", height: "260px" }}
                            />
                        )}
                    </Panel>

                    <div className="grid grid-cols-2 gap-4">
                        <Panel className="relative">
                            <p className="section-label mb-2">Vacuum Energy Sweep</p>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "scatter",
                                        x: data.sweep_d,
                                        y: data.sweep_energy,
                                        mode: "lines",
                                        line: { color: "#a855f7", width: 1.5 },
                                        fill: "tozeroy",
                                        fillcolor: "rgba(168,85,247,0.05)",
                                    }]}
                                    layout={{
                                        ...darkLayout,
                                        height: 220,
                                        margin: { l: 44, r: 8, t: 8, b: 32 },
                                        xaxis: { ...darkLayout.xaxis, type: "log" },
                                        yaxis: { ...darkLayout.yaxis, type: "log" },
                                    }}
                                    config={{ displayModeBar: false, responsive: true }}
                                    style={{ width: "100%", height: "220px" }}
                                />
                            )}
                        </Panel>

                        <Panel className="relative">
                            <p className="section-label mb-2">ZPE Spectral Density</p>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "scatter",
                                        x: data.spectral_omega,
                                        y: data.spectral_density,
                                        mode: "lines",
                                        line: { color: "#f59e0b", width: 1.5 },
                                        fill: "tozeroy",
                                        fillcolor: "rgba(245,158,11,0.05)",
                                    }]}
                                    layout={{
                                        ...darkLayout,
                                        height: 220,
                                        margin: { l: 44, r: 8, t: 8, b: 32 },
                                        xaxis: { ...darkLayout.xaxis, type: "log", title: { text: "\u03c9 (rad/s)", font: { size: 9, color: "rgba(255,255,255,0.2)" } } },
                                        yaxis: { ...darkLayout.yaxis, type: "log" },
                                    }}
                                    config={{ displayModeBar: false, responsive: true }}
                                    style={{ width: "100%", height: "220px" }}
                                />
                            )}
                        </Panel>
                    </div>
                </div>
            </div>
        </div>
    );
}
