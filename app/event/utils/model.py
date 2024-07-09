import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_delete, post_delete
from app.event.utils.thread_local import get_current_request

MODEL_REGISTRY = {}


def register_model(model: models.Model, prefix):
    """
        Maps Model class and Prefix
    """
    if MODEL_REGISTRY.get(prefix) is not None:
        if MODEL_REGISTRY[prefix] != model:
            raise AttributeError('Prefix already in use')
    # noinspection PyProtectedMember
    model._meta.get_field('id').prefix = prefix  # pylint: disable=protected-access
    MODEL_REGISTRY[prefix] = model


def model_prefix(prefix):
    """
        Decorator for prefixing Models primary key
    """

    def func(clazz):
        register_model(clazz, prefix)
        return clazz

    return func


class AbstractBaseModel(models.Model):
    """
        - All resource based models should inherit this model.
        - Contains columns like created_user, last_modified_user, last_modified_date, created_date, etc
    """

    last_modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    created_user_id: int
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='%(app_label)s_%(class)s_created_user')
    last_modified_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                           related_name='%(app_label)s_%(class)s_last_modified_user')
    is_active = models.BooleanField(default=False, blank=False, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self._fill_pre_save_fields()
        return super().save(force_insert, force_update, using, update_fields)

    def _fill_pre_save_fields(self):
        current_request = get_current_request()
        user_model_cls = get_user_model()
        if current_request and current_request.user and isinstance(current_request.user, user_model_cls):
            if self.created_user_id is None:
                self.created_user = current_request.user
            self.last_modified_user = current_request.user

    default_manager = models.Manager()
    objects = models.Manager()

    class Meta:
        abstract = True


class AbstractRemoteBaseModel(models.Model):
    """
        - All resource based models should inherit this model.
        - Contains columns like created_user, last_modified_user, last_modified_date, created_date, etc
        - Modified created_user, last_modified_user fields
    """

    last_modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    created_user_id: int
    created_user_remote_id = models.BigIntegerField(null=True, blank=True)
    last_modified_user_remote_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False, blank=False, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self._fill_pre_save_fields()
        return super().save(force_insert, force_update, using, update_fields)

    def _fill_pre_save_fields(self):
        current_request = get_current_request()
        user_model_cls = get_user_model()
        if current_request and current_request.user and isinstance(current_request.user, user_model_cls):
            if self.created_user_id is None:
                self.created_user_remote_id = current_request.user
            self.last_modified_user_remote_id = current_request.user

    default_manager = models.Manager()
    objects = models.Manager()

    class Meta:
        abstract = True


class BaseModel(AbstractRemoteBaseModel):
    """
        - Model overrides the id generation logic
    """
    id = models.BigAutoField(primary_key=True, auto_created=True)

    @property
    def sid(self):
        """
            Return PK
        """
        return self.id

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """
        Query manager for SoftDeleteModel
    """

    def delete(self):  # pylint: disable=unused-argument
        """
            Soft Delete Operation
        """
        for obj in self:
            obj.delete()


class SoftDeleteManager(models.Manager):
    """
    Model Manager for SoftDeleteModel. Assumes the model to have is_deleted field
    """

    def get_queryset(self):
        """
        :return: Queryset excluding softly deleted rows
        """
        return SoftDeleteQuerySet(self.model, using=self._db).exclude(is_deleted=True)

    def all_with_deleted(self):
        """ Returns a queryset with ALL records (without filtering out deleted) """
        return SoftDeleteQuerySet(self.model, using=self._db)

    def delete(self):
        """ no op """


# assumes the id will always be an integer
class SoftDeleteModel(BaseModel):
    """ Abstract model providing an is_deleted column and related functionality for soft-deletes """
    objects = SoftDeleteManager()
    is_deleted = models.BooleanField(default=False, blank=False, null=True)
    deleted_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        pre_delete.send(self.__class__, instance=self)
        self.is_deleted = True
        self.deleted_at = datetime.datetime.utcnow()
        self.save()
        post_delete.send(self.__class__, instance=self)
