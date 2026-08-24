import z from "zod";


export const cadastroSchema = z.object({
    nome: z.string()
        .nonempty("Insira um nome")
        .min(3, "O nome de usuário deve conter pelo menos 3 caracteres"),
    email: z.email("Email inválido")
        .nonempty("Insira um email"),
    senha: z.string()
        .nonempty("Insira uma senha")
        .min(8, "A senha deve conter pelo menos 8 caracteres"),
    confirmarSenha: z.string()
        .nonempty("Confirme sua senha")
        .min(8, "A senha deve conter pelo menos 8 caracteres")
}).refine((data) => data.senha === data.confirmarSenha, {
    message: "As senhas não coincidem",
    path: ["confirmarSenha"]
})

export type CadastroFormData = z.infer<typeof cadastroSchema>;