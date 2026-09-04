"use client";

import { postCreateUsuario } from "@/actions/usuario";
import Button from "@/components/ui/Button";
import InputAuth from "@/components/features/auth/InputAuth";
import { CadastroFormData, cadastroSchema } from "@/lib/schemas/usuario";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useState } from "react";
import FieldError from "@/components/features/auth/FieldError";
import { alert } from "@/lib/alert";
import { redirect } from "next/navigation";


export default function FormCadastro() {
  const {register, handleSubmit, trigger, getValues, formState: { isSubmitting, errors }} = useForm<CadastroFormData>({
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
      } else if (!response.success) {
        console.log(response.status, response.error);
        alert.fire({
          icon: "error",
          title: "Erro",
          text: "Erro interno"
        });
      }
    } catch(error) {
      console.log(error)
      alert.fire({
        icon: "question",
        title: "Erro",
        text: "Erro interno"
      });
    }
  }
  const [step, setStep] = useState(0);
  const fields: Array<keyof CadastroFormData> = ["nome", "email", "senha", "confirmarSenha"];

  async function handleNext() {
    const currentField = fields[step];

    if (currentField === "confirmarSenha") {
      const valid = await trigger(["senha", "confirmarSenha"]);
      if (!valid) return;
      return handleSubmit(onSubmit)();
    }

    const valid = await trigger([currentField]);
    if (!valid) return;

    if (step < fields.length - 1) {
      setStep((s) => s + 1);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter") {
      e.preventDefault();
      void handleNext();
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className="flex flex-col gap-2 w-90">
        <h1 className="text-4xl font-medium mb-8 text-center">Cadastro</h1>

        {step >= 0 && (
          <div>
            <InputAuth id="nome" labelValue="Nome de usuário" {...register("nome")} onKeyDown={handleKeyDown} />
            {errors.nome && (<FieldError aria-invalid aria-describedby="nome">{errors.nome.message}</FieldError>)}
          </div>
        )}

        {step >= 1 && (
          <div>
            <InputAuth type="email" id="email" labelValue="Email" {...register("email")} onKeyDown={handleKeyDown} />
            {errors.email && (<FieldError>{errors.email.message}</FieldError>)}
          </div>
        )}

        {step >= 2 && (
          <div>
            <InputAuth type="password" id="senha" labelValue="Senha" {...register("senha")} onKeyDown={handleKeyDown} />
            {errors.senha && (<FieldError>{errors.senha.message}</FieldError>)}
          </div>
        )}

        {step >= 3 && (
          <div>
            <InputAuth type="password" id="confirmarSenha" labelValue="Confirme sua senha" {...register("confirmarSenha")} onKeyDown={handleKeyDown} />
            {errors.confirmarSenha && (<FieldError>{errors.confirmarSenha.message}</FieldError>)}
          </div>
        )}

        
        {step < fields.length - 1 ? (
          <Button type="button" variant="outline" onClick={() => void handleNext()} disabled={isSubmitting}>
            Próximo
          </Button>
        ) : (
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Cadastrando..." : "Cadastrar-se"}
          </Button>
        )}
      </div>
    </form>
  );
}