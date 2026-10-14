class NotFoundException(Exception):
    def __init__(self, message: str):
        """
        Utilizada quando algo não foi encontrado no banco/APIs externas.

        Parâmetros:
         - message: Mensagem de erro
        """
        self.message = message
        super().__init__(self.message)

class EntityNotFoundException(NotFoundException):
    def __init__(self, entity: str, id: int):
        """
        Utilizada quando alguma entidade de certo id não foi encontrada no banco.
        Gera uma mensagem genérica para esse caso

        Parâmetros:
         - entity: Nome da entidade que não foi encontrado o objeto específico
         - id: Id que não foi encontrado
        Exemplo de mensagem de erro (entity="Usuário", id=4):
         - "Usuário de id 4 não encontrado"
        """
        self.message = f"{entity} de id {id} não encontrado"
        super().__init__(self.message)