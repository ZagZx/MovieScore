import Button from "@/components/Button";
import FormCadastro from "@/components/forms/FormCadastro";
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
        <FormCadastro />
      </main>
    </>
  );
}