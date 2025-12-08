"""Azure helpers for common cloud operations."""

from .keyvault import get_keyvault_secret

__all__ = ["get_keyvault_secret"]
