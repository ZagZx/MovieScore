import Button from "@/components/ui/Button";
import Logo from "@/components/ui/Logo";

export default function HeaderLanding() {
  return (
    <header
      className="
        flex justify-between 
        absolute 
        w-screen
        px-12
        py-6
      "
    >
      <div>
        <a href=""> {/* LINK PARA /home */}
          <Logo />
        </a>
      </div>
      <div className="flex items-center gap-4">
        <a href="/login">
          <Button>
            Entrar
          </Button>
        </a>
        <a href="/cadastro">
          <Button>
            Cadastrar-se
          </Button>
        </a>
      </div>
    </header>
  );
}