import type { ChangeEventHandler } from "react";
import { HiOutlineSquare2Stack } from "react-icons/hi2";
import Select from "../Select";

interface FiltroOrdemRecentesProps {
  value: "recentes" | "antigos";
  onChange: ChangeEventHandler<HTMLSelectElement>;
}

export default function FiltroOrdemRecentes({ value, onChange }: FiltroOrdemRecentesProps) {
  return (
    <Select
      icon={HiOutlineSquare2Stack}
      aria-label="Ordenar favoritos"
      value={value}
      onChange={onChange}
    >
      <option value="recentes">Mais recentes</option>
      <option value="antigos">Mais antigos</option>
    </Select>
  );
}