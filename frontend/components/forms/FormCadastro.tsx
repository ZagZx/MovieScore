"use client";

import { postCreateUsuario } from "@/actions/usuario";
import Button from "@/components/Button";
import InputAuth from "@/components/inputs/InputAuth";
import { useForm } from "react-hook-form";
import Swal from "sweetalert2";


interface CadastroFormData {
  nome: string;
  email: string;
  senha: string;
  confirmarSenha: string;
}

export default function FormCadastro() {
  const {register, handleSubmit, formState: { isSubmitting }} = useForm<CadastroFormData>({
    defaultValues: {
      nome: "",
      email: "",
      senha: "",
      confirmarSenha: ""
    }
  });

  async function onSubmit(data: CadastroFormData) {
    const nome = data.nome;
    const email = data.email;
    const senha = data.senha;
    const confirmarSenha = data.confirmarSenha;

    if (senha !== confirmarSenha) {
      Swal.fire({
        icon: "error",
        title: "Senhas não coincidem",
        text: "Confirme sua senha novamente"
      });

      return;
    }

    try {
      const response = await postCreateUsuario({
        nome: nome,
        email: email,
        senha: senha
      });

      if (response?.status === 201) {
        Swal.fire({
          icon: "success",
          title: "Usuário cadastrado",
        })
      }
    } catch(error) {
      Swal.fire({
        icon: "error",
        title: "Erro",
        text: "deu erro ai"
      });
    }
    return;
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div 
        className="
          flex flex-col gap-2
        "
      >
        <h1 className="text-4xl font-medium mb-8 text-center">
          Cadastro
        </h1>
        <InputAuth required id="nome" label="Nome de usuário" {...register("nome")}/>
        <InputAuth required type="email" id="email" label="Email" {...register("email")}/>
        <InputAuth required type="password" id="senha" label="Senha" {...register("senha")}/>
        <InputAuth required type="password" id="confirmarSenha" label="Confirme sua senha" {...register("confirmarSenha")}/>
        <Button type="submit" className="mt-4" disabled={isSubmitting}>{isSubmitting ? "Cadastrando..." : "Cadastrar-se"}</Button>
      </div>
    </form>
  );
}