"""Declares authentication backends for the :mod:`iam.ext.django` Django
application.
"""
from iam.ext.django.models import Subject


class LocalSubjectBackend:
    model = Subject

    def authenticate(self, request, realm, principal, credential, **kwargs):
        """Authenticate a :term:`Subject` using the provided :term:`Principal`
        and :term:`Credential`.
        """
        try:
            subject = principal.resolve(realm, self.get_resolver())
        except self.model.DoesNotExist:
            credential.cooldown()
            return None
        else:
            if subject.check_credential(credential)\
            and self.can_authenticate(subject):
                return subject

    def can_authenticate(self, subject):
        """Return a boolean indicating if a :term:`Subject` may
        authenticate.
        """
        return True

    def get_user(self, subject_id):
        """Return a :class:`Subject` instance using the given `subject_id`."""
        return self.model.objects.get(pk=subject_id)

    def get_resolver(self):
        """Return an instance that can resolve a :class:`~iam.domain.Principal`."""
        return self.model.objects
