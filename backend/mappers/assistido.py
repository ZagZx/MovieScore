from schemas.conteudo import ImagensConteudo
from schemas.assistido import SerieAssistidaRead
from models import Assistido, Serie
from .serie import SerieMapper


class AssistidoMapper:
    @staticmethod
    def map_serie(serie: Serie, assistido: Assistido) -> SerieAssistidaRead:
        return SerieAssistidaRead(
            id=serie.conteudo.id_externo,
            titulo=serie.titulo,
            titulo_original=serie.titulo_original,
            status=serie.status,
            imagens=ImagensConteudo(
                capa=SerieMapper.map_image(serie.capa, "w500"),
                banner=SerieMapper.map_image(serie.banner, "original"),
            ),
            data_lancamento=serie.data_lancamento,
            data_adicao=assistido.data_adicao,
        )

    @staticmethod
    def map_series(items: list[tuple[Serie, Assistido]]) -> list[SerieAssistidaRead]:
        return [
            AssistidoMapper.map_serie(serie, assistido)
            for serie, assistido in items
        ]
