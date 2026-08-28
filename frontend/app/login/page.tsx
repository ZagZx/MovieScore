import FormLogin from "@/components/features/auth/login/FormLogin";
import HeaderLanding from "@/components/features/landing/HeaderLanding";


export default async function Login() {
  return (
    <>
      <HeaderLanding/>
      <main
        className="
          flex flex-1 
          items-center 
          justify-center
        "
      >
        <FormLogin />
      </main>
    </>
  );
}