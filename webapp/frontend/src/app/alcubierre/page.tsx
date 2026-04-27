"use client";

import { useState, useEffect, useRef } from "react";
import Plot from "@/components/PlotWrapper";
import { darkLayout, blueScale, heatScale } from "@/components/PlotWrapper";
import { PageHeader, ParamSlider, MetricCard, Panel, LoadingOverlay, Divider } from "@/components/ui";
import { fetchAPI, formatScientific } from "@/lib/api";

export default function AlcubierrePage() {
    const [v, setV] = useState(0.5);
    const [R, setR] = useState(100);
    const [sigma, setSigma] = useState(8);
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

    useEffect(() => {
        if (timer.current) clearTimeout(timer.current);
        timer.current = setTimeout(async () => {
            setLoading(true);
            try {
                const res = await fetchAPI("/api/alcubierre", { velocity: v, radius: R, sigma });
                setData(res);
            } catch { }
            setLoading(false);
        }, 400);
        return () => { if (timer.current) clearTimeout(timer.current); };
    }, [v, R, sigma]);

    const causal = data?.is_causally_disconnected ? "Disconnected" : "Causal";

    return (
        <div className="max-w-[1100px] animate-in">
            <PageHeader
                title="Alcubierre Warp Drive"
                subtitle="ADM 3+1 decomposition of the warp metric"
                equation="ds\u00b2 = -c\u00b2dt\u00b2 + (dx - v\u209bf dt)\u00b2"
            />

            <div className="grid grid-cols-[240px_1fr] gap-5">
                <div className="space-y-4">
                    <Panel>
                        <p className="section-label mb-3">Parameters</p>
                        <div className="space-y-4">
                            <ParamSlider label="Velocity" value={v} min={0.1} max={2} step={0.01} unit="c" onChange={setV} />
                            <ParamSlider label="Radius" value={R} min={10} max={500} step={1} unit="m" onChange={setR} />
                            <ParamSlider label="Sigma" value={sigma} min={1} max={30} step={0.5} onChange={setSigma} />
                        </div>
                    </Panel>

                    {data && (
                        <Panel>
                            <p className="section-label mb-2">Results</p>
                            <MetricCard label="Exotic Energy" value={formatScientific(data.total_exotic_energy)} unit="J" tone="negative" />
                            <Divider />
                            <MetricCard label="Pfenning-Ford" value={formatScientific(data.pfenning_ford_bound)} unit="J" />
                            <Divider />
                            <MetricCard label="Hawking Temp" value={formatScientific(data.hawking_temperature)} unit="K" tone="caution" />
                            <Divider />
                            <MetricCard label="Causality" value={causal} tone={causal === "Causal" ? "positive" : "negative"} />
                        </Panel>
                    )}
                </div>

                <div className="space-y-4">
                    <Panel className="relative">
                        {loading && <LoadingOverlay />}
                        <p className="section-label mb-2">Expansion Scalar \u03b8</p>
                        {data && (
                            <Plot
                                data={[{
                                    type: "surface",
                                    z: data.expansion_scalar,
                                    colorscale: blueScale,
                                    showscale: false,
                                    contours: { z: { show: true, usecolormap: true, project: { z: false } } },
                                }]}
                                layout={{
                                    ...darkLayout,
                                    height: 320,
                                    scene: {
                                        bgcolor: "rgba(0,0,0,0)",
                                        xaxis: { gridcolor: "rgba(255,255,255,0.02)", showbackground: false, tickfont: { size: 8, color: "rgba(255,255,255,0.15)" } },
                                        yaxis: { gridcolor: "rgba(255,255,255,0.02)", showbackground: false, tickfont: { size: 8, color: "rgba(255,255,255,0.15)" } },
                                        zaxis: { gridcolor: "rgba(255,255,255,0.02)", showbackground: false, tickfont: { size: 8, color: "rgba(255,255,255,0.15)" } },
                                        camera: { eye: { x: 1.5, y: 1.5, z: 1.0 } },
                                    },
                                }}
                                config={{ displayModeBar: false, responsive: true }}
                                style={{ width: "100%", height: "320px" }}
                            />
                        )}
                    </Panel>

                    <div className="grid grid-cols-2 gap-4">
                        <Panel className="relative">
                            <p className="section-label mb-2">Energy Density</p>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "heatmap",
                                        z: data.energy_density,
                                        colorscale: heatScale,
                                        showscale: false,
                                    }]}
                                    layout={{ ...darkLayout, height: 220, margin: { l: 32, r: 8, t: 8, b: 32 } }}
                                    config={{ displayModeBar: false, responsive: true }}
                                    style={{ width: "100%", height: "220px" }}
                                />
                            )}
                        </Panel>

                        <Panel className="relative">
                            <p className="section-label mb-2">Shape Function f(r)</p>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "scatter",
                                        x: data.shape_profile_r,
                                        y: data.shape_profile_f,
                                        mode: "lines",
                                        line: { color: "#3b82f6", width: 1.5 },
                                        fill: "tozeroy",
                                        fillcolor: "rgba(59,130,246,0.05)",
                                    }]}
                                    layout={{
                                        ...darkLayout,
                                        height: 220,
                                        margin: { l: 32, r: 8, t: 8, b: 32 },
                                        xaxis: { ...darkLayout.xaxis, title: { text: "r", font: { size: 9, color: "rgba(255,255,255,0.2)" } } },
                                        yaxis: { ...darkLayout.yaxis, title: { text: "f", font: { size: 9, color: "rgba(255,255,255,0.2)" } } },
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
