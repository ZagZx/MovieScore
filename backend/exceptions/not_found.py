class NotFoundException(Exception):
    def __init__(self, entity: str, id: int):
        '''
        Utilizada quando alguma entidade de certo id não foi encontrada no banco

        Parâmetros:
         - entity: Nome da entidade que não foi encontrado o objeto específico
         - id: Id que não foi encontrado
        Exemplo de mensagem de erro (entity="Usuário", id=4):
         - "Usuário de id 4 não encontrado"
        '''
        self.message = f"{entity} de id {id} não encontrado"
        super().__init__(self.message)