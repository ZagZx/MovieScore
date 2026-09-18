"use client";

import Logo from "@/components/ui/Logo";
import SearchBar from "@/components/ui/SearchBar";
import Link from "next/link";
import clsx from "clsx";
import { HiFilm, HiHome, HiUser, HiTv } from "react-icons/hi2";
import { GiSharpShuriken } from "react-icons/gi";
import { usePathname } from "next/navigation";

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
    <header className="bg-surface font-sansation px-5 py-3 shadow-lg ">
      <div className="mx-auto flex max-w-375 items-center gap-8">
        <Link href="/home"><Logo /></Link>
        <div className="ml-auto flex items-center gap-4">
          <SearchBar />

          {/* <button
            type="button"
            aria-label="Perfil do usuário"
            className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-full border border-white/10 bg-[radial-gradient(circle_at_30%_30%,#f7d3a4,#b47634_30%,#3b2d1e_80%)] text-sm font-bold text-[#111111] shadow-sm shadow-black/40"
          >
            U
          </button> */}
        </div>
      </div>

      <nav className="mx-auto mt-4 flex max-w-375 items-center justify-between gap-3 rounded-b-md border-t border-surface-border pt-3">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link
            key={label}
            href={href}
            className={clsx(
              "group flex flex-1",
              "items-center justify-center gap-2",
              "rounded-lg px-3 py-2",
              "transition-color",
              "hover:bg-surface-hover hover:text-foreground",
              pathname === href && "text-primary bg-surface-hover hover:text-primary underline" 
            )}
          >
            <Icon className="size-4" />
            <span>{label}</span>
          </Link>
        ))}
      </nav>
    </header>
  );
}
