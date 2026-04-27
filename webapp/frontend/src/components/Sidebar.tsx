"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Atom, Orbit, Zap, Navigation, LayoutDashboard } from "lucide-react";

const navItems = [
    { href: "/", label: "Overview", icon: LayoutDashboard },
    { href: "/alcubierre", label: "Alcubierre", icon: Navigation },
    { href: "/gravitomagnetic", label: "GEM", icon: Atom },
    { href: "/zpe", label: "Zero-Point", icon: Zap },
    { href: "/geodesic", label: "Geodesics", icon: Orbit },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="fixed left-0 top-0 bottom-0 w-[200px] bg-[#08090d] border-r border-white/[0.04] flex flex-col z-50">
            {/* Logo */}
            <div className="px-5 pt-5 pb-4">
                <Link href="/" className="block">
                    <span className="text-[13px] font-semibold text-white/90 tracking-[0.04em]">GRAVITON</span>
                    <span className="block text-[10px] text-white/20 mt-0.5 tracking-wide">v1.0</span>
                </Link>
            </div>

            <div className="divider mx-4" />

            {/* Nav */}
            <nav className="flex-1 px-3 py-3 space-y-0.5">
                {navItems.map((item) => {
                    const active = pathname === item.href;
                    const Icon = item.icon;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`flex items-center gap-2.5 px-2.5 py-[7px] rounded-lg text-[12.5px] transition-colors duration-150 ${active
                                    ? "text-white/90 bg-white/[0.05]"
                                    : "text-white/30 hover:text-white/55 hover:bg-white/[0.02]"
                                }`}
                        >
                            <Icon className="w-[14px] h-[14px] flex-shrink-0" strokeWidth={active ? 2 : 1.5} />
                            <span className="font-medium">{item.label}</span>
                        </Link>
                    );
                })}
            </nav>

            {/* Footer */}
            <div className="px-5 pb-4">
                <div className="flex items-center gap-1.5 mb-2">
                    <div className="status-dot status-dot-live" />
                    <span className="text-[10px] text-white/25">API Connected</span>
                </div>
                <p className="text-[9px] text-white/12 leading-relaxed">
                    Peer-reviewed physics
                </p>
            </div>
        </aside>
    );
}
