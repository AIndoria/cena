import enum

from cena.schema._cena import CenaModel


class SupportedMigrations(str, enum.Enum):
    nextcloud = "nextcloud"
    chowdown = "chowdown"
    paprika = "paprika"
    cena_alpha = "cena_alpha"


class DataMigrationCreate(CenaModel):
    source_type: SupportedMigrations
