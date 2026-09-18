import { cn } from "@/lib/utils";
import { cva, VariantProps } from "class-variance-authority";
import Link, { LinkProps as NextLinkProps } from "next/link";
import { AnchorHTMLAttributes, ReactNode } from "react";

const linkVariants = cva(
  "cursor-pointer underline transition-colors duration-300",
  {
    variants: {
      variant: {
        primary: "text-primary hover:text-primary-hover",
        // secondary: "bg-secondary text-secondary-foreground hover:bg-secondary-hover",
        // outline: "bg-neutral text-neutral-foreground border-neutral-border border-2 shadow-0 hover:bg-neutral-hover"
      },
      size: {
        sm: "text-sm",
        md: "text-base",
        lg: "text-lg",
        xl: "text-xl",
        xl2: "text-2xl",
        xl4: "text-4xl",
      }
    },
    defaultVariants: {
      variant: "primary",
      size: "md"
    }
  }
);

type LinkHighlightProps = NextLinkProps &
  VariantProps<typeof linkVariants> &
  Omit<AnchorHTMLAttributes<HTMLAnchorElement>, keyof NextLinkProps> & {
    children: ReactNode;
  };

export default function LinkHighlight({ children, className, variant, size, ...props }: LinkHighlightProps) {
  return (
    <Link {...props}
      className={cn(linkVariants({ variant, size }), className)}
    >
      {children}
    </Link>
  );
}