import Button from "@/components/Button";
import FormAuth from "@/components/forms/FormAuth";
import HeaderLanding from "@/components/headers/HeaderLanding";
import InputAuth from "@/components/inputs/InputAuth";


export default function Cadastro() {
  return (
    <>
      <HeaderLanding/>
      <main
        className="
          flex flex-1 
          items-center 
          justify-center
        "
      >
        <FormAuth />
      </main>
    </>
  );
}