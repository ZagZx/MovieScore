import { HiOutlineSquare2Stack } from "react-icons/hi2";
import Select from "../Select";

export default function FiltroOrdemRecentes() {
  return (
    <Select
      icon={HiOutlineSquare2Stack}
    >
      <option value="recentes">Mais recentes</option>
      <option value="antigos">Mais antigos</option>
    </Select>
  );
}