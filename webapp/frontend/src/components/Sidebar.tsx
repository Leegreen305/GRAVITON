"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Atom, Orbit, Zap, Navigation, LayoutDashboard } from "lucide-react";
import { motion } from "framer-motion";

const navItems = [
    { href: "/", label: "Overview", icon: LayoutDashboard },
    { href: "/alcubierre", label: "Alcubierre", icon: Navigation },
    { href: "/gravitomagnetic", label: "Gravitomagnetic", icon: Atom },
    { href: "/zpe", label: "Zero-Point Energy", icon: Zap },
    { href: "/geodesic", label: "Geodesics", icon: Orbit },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="fixed left-0 top-0 bottom-0 w-[220px] bg-[#08080f] border-r border-white/[0.04] flex flex-col z-50">
            {/* Logo */}
            <div className="px-5 pt-6 pb-4">
                <Link href="/" className="flex items-center gap-2.5 group">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-[0_0_15px_rgba(6,182,212,0.3)]">
                        <span className="text-white font-bold text-xs">G</span>
                    </div>
                    <div>
                        <span className="text-sm font-bold text-white tracking-wide">GRAVITON</span>
                        <span className="block text-[9px] text-white/30 uppercase tracking-[0.2em] -mt-0.5">Simulator</span>
                    </div>
                </Link>
            </div>

            {/* Divider */}
            <div className="mx-4 glow-line mb-4" />

            {/* Nav */}
            <nav className="flex-1 px-3 space-y-1">
                {navItems.map((item) => {
                    const active = pathname === item.href;
                    const Icon = item.icon;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`relative flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all duration-200 group ${active
                                    ? "text-cyan-400 bg-white/[0.04]"
                                    : "text-white/40 hover:text-white/70 hover:bg-white/[0.02]"
                                }`}
                        >
                            {active && (
                                <motion.div
                                    layoutId="nav-indicator"
                                    className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-5 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(6,182,212,0.5)]"
                                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                                />
                            )}
                            <Icon className="w-4 h-4 flex-shrink-0" />
                            <span className="font-medium">{item.label}</span>
                        </Link>
                    );
                })}
            </nav>

            {/* Footer */}
            <div className="px-5 pb-5">
                <div className="text-[10px] text-white/20 space-y-1">
                    <p>Peer-reviewed physics</p>
                    <p className="font-mono">v1.0.0</p>
                </div>
            </div>
        </aside>
    );
}
