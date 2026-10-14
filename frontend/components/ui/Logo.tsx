import logo from "@/public/logo.png";
import Image from "next/image";

export default function Logo() {
  return (
    <Image
      src={logo}
      loading="eager"
      preload
      alt=""
      className="w-3xs"
    />
  );
}