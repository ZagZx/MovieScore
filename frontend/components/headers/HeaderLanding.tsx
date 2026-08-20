import logo from "@/public/logo.png";
import Image from "next/image";
import Button from "@/components/Button";

export default function HeaderLanding() {
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
          <Image 
            src={logo}
            loading="eager"
            preload
            alt=""
            className="w-3xs"
          />
        </a>
      </div>
      <div className="space-x-4">
        <a href="/login">
          <Button>
            Entrar
          </Button>
        </a>
        <a href="/cadastro">
          <Button>
            Cadastrar-se
          </Button>
        </a>
      </div>
    </header>
  );
}