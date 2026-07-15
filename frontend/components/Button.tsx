import { ComponentProps, ReactNode } from "react";

interface ButtonProps extends ComponentProps<"button"> {
  children: ReactNode
}


export default function Button({ children, ...props }: ButtonProps) {
  return (
    <button {...props}
      className="
        cursor-pointer
        bg-primary
        text-white
        hover:bg-white
        hover:text-black
        transition-all
        duration-200
        py-2 px-10
        rounded-2xl
        shadow-black
        shadow
      "
    >
      {children}
    </button>
  );
}