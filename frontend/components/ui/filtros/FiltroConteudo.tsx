import type { ChangeEventHandler } from "react";
import { HiOutlineAdjustmentsHorizontal } from "react-icons/hi2";
import Select from "../Select";

interface FiltroConteudoProps {
  value: string;
  onChange: ChangeEventHandler<HTMLSelectElement>;
}

export default function FiltroConteudo({ value, onChange }: FiltroConteudoProps) {
  return (
    <Select
      icon={HiOutlineAdjustmentsHorizontal}
      aria-label="Filtrar favoritos por tipo de conteúdo"
      value={value}
      onChange={onChange}
    >
      <option value="">Todos</option>
      <option value="filme">Filmes</option>
      <option value="serie">Séries</option>
      <option value="anime">Animes</option>
    </Select>
  );
}