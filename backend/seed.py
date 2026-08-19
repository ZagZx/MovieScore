"""Cliente de terminal para popular o banco com dados fictícios (Faker).

Uso:
    python seed.py --usuarios 1000 --conteudos 2000 --avaliacoes 5000
    python seed.py --usuarios 50000 --conteudos 100000 --avaliacoes 300000 --batch 2000

O objetivo é gerar dados coerentes para as tabelas do projeto e permitir
testes de volume sem depender de dados manuais.
"""

import argparse
import random
import sys
import time
from decimal import Decimal

from faker import Faker
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import SessionFactory
from models import Assistido, Avaliacao, Conteudo, Favorito, Usuario
from models.conteudo import TipoConteudo
from utils import get_password_hash

fake = Faker("pt_BR")

SENHA_PADRAO = get_password_hash("12345678")
FONTES_POR_TIPO = {
    TipoConteudo.ANIME: "https://kitsu.io/api/edge",
    TipoConteudo.FILME: "https://api.themoviedb.org/3",
    TipoConteudo.SERIE: "https://api.themoviedb.org/3",
}
TIPOS_CONTEUDO = list(TipoConteudo)
VALORES_ESTRELAS = [
    Decimal("1.0"),
    Decimal("1.5"),
    Decimal("2.0"),
    Decimal("2.5"),
    Decimal("3.0"),
    Decimal("3.5"),
    Decimal("4.0"),
    Decimal("4.5"),
    Decimal("5.0"),
]


def _limitar_texto(texto: str, limite: int) -> str:
    return texto[:limite]


def _imprimir_progresso(rotulo: str, atual: int, total: int, inicio: float) -> None:
    if total <= 0:
        return

    percentual = (atual / total) * 100
    decorrido = time.perf_counter() - inicio
    sys.stdout.write(
        f"\r{rotulo}: {atual}/{total} ({percentual:5.1f}%) - {decorrido:,.1f}s"
    )
    sys.stdout.flush()
    if atual >= total:
        sys.stdout.write("\n")
        sys.stdout.flush()


def _salvar_lote(session: Session, objetos: list) -> None:
    session.add_all(objetos)
    session.flush()
    session.commit()


def _obter_ids(session: Session, modelo) -> list[int]:
    return list(session.execute(select(modelo.id).order_by(modelo.id)).scalars().all())


def popular_usuarios(session: Session, quantidade: int, tamanho_lote: int) -> list[int]:
    """Popula a tabela de usuários e retorna os IDs criados."""
    if quantidade <= 0:
        return []

    contador_atual = session.scalar(select(func.count(Usuario.id))) or 0
    usuarios: list[Usuario] = []
    inicio = time.perf_counter()

    for indice in range(quantidade):
        sequencia = contador_atual + indice + 1
        usuario = Usuario(
            nome=_limitar_texto(fake.name(), 50),
            email=f"usuario.{sequencia}@example.com",
            senha_hash=SENHA_PADRAO,
            #   foto_perfil_path=(f"/storage/usuarios/fotos/usuario_{sequencia}.jpg" if random.random() < 0.4 else None),
        )
        usuarios.append(usuario)

        if len(usuarios) == tamanho_lote or indice == quantidade - 1:
            _salvar_lote(session, usuarios)
            usuarios = []
            _imprimir_progresso("Usuários", indice + 1, quantidade, inicio)

    return _obter_ids(session, Usuario)


def popular_conteudos(
    session: Session, quantidade: int, tamanho_lote: int
) -> list[int]:
    """Popula a tabela de conteúdos e retorna os IDs criados."""
    if quantidade <= 0:
        return []

    ultimo_id_externo = (
        session.scalar(select(func.coalesce(func.max(Conteudo.id_externo), 0))) or 0
    )
    conteudos: list[Conteudo] = []
    inicio = time.perf_counter()

    for indice in range(quantidade):
        tipo = random.choice(TIPOS_CONTEUDO)
        conteudo = Conteudo(
            id_externo=ultimo_id_externo + indice + 1,
            api_fonte=FONTES_POR_TIPO[tipo],
            tipo=tipo,
        )
        conteudos.append(conteudo)

        if len(conteudos) == tamanho_lote or indice == quantidade - 1:
            _salvar_lote(session, conteudos)
            conteudos = []
            _imprimir_progresso("Conteúdos", indice + 1, quantidade, inicio)

    return _obter_ids(session, Conteudo)


