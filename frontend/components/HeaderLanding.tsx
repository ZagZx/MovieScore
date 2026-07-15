import logo from "@/public/logo.png";
import Image from "next/image";
import Button from "./Button";

export default function HeaderLanding() {
  return (
    <header
      className="
        flex justify-between 
        absolute 
        w-screen
        px-8
        py-6
      "
    >
      <div>
        <Image 
          src={logo}
          loading="eager"
          preload
          alt=""
          className="w-3xs"
        />
      </div>
      <div className="space-x-2">
        <Button>
          Entrar
        </Button>
        <Button>
          Cadastrar-se
        </Button>
      </div>
    </header>
  );
}