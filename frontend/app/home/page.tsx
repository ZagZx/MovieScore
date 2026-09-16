import Header from "@/components/ui/Header";
import FilmesEmAlta from "@/components/features/home/FilmesEmAlta";
import FilmesEmAltaBackup from "@/components/features/home/FilmesEmAltaBackup";
import { filmesListagemMock } from "@/lib/mocks/filme";

export default async function HomePage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />

      <main className="px-5 py-8 md:px-8">
        <FilmesEmAlta filmes={filmesListagemMock} />
        <FilmesEmAltaBackup filmes={filmesListagemMock} />
      </main>
    </div>
  );
}
