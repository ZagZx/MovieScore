"use client";

import { postCreateUsuario } from "@/actions/usuario";
import Button from "@/components/ui/Button";
import InputAuth from "@/components/features/auth/InputAuth";
import { CadastroFormData, cadastroSchema } from "@/lib/schemas/usuario";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import Swal from "sweetalert2";


export default function FormCadastro() {
  const {register, handleSubmit, formState: { isSubmitting, errors }} = useForm<CadastroFormData>({
    defaultValues: {
      nome: "",
      email: "",
      senha: "",
      confirmarSenha: ""
    },
    resolver: zodResolver(cadastroSchema)
  });

  async function onSubmit(data: CadastroFormData) {
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
        {errors.nome && (<span>{errors.nome.message}</span>)}
        <InputAuth required type="email" id="email" label="Email" {...register("email")}/>
        {errors.email && (<span>{errors.email.message}</span>)}
        <InputAuth required type="password" id="senha" label="Senha" {...register("senha")}/>
        {errors.senha && (<span>{errors.senha.message}</span>)}
        <InputAuth required type="password" id="confirmarSenha" label="Confirme sua senha" {...register("confirmarSenha")}/>
        {errors.confirmarSenha && (<span>{errors.confirmarSenha.message}</span>)}
        <Button type="submit" className="mt-4" disabled={isSubmitting}>{isSubmitting ? "Cadastrando..." : "Cadastrar-se"}</Button>
      </div>
    </form>
  );
}