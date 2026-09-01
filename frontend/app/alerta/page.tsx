"use client"

import Button from "@/components/ui/Button";
import { alert } from "@/lib/alert";

export default function Alerta() {
  function clickHandler() {
    alert.fire({
      title: "Teste",
      icon: "success",
      text: "sei la vei"
    })
  }

  return (
    <Button onClick={clickHandler}>Alerta</Button>
  );
}