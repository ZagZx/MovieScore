import { cva } from "class-variance-authority";
import { ComponentProps } from "react";

const inputAuthVariants = cva(
  ""
)


interface InputAuthProps extends ComponentProps<"input"> {
  label: string;
}

function onFocus() {

}

export default function InputAuth({label, ...props}: InputAuthProps) {
  return (
    <div className="flex flex-col">
      <label
        htmlFor={props.id}
        >
          {label}
      </label>
      <input {...props} 
        className="outline-0 text-foreground-muted"
      />
      <div className="bg-primary h-0.5"></div>
    </div>
  );
}