"use client";

import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

export const darkLayout = {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: "rgba(255,255,255,0.35)", family: "'JetBrains Mono', monospace", size: 10 },
    margin: { l: 44, r: 16, t: 20, b: 40 },
    xaxis: {
        gridcolor: "rgba(255,255,255,0.025)",
        zerolinecolor: "rgba(255,255,255,0.04)",
        tickfont: { size: 9, color: "rgba(255,255,255,0.25)" },
        linecolor: "rgba(255,255,255,0.04)",
    },
    yaxis: {
        gridcolor: "rgba(255,255,255,0.025)",
        zerolinecolor: "rgba(255,255,255,0.04)",
        tickfont: { size: 9, color: "rgba(255,255,255,0.25)" },
        linecolor: "rgba(255,255,255,0.04)",
    },
    legend: {
        bgcolor: "rgba(0,0,0,0)",
        font: { color: "rgba(255,255,255,0.35)", size: 9 },
    },
    modebar: { bgcolor: "rgba(0,0,0,0)" },
};

export const blueScale: [number, string][] = [
    [0, "#0a0b10"],
    [0.15, "#0f1428"],
    [0.35, "#132450"],
    [0.55, "#1d4ed8"],
    [0.75, "#60a5fa"],
    [1, "#e0eeff"],
];

export const heatScale: [number, string][] = [
    [0, "#0a0b10"],
    [0.12, "#1a0828"],
    [0.28, "#3b0764"],
    [0.45, "#9333ea"],
    [0.62, "#e879f9"],
    [0.8, "#fde68a"],
    [1, "#ffffff"],
];

export default Plot;
