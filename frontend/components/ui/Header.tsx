"use client";

import Logo from "@/components/ui/Logo";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { FiSearch } from "react-icons/fi";
import { HiFilm, HiHome, HiUser, HiTv } from "react-icons/hi2";
import { GiSharpShuriken } from "react-icons/gi";
import clsx from "clsx";

const navItems = [
  { href: "/home", label: "Início", icon: HiHome },
  { href: "/filmes", label: "Filmes", icon: HiFilm },
  { href: "/series", label: "Séries", icon: HiTv },
  { href: "/animes", label: "Animes", icon: GiSharpShuriken },

  // { href: "/assistidos", label: "Assistidos", icon: HiClock },
  // { href: "/favoritos", label: "Favoritos", icon: HiHeart },
  { href: "/perfil", label: "Perfil", icon: HiUser },
];

export default function HeaderHome() {
  const pathname = usePathname();

  return (
    <header className="bg-[#121212] px-5 py-3 shadow-[0_8px_24px_rgba(0,0,0,0.35)]">
      <div className="mx-auto flex max-w-375 items-center gap-8">
        <Link href="/home"><Logo /></Link>
        <div className="ml-auto flex items-center gap-4">
          <div className="flex w-full max-w-140 items-center gap-3 rounded-full border border-white/10 bg-[#2b2b2b] px-4 py-2 shadow-inner shadow-black/20">
            <input
              type="text"
              placeholder="Pesquisar"
              className="w-full bg-transparent text-sm text-white placeholder:text-[#b0b0b0] outline-none"
            />
            <button
              type="button"
              aria-label="Pesquisar"
              className="flex h-8 w-8 items-center justify-center rounded-full bg-[#3a3a3a] text-lg text-white transition-colors hover:bg-[#4a4a4a] cursor-pointer"
            >
              <FiSearch />
            </button>
          </div>

          <button
            type="button"
            aria-label="Perfil do usuário"
            className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-full border border-white/10 bg-[radial-gradient(circle_at_30%_30%,#f7d3a4,#b47634_30%,#3b2d1e_80%)] text-sm font-bold text-[#111111] shadow-sm shadow-black/40"
          >
            U
          </button>
        </div>
      </div>

      <nav className="mx-auto mt-4 flex max-w-375 items-center justify-between gap-3 rounded-b-md border-t border-white/10 pt-3 text-sm font-medium text-[#d9d9d9]">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link
            key={label}
            href={href}
            className={clsx(
              "group flex flex-1",
              "items-center justify-center gap-2",
              "rounded-lg px-3 py-2",
              "transition-color",
              pathname === href ? 
                "text-primary bg-white/5 hover:text-primary underline" 
                :
                "hover:bg-white/5 hover:text-white",
            )}
          >
            <Icon className="h-4 w-4 text-current" />
            <span>{label}</span>
          </Link>
        ))}
      </nav>
    </header>
  );
}
