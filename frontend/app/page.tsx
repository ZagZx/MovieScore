import filmesLandingImage  from "@/public/filmes-landing.jpeg"
import HeaderLanding from "@/components/HeaderLanding";
import Button from "@/components/Button";

export default async function Home() {
  return (
    <div className="relative flex min-h-screen flex-col overflow-hidden bg-background">
      <div
        aria-hidden="true"
        className={`absolute inset-0 bg-center bg-cover bg-no-repeat opacity-25`}
        style={{ backgroundImage: `url(${filmesLandingImage.src})` }}
      />
      <div className="relative z-10 flex min-h-screen flex-col">
        <HeaderLanding />
        <main
          className={`
            flex flex-1 
            items-center 
            justify-center
          `}
        >
          <div className="space-y-2 text-center">
            <h1 
              className="
                font-bold
                text-4xl
              "
            >
              Filmes, séries e animes, sem limites
            </h1>
            <div className="space-x-4">
              <span className="text-xl">Quer avaliar? Crie sua conta</span>
              <Button>Vamos lá</Button>
            </div>
          </div>

        </main>
      </div>
    </div>
  );
}
