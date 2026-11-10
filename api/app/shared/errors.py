class MissingSettingError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"Environment variable {name} is required but missing or empty")
