import { getFavoritosUsuario } from "@/actions/usuario";
import Header from "@/components/ui/Header";
import FiltroConteudo from "@/components/ui/filtros/FiltroConteudo";
import FiltroOrdemRecentes from "@/components/ui/filtros/FiltroOrdemRecentes";

export default async function FavoritosPage() {
  const result = await getFavoritosUsuario();
  console.log(result)
  return (
    <>
      <Header />
      <main className="px-5 py-8 md:px-8">
        <h1 className="text-2xl my-2 font-bold border-b border-surface-border pb-2">
          Favoritos
        </h1>
        <div className="flex gap-2">
          <FiltroConteudo />
          <FiltroOrdemRecentes />
        </div>
      </main>
    </>
  );
}