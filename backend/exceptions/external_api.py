class ExternalAPIException(Exception):
    def __init__(self, message: str, status_code: int = 502):
        """
        Exceção genérica para erros de APIs externas.

        Parâmetros:
         - message: Mensagem legível para logs / respostas HTTP
         - status_code: Código HTTP sugerido para repassar ao cliente
        """
        self.message = message
        self.status_code = status_code
        super().__init__(message)
