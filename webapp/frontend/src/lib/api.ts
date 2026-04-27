const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

export async function fetchAPI<T>(endpoint: string, body: Record<string, unknown>): Promise<T> {
    const res = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(err.detail || `API error ${res.status}`);
    }
    return res.json();
}

export function formatScientific(value: number, digits: number = 2): string {
    if (value === 0) return "0";
    if (!isFinite(value)) return value > 0 ? "+Inf" : "-Inf";
    const exp = Math.floor(Math.log10(Math.abs(value)));
    const mantissa = value / Math.pow(10, exp);
    if (Math.abs(exp) <= 3) return value.toFixed(digits);
    return `${mantissa.toFixed(digits)} × 10^${exp}`;
}

export function formatSI(value: number, unit: string): string {
    const abs = Math.abs(value);
    const prefixes = [
        { threshold: 1e24, symbol: "Y" },
        { threshold: 1e21, symbol: "Z" },
        { threshold: 1e18, symbol: "E" },
        { threshold: 1e15, symbol: "P" },
        { threshold: 1e12, symbol: "T" },
        { threshold: 1e9, symbol: "G" },
        { threshold: 1e6, symbol: "M" },
        { threshold: 1e3, symbol: "k" },
        { threshold: 1, symbol: "" },
        { threshold: 1e-3, symbol: "m" },
        { threshold: 1e-6, symbol: "μ" },
        { threshold: 1e-9, symbol: "n" },
        { threshold: 1e-12, symbol: "p" },
    ];
    for (const p of prefixes) {
        if (abs >= p.threshold) {
            return `${(value / p.threshold).toFixed(2)} ${p.symbol}${unit}`;
        }
    }
    return formatScientific(value) + " " + unit;
}