def popular_avaliacoes(
    session: Session, quantidade: int, tamanho_lote: int
) -> list[int]:
    """Popula a tabela de avaliações usando usuários e conteúdos existentes."""
    if quantidade <= 0:
        return []

    usuario_ids = _obter_ids(session, Usuario)
    conteudo_ids = _obter_ids(session, Conteudo)
    if not usuario_ids or not conteudo_ids:
        raise ValueError(
            "É necessário popular usuários e conteúdos antes das avaliações."
        )

    avaliacoes: list[Avaliacao] = []
    inicio = time.perf_counter()

    for indice in range(quantidade):
        avaliacao = Avaliacao(
            usuario_id=random.choice(usuario_ids),
            conteudo_id=random.choice(conteudo_ids),
            estrelas=random.choice(VALORES_ESTRELAS),
            comentario=(
                fake.sentence(nb_words=random.randint(8, 16))
                if random.random() < 0.7
                else None
            ),
        )
        avaliacoes.append(avaliacao)

        if len(avaliacoes) == tamanho_lote or indice == quantidade - 1:
            _salvar_lote(session, avaliacoes)
            avaliacoes = []
            _imprimir_progresso("Avaliações", indice + 1, quantidade, inicio)

    return _obter_ids(session, Avaliacao)


def popular_favoritos(
    session: Session, quantidade: int, tamanho_lote: int
) -> list[int]:
    """Popula a tabela de favoritos usando usuários e conteúdos existentes."""
    if quantidade <= 0:
        return []

    usuario_ids = _obter_ids(session, Usuario)
    conteudo_ids = _obter_ids(session, Conteudo)
    if not usuario_ids or not conteudo_ids:
        raise ValueError(
            "É necessário popular usuários e conteúdos antes dos favoritos."
        )

    favoritos: list[Favorito] = []
    inicio = time.perf_counter()

    for indice in range(quantidade):
        favorito = Favorito(
            usuario_id=random.choice(usuario_ids),
            conteudo_id=random.choice(conteudo_ids),
        )
        favoritos.append(favorito)

        if len(favoritos) == tamanho_lote or indice == quantidade - 1:
            _salvar_lote(session, favoritos)
            favoritos = []
            _imprimir_progresso("Favoritos", indice + 1, quantidade, inicio)

    return _obter_ids(session, Favorito)


def popular_assistidos(
    session: Session, quantidade: int, tamanho_lote: int
) -> list[int]:
    """Popula a tabela de assistidos usando usuários e conteúdos existentes."""
    if quantidade <= 0:
        return []

    usuario_ids = _obter_ids(session, Usuario)
    conteudo_ids = _obter_ids(session, Conteudo)
    if not usuario_ids or not conteudo_ids:
        raise ValueError(
            "É necessário popular usuários e conteúdos antes dos assistidos."
        )

    assistidos: list[Assistido] = []
    inicio = time.perf_counter()

    for indice in range(quantidade):
        assistido = Assistido(
            usuario_id=random.choice(usuario_ids),
            conteudo_id=random.choice(conteudo_ids),
        )
        assistidos.append(assistido)

        if len(assistidos) == tamanho_lote or indice == quantidade - 1:
            _salvar_lote(session, assistidos)
            assistidos = []
            _imprimir_progresso("Assistidos", indice + 1, quantidade, inicio)

    return _obter_ids(session, Assistido)


def main() -> None:
    parser = argparse.ArgumentParser(description="Popula o banco com dados fictícios.")
    parser.add_argument(
        "--usuarios", type=int, default=1000, help="Quantidade de usuários a criar"
    )
    parser.add_argument(
        "--conteudos", type=int, default=2000, help="Quantidade de conteúdos a criar"
    )
    parser.add_argument(
        "--avaliacoes", type=int, default=5000, help="Quantidade de avaliações a criar"
    )
    parser.add_argument(
        "--favoritos", type=int, default=3000, help="Quantidade de favoritos a criar"
    )
    parser.add_argument(
        "--assistidos", type=int, default=3000, help="Quantidade de assistidos a criar"
    )
    parser.add_argument(
        "--batch", type=int, default=1000, help="Tamanho do lote para inserção"
    )
    args = parser.parse_args()

    with SessionFactory() as session:
        print("Populando usuários...")
        popular_usuarios(session, args.usuarios, args.batch)
        print("Populando conteúdos...")
        popular_conteudos(session, args.conteudos, args.batch)
        print("Populando avaliações...")
        popular_avaliacoes(session, args.avaliacoes, args.batch)
        print("Populando favoritos...")
        popular_favoritos(session, args.favoritos, args.batch)
        print("Populando assistidos...")
        popular_assistidos(session, args.assistidos, args.batch)

    print("Seed concluído com sucesso.")


if __name__ == "__main__":
    main()
