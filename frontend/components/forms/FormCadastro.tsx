"use client";

import { postCreateUsuario } from "@/actions/usuario";
import Button from "@/components/Button";
import InputAuth from "@/components/inputs/InputAuth";
import { CadastroFormData, cadastroSchema } from "@/schemas/usuario";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import Swal from "sweetalert2";


export default function FormCadastro() {
  const {register, handleSubmit, formState: { isSubmitting }} = useForm<CadastroFormData>({
    defaultValues: {
      nome: "",
      email: "",
      senha: "",
      confirmarSenha: ""
    },
    resolver: zodResolver(cadastroSchema)
  });

  async function onSubmit(data: CadastroFormData) {
    if (data.senha !== data.confirmarSenha) {
      Swal.fire({
        icon: "error",
        title: "Senhas não coincidem",
        text: "Confirme sua senha novamente"
      });

      return;
    }

    try {
      const response = await postCreateUsuario({
        nome: data.nome,
        email: data.email,
        senha: data.senha
      });

      if (response?.status === 201) {
        Swal.fire({
          icon: "success",
          title: "Usuário cadastrado",
        })
      }
    } catch(error) {
      Swal.fire({
        icon: "question",
        title: "Erro",
        text: "Erro interno"
      });
    }
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