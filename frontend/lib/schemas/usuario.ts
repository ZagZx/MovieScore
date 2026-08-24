import z from "zod";


export const cadastroSchema = z.object({
    nome: z.string().trim()
        .nonempty("Insira um nome")
        .min(3, "O nome de usuário deve conter pelo menos 3 caracteres")
        .max(50, "O nome de usuário deve conter no máximo 50 caracteres"),
    email: z.string()
        .trim()
        .nonempty("Insira um email")
        .pipe(z.email("Email inválido")),
    senha: z.string()
        .nonempty("Insira uma senha")
        .min(8, "A senha deve conter pelo menos 8 caracteres"),
    confirmarSenha: z.string()
        .nonempty("Confirme a senha")
        .min(8, "A senha deve conter pelo menos 8 caracteres")
}).refine((data) => data.senha === data.confirmarSenha, {
    message: "As senhas não coincidem",
    path: ["confirmarSenha"]
})

export type CadastroFormData = z.infer<typeof cadastroSchema>;