"use client";

import { postCreateUsuario } from "@/actions/usuario";
import Button from "@/components/ui/Button";
import InputAuth from "@/components/features/auth/InputAuth";
import { CadastroFormData, cadastroSchema } from "@/lib/schemas/usuario";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import Swal from "sweetalert2";
import FieldError from "@/components/features/auth/FieldError";
import { alert } from "@/lib/alert";
import { redirect } from "next/navigation";


export default function FormCadastro() {
  const {register, handleSubmit, formState: { isSubmitting, errors }} = useForm<CadastroFormData>({
    mode: "onBlur",
    reValidateMode: "onBlur",
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
        alert.fire({
          icon: "success",
          title: "Usuário cadastrado",
          text: "Prossiga para fazer login"
        }).then(() => redirect("/login"));
      } else if (response?.status === 409) {
        alert.fire({
          icon: "error",
          title: "Email já cadastrado",
          text: "Insira outro email ou faça login",
          showCancelButton: true,
          cancelButtonText: "Voltar",
          confirmButtonText: "Iniciar sessão"
        }).then((result) => result.isConfirmed && redirect("/login"));
      }
    } catch(error) {
      alert.fire({
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
          flex flex-col gap-2 w-90
        "
      >
        <h1 className="text-4xl font-medium mb-8 text-center">
          Cadastro
        </h1>

        <div>
          <InputAuth id="nome" labelValue="Nome de usuário" {...register("nome")}/>
          {errors.nome && (<FieldError aria-invalid aria-describedby="nome">{errors.nome.message}</FieldError>)}
        </div>
        <div>
          <InputAuth type="email" id="email" labelValue="Email" {...register("email")}/>
          {errors.email && (<FieldError>{errors.email.message}</FieldError>)}
        </div>
        <div>
          <InputAuth type="password" id="senha" labelValue="Senha" {...register("senha")}/>
          {errors.senha && (<FieldError>{errors.senha.message}</FieldError>)}
        </div>
        <div>
          <InputAuth type="password" id="confirmarSenha" labelValue="Confirme sua senha" {...register("confirmarSenha")}/>
          {errors.confirmarSenha && (<FieldError>{errors.confirmarSenha.message}</FieldError>)}
        </div>

        <Button type="submit" className="mt-4" disabled={isSubmitting}>{isSubmitting ? "Cadastrando..." : "Cadastrar-se"}</Button>
      </div>
    </form>
  );
}