from django.db import models


class UserGroup(models.Model):
    '''
    auth_user_groups is how django handels user group membership by default.
    This class simply allows me to interface with that table without going
    through the djanog admin api.

    Notice the managed=False... this means that django will not try to create
    a migration if this class is created or altered.
    '''

    user = models.ForeignKey('auth.User')
    group = models.ForeignKey('auth.Group')

    class Meta:
        db_table = 'auth_user_groups'
        managed = False
