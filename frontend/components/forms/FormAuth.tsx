import { postCreateUsuario } from "@/actions/usuario";
import Button from "@/components/Button";
import InputAuth from "@/components/inputs/InputAuth";

export default async function FormAuth() {
  return (
    <form action="">
      <div 
        className="
          flex flex-col gap-2
        "
      >
        <h1 className="text-4xl font-medium mb-8 text-center">
          Cadastro
        </h1>
        <InputAuth required id="username" name="username" label="Nome de usuário"/>
        <InputAuth required type="email" id="email" name="email" label="Email"/>
        <InputAuth required type="password" id="password" name="password" label="Senha"/>
        <InputAuth required type="password" id="passwordConfirm" name="passwordConfirm" label="Confirme sua senha"/>
        <Button className="mt-4">Cadastrar-se</Button>
      </div>
    </form>
  );
}