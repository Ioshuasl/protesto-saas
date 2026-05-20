from packages.v1.nfse.actions.parametros_index_action import ParametrosIndexAction


class ParametrosIndexService:
    def execute(self):
        action = ParametrosIndexAction()
        return action.execute()

