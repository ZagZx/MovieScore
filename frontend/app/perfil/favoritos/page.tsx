import { HiOutlineChevronDown, HiOutlineSquare2Stack } from "react-icons/hi2";
import Header from "@/components/ui/Header";
import Select from "@/components/ui/Select";

export default function FavoritosPage() {
  return (
    <>
      <Header />
      <main className="px-5 py-8 md:px-8">
        <h1 className="text-3xl my-2 font-bold border-b border-foreground-muted pb-2">
          Favoritos
        </h1>

        <Select 
          icon={HiOutlineSquare2Stack}
          defaultValue="recentes"
        >
          <option value="recentes">Mais recentes</option>
          <option value="antigos">Mais antigos</option>
        </Select>
      </main>
    </>
  );
}