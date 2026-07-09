import logo from "@/public/logo.png";
import Image from "next/image";

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
          alt=""
          className="w-3xs"
        />
      </div>
      <div>
        Entrar
      </div>
    </header>
  );
}