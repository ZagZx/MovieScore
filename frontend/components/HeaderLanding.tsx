import logo from "@/public/logo.png";
import Image from "next/image";
import Button from "./Button";

export default function HeaderLanding() {
  return (
    <header
      className="
        flex justify-between 
        mx-8
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
      <div>
        <Button>
          Entrar
        </Button>
      </div>
    </header>
  );
}