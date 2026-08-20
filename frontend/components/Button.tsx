import { cn } from "@/lib/utils";
import { cva, VariantProps } from "class-variance-authority";
import { ClassArray } from "clsx";

import { ComponentProps, ReactNode } from "react";


const buttonVariants = cva(
  "cursor-pointer transition-colors duration-200 shadow shadow-black rounded-xl",
  {
    variants: {
      variant: {
        primary: "bg-primary text-white hover:bg-white hover:text-black"
      },
      size: {
        sm: "h-8 px-4 text-sm",
        md: "h-10 px-6 text-base",
        lg: "h-12 px-12 text-lg"
      }
    },
    defaultVariants: {
      variant: "primary",
      size: "md"
    }
  }
);

interface ButtonProps extends ComponentProps<"button">, VariantProps<typeof buttonVariants> {
  children: ReactNode
}  


export default function Button({ children, className, variant, size, ...props }: ButtonProps) {
  return (
    <button {...props}
      className={cn(buttonVariants({variant, size}), className)}
    >
      {children}
    </button>
  );
}