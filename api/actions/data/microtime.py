import time


class Microtime:
    """
    Utilitário para manipulação de tempo com alta precisão (microssegundos).
    """

    @staticmethod
    def get() -> float:
        """
        Retorna o timestamp Unix atual com precisão de microssegundos.
        Equivalente ao microtime(true) do PHP.
        """
        return time.time()

    @staticmethod
    def as_int() -> int:
        """
        Retorna o tempo atual puramente em microssegundos (Inteiro).
        Útil para gerar IDs únicos ou ordenação precisa.
        """
        # Pega em nanosegundos e converte para microssegundos
        return time.time_ns() // 1000

    @staticmethod
    def diff(start_time: float) -> float:
        """
        Calcula a diferença (duração) em segundos com precisão.
        """
        return time.time() - start_time
