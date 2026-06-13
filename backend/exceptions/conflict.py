class ConflictException(Exception):
    def __init__(self, message: str):
        '''Utilizada quando algum dado de caráter UNIQUE a ser inserido ou atualizado já existe no banco'''
        self.message = message
        super().__init__(message)