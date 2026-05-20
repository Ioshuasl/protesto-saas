from abc import abstractmethod


class BaseAction:

    """
    Classe abstrata base para todos as actions do sistema.
    Obriga implementação de um método execute().
    """

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Método abstrato obrigatório a ser implementado pelas subclasses.
        Deve conter a lógica principal do repositório.
        """
        pass