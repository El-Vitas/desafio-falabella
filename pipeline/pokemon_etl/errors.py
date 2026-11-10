from collections.abc import Mapping


class MissingSettingError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"Environment variable {name} is required but missing or empty")


class LoadCountMismatchError(Exception):
    def __init__(self, expected: Mapping[str, int], loaded: Mapping[str, int]) -> None:
        super().__init__(f"Loaded row counts {dict(loaded)} differ from validated {dict(expected)}")
