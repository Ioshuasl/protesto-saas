from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DialectCapabilities:
    supports_returning: bool
    supports_merge: bool
    supports_offset_fetch: bool
    supports_update_or_insert: bool

    @classmethod
    def default_firebird(cls) -> "DialectCapabilities":
        return cls(
            supports_returning=True,
            supports_merge=False,
            supports_offset_fetch=False,
            supports_update_or_insert=True,
        )
