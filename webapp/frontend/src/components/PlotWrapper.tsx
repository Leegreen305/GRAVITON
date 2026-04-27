"use client";

import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

export const darkLayout = {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: "rgba(255,255,255,0.6)", family: "JetBrains Mono, monospace", size: 11 },
    margin: { l: 50, r: 20, t: 30, b: 50 },
    xaxis: {
        gridcolor: "rgba(255,255,255,0.04)",
        zerolinecolor: "rgba(255,255,255,0.08)",
        tickfont: { size: 10 },
    },
    yaxis: {
        gridcolor: "rgba(255,255,255,0.04)",
        zerolinecolor: "rgba(255,255,255,0.08)",
        tickfont: { size: 10 },
    },
    legend: {
        bgcolor: "rgba(0,0,0,0)",
        font: { color: "rgba(255,255,255,0.5)", size: 10 },
    },
    modebar: { bgcolor: "rgba(0,0,0,0)" },
};

export const cyanColorscale: [number, string][] = [
    [0, "#0a0a14"],
    [0.2, "#0d1b3e"],
    [0.4, "#0e3d6b"],
    [0.6, "#0891b2"],
    [0.8, "#22d3ee"],
    [1, "#ffffff"],
];

export const energyColorscale: [number, string][] = [
    [0, "#0a0a14"],
    [0.15, "#1e0038"],
    [0.3, "#5b0099"],
    [0.5, "#e00060"],
    [0.7, "#ff6600"],
    [0.85, "#ffcc00"],
    [1, "#ffffff"],
];

export default Plot;
