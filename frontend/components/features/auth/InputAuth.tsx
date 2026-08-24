import { cn } from "@/lib/utils";
import { cva } from "class-variance-authority";
import { ComponentProps } from "react";

const inputAuthVariants = cva(
  ""
)


interface InputAuthProps extends ComponentProps<"input"> {
  labelValue: string;
  labelClassName?: string;
}


export default function InputAuth({labelValue, labelClassName, className, ...props}: InputAuthProps) {
  return (
    <div className="flex flex-col">
      <label
        htmlFor={props.id}
        className={cn(labelClassName)}
      >
        {labelValue}
      </label>
      <input {...props} 
        className={cn(
          "text-foreground-muted",
          "outline-0 border-b-2 border-primary",
          "focus:border-secondary",
          className
        )}
      />
    </div>
  );
}