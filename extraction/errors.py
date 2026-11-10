class ExtractionError(Exception):
    pass


class PokeApiRequestError(ExtractionError):
    def __init__(self, url: str, reason: str) -> None:
        super().__init__(f"Request to {url} failed: {reason}")


class InvalidPokemonPayloadError(ExtractionError):
    def __init__(self, source: str, problem: str) -> None:
        super().__init__(f"Invalid PokeAPI payload ({source}): {problem}")


class IncompleteExtractionError(ExtractionError):
    pass


class MissingSettingError(ExtractionError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Environment variable {name} is required but missing or empty")
