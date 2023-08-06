"""Declares :class:`AgreementAcceptanceService`."""
from django.apps import apps


class AgreementAcceptanceService:
    """Provides an interface to accept :term:`Platform Agreements`."""

    def accept(self, checksum, subject, host):
        """Accepts the :term:`Platform Agreement` `oid` for a
        :term:`Subject`.

        Args:
            checksum (:obj:`int`): the checksum of the agreement to accept.
            subject (:obj:`uuid.UUID`): identifies the :term:`Subject`.
            host (:obj:`str`): the remote host address (IPv4/IPv6) from
                which the HTTP request to accept the agreement was made.

        Returns:
            :class:`types.NoneType`
        """
        AcceptedPlatformAgreement = apps.get_model(
            'iam.AcceptedPlatformAgreement')

        AcceptedPlatformAgreement.objects.create(agreement_id=checksum,
            subject_id=subject, host=host)
