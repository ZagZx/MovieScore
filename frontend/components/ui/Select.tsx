import { ComponentProps, ReactNode } from "react";
import type { IconType } from "react-icons";
import { HiOutlineChevronDown } from "react-icons/hi2";


interface SelectProps extends ComponentProps<"select">{
  children: ReactNode;
  icon?: IconType;
}

// ARRUMAR
// quando tá sem ícone fica um espaço vazio
export default function Select({
  children,
  icon,
  ...props
}: SelectProps
){
  const Icon = icon;

  return(
    <div className="relative ml-auto w-fit">
      { Icon &&
        <div className="pointer-events-none absolute left-3 top-1/2 z-10 size-4 -translate-y-1/2">
          <Icon />
        </div>
      }
      <select 
        {...props} 
        className="block h-10 cursor-pointer appearance-none rounded-md bg-neutral text-sm px-9 text-neutral-foreground outline-none transition-colors hover:bg-neutral-hover focus-visible:ring-2 focus-visible:ring-primary"
      >
        { children }
      </select>
      <div className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2">
        <HiOutlineChevronDown/>
      </div>
    </div>
  );
}