"use client";

import Button from "@/components/ui/Button";
import InputAuth from "@/components/features/auth/InputAuth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useState } from "react";
import FieldError from "@/components/features/auth/FieldError";
import { LoginFormData, loginSchema } from "@/lib/schemas/auth";
import { login } from "@/actions/auth";
import { alert } from "@/lib/alert";


export default function FormLogin() {
  const {register, handleSubmit, trigger, formState: { isSubmitting, errors }} = useForm<LoginFormData>({
    mode: "onBlur",
    reValidateMode: "onBlur",
    defaultValues: {
      email: "",
      senha: ""
    },
    resolver: zodResolver(loginSchema)
  });

  const [step, setStep] = useState(0);
  const fields: Array<keyof LoginFormData> = ["email", "senha"];

  async function handleNext() {
    const current = fields[step];

    // If last field, validate both and submit
    if (current === "senha") {
      const valid = await trigger(["email", "senha"]);
      if (!valid) return;
      return handleSubmit(async (data) => await onSubmit(data as LoginFormData))();
    }

    const valid = await trigger([current]);
    if (!valid) return;

    if (step < fields.length - 1) setStep((s) => s + 1);
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter") {
      e.preventDefault();
      void handleNext();
    }
  }

  async function onSubmit(data: LoginFormData) {
    try {
      const response = await login({
        email: data.email,
        senha: data.senha
      });
      
      if (response?.status === 200) {
        alert.fire({
          icon: "success",
          title: "Login realizado",
          text: "Bem vindo!"
        });
      } else if (response?.status === 401) {
        alert.fire({
          icon: "question",
          title: "Credenciais inválidas",
          text: "E-mail e/ou senha incorretos"
        });
      } else if (!response.success) {
        console.log(response.status, response.error);
        alert.fire({
          icon: "error",
          title: "Erro",
          text: "Erro interno"
        });
      }
    } catch(error) {
      console.log(error);
      alert.fire({
        icon: "error",
        title: "Erro",
        text: "Erro interno"
      });
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className="flex flex-col gap-2 w-90">
        <h1 className="text-4xl font-medium mb-8 text-center">Login</h1>

        {step >= 0 && (
          <div>
            <InputAuth type="email" id="email" labelValue="Email" {...register("email")} onKeyDown={handleKeyDown} />
            {errors.email && (<FieldError>{errors.email.message}</FieldError>)}
          </div>
        )}

        {step >= 1 && (
          <div>
            <InputAuth type="password" id="senha" labelValue="Senha" {...register("senha")} onKeyDown={handleKeyDown} />
            {errors.senha && (<FieldError>{errors.senha.message}</FieldError>)}
          </div>
        )}

        
        {step < fields.length - 1 ? (
          <Button type="button" variant="outline" onClick={() => void handleNext()} disabled={isSubmitting}>
            Próximo
          </Button>
        ) : (
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Aguarde..." : "Iniciar sessão"}
          </Button>
        )}
      </div>
    </form>
  );
}