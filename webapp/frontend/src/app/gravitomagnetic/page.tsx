"use client";

import { useState, useEffect, useRef } from "react";
import Plot from "@/components/PlotWrapper";
import { darkLayout, blueScale, heatScale } from "@/components/PlotWrapper";
import { PageHeader, ParamSlider, MetricCard, Panel, LoadingOverlay, Divider } from "@/components/ui";
import { fetchAPI, formatScientific } from "@/lib/api";

const presets = [
    { name: "Earth", mass: 5.97e24, radius: 6.371e6, angular_momentum_z: 7.07e33 },
    { name: "Neutron Star", mass: 2.78e30, radius: 1.2e4, angular_momentum_z: 1.5e40 },
    { name: "Black Hole 10M\u2609", mass: 1.989e31, radius: 2.95e4, angular_momentum_z: 6.0e42 },
];

export default function GravitomageticPage() {
    const [mass, setMass] = useState(5.97e24);
    const [radius, setRadius] = useState(6.371e6);
    const [angMomZ, setAngMomZ] = useState(7.07e33);
    const [activePreset, setActivePreset] = useState(0);
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

    function applyPreset(i: number) {
        setActivePreset(i);
        setMass(presets[i].mass);
        setRadius(presets[i].radius);
        setAngMomZ(presets[i].angular_momentum_z);
    }

    useEffect(() => {
        if (timer.current) clearTimeout(timer.current);
        timer.current = setTimeout(async () => {
            setLoading(true);
            try {
                const res = await fetchAPI("/api/gravitomagnetic", { mass, radius, angular_momentum_z: angMomZ });
                setData(res);
            } catch { }
            setLoading(false);
        }, 500);
        return () => { if (timer.current) clearTimeout(timer.current); };
    }, [mass, radius, angMomZ]);

    return (
        <div className="max-w-[1100px] animate-in">
            <PageHeader
                title="Gravitoelectromagnetism"
                subtitle="Linearized GR field equations"
                equation="F = m(E\u2091 + v \u00d7 B\u2091)"
            />

            <div className="grid grid-cols-[240px_1fr] gap-5">
                <div className="space-y-4">
                    <Panel>
                        <p className="section-label mb-3">Presets</p>
                        <div className="flex flex-wrap gap-1.5">
                            {presets.map((p, i) => (
                                <button
                                    key={p.name}
                                    onClick={() => applyPreset(i)}
                                    className={`preset-pill ${activePreset === i ? "preset-pill-active" : ""}`}
                                >
                                    {p.name}
                                </button>
                            ))}
                        </div>
                    </Panel>

                    <Panel>
                        <p className="section-label mb-3">Parameters</p>
                        <div className="space-y-4">
                            <ParamSlider label="Mass" value={Math.log10(mass)} min={20} max={35} step={0.1} onChange={(v) => { setMass(10 ** v); setActivePreset(-1); }} formatValue={(v) => `10^${v.toFixed(1)}`} unit="kg" />
                            <ParamSlider label="Radius" value={Math.log10(radius)} min={3} max={8} step={0.1} onChange={(v) => { setRadius(10 ** v); setActivePreset(-1); }} formatValue={(v) => `10^${v.toFixed(1)}`} unit="m" />
                            <ParamSlider label="J" value={Math.log10(angMomZ)} min={30} max={45} step={0.1} onChange={(v) => { setAngMomZ(10 ** v); setActivePreset(-1); }} formatValue={(v) => `10^${v.toFixed(1)}`} unit="kg\u00b7m\u00b2/s" />
                        </div>
                    </Panel>

                    {data && (
                        <Panel>
                            <p className="section-label mb-2">Results</p>
                            <MetricCard label="E\u2091 magnitude" value={formatScientific(data.Eg_magnitude)} unit="m/s\u00b2" />
                            <Divider />
                            <MetricCard label="B\u2091 magnitude" value={formatScientific(data.Bg_magnitude)} unit="1/s" />
                            <Divider />
                            <MetricCard label="LT Precession" value={formatScientific(data.lt_precession_rate)} unit="rad/s" />
                            <Divider />
                            <MetricCard label="Time Dilation" value={data.time_dilation?.toFixed(12) ?? "\u2014"} />
                        </Panel>
                    )}
                </div>

                <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <Panel className="relative">
                            {loading && <LoadingOverlay />}
                            <p className="section-label mb-2">|E\u2091| Field</p>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "heatmap",
                                        z: data.Eg_field,
                                        colorscale: blueScale,
                                        showscale: false,
                                    }]}
                                    layout={{ ...darkLayout, height: 300, margin: { l: 32, r: 8, t: 8, b: 32 } }}
                                    config={{ displayModeBar: false, responsive: true }}
                                    style={{ width: "100%", height: "300px" }}
                                />
                            )}
                        </Panel>

                        <Panel className="relative">
                            {loading && <LoadingOverlay />}
                            <p className="section-label mb-2">|B\u2091| Field</p>
                            {data && (
                                <Plot
                                    data={[{
                                        type: "heatmap",
                                        z: data.Bg_field,
                                        colorscale: heatScale,
                                        showscale: false,
                                    }]}
                                    layout={{ ...darkLayout, height: 300, margin: { l: 32, r: 8, t: 8, b: 32 } }}
                                    config={{ displayModeBar: false, responsive: true }}
                                    style={{ width: "100%", height: "300px" }}
                                />
                            )}
                        </Panel>
                    </div>
                </div>
            </div>
        </div>
    );
}
