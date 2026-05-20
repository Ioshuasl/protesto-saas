class PyrosError(Exception):
    """Base error for the Pyros package."""


class PyrosValidationError(PyrosError):
    """Validation error for invalid query inputs."""


class PyrosSecurityError(PyrosError):
    """Security error for unsafe or forbidden operations."""


class PyrosCompilationError(PyrosError):
    """Compilation error while generating SQL from AST."""


class PyrosExecutionError(PyrosError):
    """Execution error while running compiled SQL."""


class PyrosTransactionError(PyrosError):
    """Transaction error for transactional flow failures."""
