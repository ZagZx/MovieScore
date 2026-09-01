import z from "zod";

export const loginSchema = z.object({
    email: z.string()
        .trim()
        .nonempty("Insira um email")
        .pipe(z.email("Email inválido")),
    senha: z.string()
        .nonempty("Insira uma senha")
        .min(8, "A senha deve conter pelo menos 8 caracteres"),
});

export type LoginFormData = z.infer<typeof loginSchema>;