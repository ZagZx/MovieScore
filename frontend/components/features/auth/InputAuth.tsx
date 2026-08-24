"use client";

import { cn } from "@/lib/utils";
import { ComponentProps, useState } from "react";
import { AiOutlineEye, AiOutlineEyeInvisible } from "react-icons/ai";


interface InputAuthProps extends ComponentProps<"input"> {
  labelValue: string;
  labelClassName?: string;
}


export default function InputAuth({labelValue, labelClassName, className, ...props}: InputAuthProps) {
  const isPassword = props.type === "password";
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const inputType = isPassword && isPasswordVisible ? "text" : props.type;

  return (
    <div className="flex flex-col">
      <label
        htmlFor={props.id}
        className={cn(labelClassName)}
      >
        {labelValue}
      </label>
      <div className="relative">
        <input {...props}
          type={inputType}
          className={cn(
            "w-full pr-8 text-foreground-muted",
            "outline-0 border-b-2 border-primary",
            "focus:border-secondary",
            className
          )}
        />
        {isPassword && (
          <button
            type="button"
            aria-label={isPasswordVisible ? "Ocultar senha" : "Exibir senha"}
            title={isPasswordVisible ? "Ocultar senha" : "Exibir senha"}
            className="absolute right-0 top-1 cursor-pointer text-primary text-xl"
            onClick={() => setIsPasswordVisible((visible) => !visible)}
          >
            {isPasswordVisible ? <AiOutlineEyeInvisible /> : <AiOutlineEye />}
          </button>
        )}
      </div>
    </div>
  );
}