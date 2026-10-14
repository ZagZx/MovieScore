import { cn } from "@/lib/utils";
import { ClassValue } from "clsx";
import { ComponentProps, ReactNode } from "react";

interface FieldErrorProps extends ComponentProps<"span">{
  children: ReactNode;
}

export default function FieldError({children, className, ...props}: FieldErrorProps) {
  return (
    <span {...props}
      className={cn(
        "text-sm text-primary",
        className
      )}
    >
      {children}
    </span>
  );
}