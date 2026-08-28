import { getUsuarios } from "@/actions/usuario";

export default async function UsuariosTeste() {
  const response = await getUsuarios({limit: 5, cursor: 0});
  const usuarios = response?.data;

  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex flex-1 w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        { usuarios?.data.map((usuario) => 
          <div key={usuario.id} className="m-4">
            <ul>
              <li>{usuario.id}</li>
              <li>{usuario.nome}</li>
              <li>{usuario.email}</li>
              <li>{usuario.data_criacao}</li>
              <li>
                <img 
                  src={usuario.foto_perfil_url || undefined}
                  title="Foto de perfil"
                  width={70} 
                />
              </li>
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}
