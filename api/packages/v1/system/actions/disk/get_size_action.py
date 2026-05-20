import shutil



class GetSizeAction:

    def execute(self):

        # Verificar espaço em disco
        total, used, free = shutil.disk_usage("/")

        # Converter de bytes para gigabytes
        total_gb = total / (1024 ** 3)
        used_gb = used / (1024 ** 3)
        free_gb = free / (1024 ** 3)

        return {
            "total" : round(total_gb, 2),
            "used" : round(used_gb, 2),
            "free" : round(free_gb, 2)
        }

    