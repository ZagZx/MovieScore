class UnsupportedMediaTypeException(Exception):
    def __init__(self, message: str):
        '''
        Utilizada quando o tipo de mídia recebido não é suportado

        Exemplo: 
         - application/pdf quando deveria ser image/png ou image/jpeg 
        '''
        self.message = message
        super().__init__(self.message)