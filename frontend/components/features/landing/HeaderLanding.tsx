"use client";

import Button from "@/components/ui/Button";
import Logo from "@/components/ui/Logo";
import { usePathname } from "next/navigation";

export default function HeaderLanding() {
  const pathname = usePathname();

  return (
    <header
      className="
        flex justify-between 
        absolute 
        w-screen
        px-12
        py-6
      "
    >
      <div>
        <a href=""> {/* LINK PARA /home */}
          <Logo />
        </a>
      </div>
      <div className="flex items-center gap-4">
        {['/', '/cadastro'].includes(pathname) && 
          (<a href="/login">
            <Button>
              Entrar
            </Button>
          </a>)
        }
        {['/', '/login'].includes(pathname) && 
          (<a href="/cadastro">
            <Button>
              Cadastrar-se
            </Button>
          </a>)
        }
        
      </div>
    </header>
  );
}