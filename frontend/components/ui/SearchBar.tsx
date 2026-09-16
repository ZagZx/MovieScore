import { FiSearch } from "react-icons/fi";

export default function SearchBar() {
  return(
    <div className="flex w-full max-w-140 items-center gap-3 rounded-full border border-input-border bg-input pl-4 pr-2 py-1 shadow-inner shadow-input-shadow">
      <input
        type="text"
        placeholder="Pesquisar"
        className="w-full bg-transparent text-foreground placeholder:text-foreground-muted outline-none"
      />
      <button
        type="button"
        aria-label="Pesquisar"
        className="flex size-9 shrink-0 items-center justify-center rounded-full text-xl text-foreground transition-colors hover:bg-input-hover cursor-pointer"
      >
        <FiSearch />
      </button>
    </div>
  );
}