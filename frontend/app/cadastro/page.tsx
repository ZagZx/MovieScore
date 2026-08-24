import FormCadastro from "@/components/features/auth/cadastro/FormCadastro";
import HeaderLanding from "@/components/features/landing/HeaderLanding";


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