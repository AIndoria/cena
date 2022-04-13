from cena.core import exceptions
from cena.lang import local_provider


def test_cena_registered_exceptions() -> None:
    provider = local_provider()

    lookup = exceptions.cena_registered_exceptions(provider)

    assert "permission" in lookup[exceptions.PermissionDenied]
    assert "The requested resource was not found" in lookup[exceptions.NoEntryFound]
    assert "integrity" in lookup[exceptions.IntegrityError]
