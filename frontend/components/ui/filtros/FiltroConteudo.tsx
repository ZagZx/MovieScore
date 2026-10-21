import { HiOutlineAdjustmentsHorizontal } from "react-icons/hi2";
import Select from "../Select";

export default function FiltroConteudo() {
  return (
    <Select
      icon={HiOutlineAdjustmentsHorizontal}
    >
      <option value="">Todos</option>
      <option value="filmes">Filmes</option>
      <option value="series">Séries</option>
      <option value="animes">Animes</option>
    </Select>
  );
}