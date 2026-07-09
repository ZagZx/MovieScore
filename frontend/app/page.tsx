import filmesLandingImage  from "@/public/filmes-landing.jpeg"
import HeaderLanding from "@/components/HeaderLanding";

export default async function Home() {
  const opacity = 20; // opacidade do fundo em porcentagem

  return (
    <div className="relative flex min-h-screen flex-col overflow-hidden">
      <div
        aria-hidden="true"
        className={`absolute inset-0 bg-center bg-cover bg-no-repeat opacity-${opacity}`}
        style={{ backgroundImage: `url(${filmesLandingImage.src})` }}
      />
      <div className="relative z-10 flex min-h-screen flex-col">
        <HeaderLanding />
        <main
          className={`
            flex flex-1 flex-col items-center justify-between 
            w-full 
            py-32 px-1
          `}
        >
          TESTEE
        </main>
      </div>
    </div>
  );
}
