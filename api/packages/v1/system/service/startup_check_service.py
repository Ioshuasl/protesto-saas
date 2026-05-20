from packages.v1.system.actions.disk.get_size_action import GetSizeAction


class StartupCheckService:

    def execute(self):

        get_size_action = GetSizeAction()
        get_size_action_result = get_size_action.execute()

        return get_size_action_result

