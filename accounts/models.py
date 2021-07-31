from __future__ import unicode_literals
''' Import Remita Model'''

import hashlib
import os
import datetime
import json
from decimal import Decimal
import uuid

from PIL import Image, ImageOps, ImageDraw
from datetime import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Sum, F, Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.db import models
from django.conf import settings
# from BlogAppApi.storage_backends import PrivateMediaStorage


class User(AbstractBaseUser, PermissionsMixin):
    """User model class"""
    auto_password = models.CharField(
        _('auto_password'), max_length=128, null=True)
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    regular_email_status = models.DateTimeField(
        _('regular email status'), null=True)
    token_email_status = models.DateTimeField(
        _('token email status'), null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    remember_token = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_verified = models.BooleanField(
        _('user verified'),
        default=False,
        help_text=_('Designates whether the user is verified using email.'),
    )
    is_blocked = models.BooleanField(
        _('account block'),
        default=True,
        help_text=_('Designates whether the user is blocked.'),
    )
    is_suspended = models.BooleanField(
        _('account suspend status'),
        default=False,
        help_text=_('Check if user account has been suspended.'),
    )
    deleted_at = models.DateTimeField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = "users"



    def has_profile(self):
        try:
            # Profile.objects.filter(user=self.pk).first()
            return hasattr(self, 'profile')
        except Exception as e:
            return False


    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        try:
            profile = Profile.objects.get(user=self.pk)
            full_name = '%s %s' % (profile.last_name, profile.first_name)
            return full_name.strip()
        except:
            return '%s - Regular not fully registered' % self.email

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        try:
            profile = Profile.objects.get(user=self.pk)
            full_name = '%s ' % profile.last_name
            return full_name.strip()
        except:
            return '%s - Regular not fully registered' % (self.email,)

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)



class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def get_image_path(instance, filename):
    filename, extension = os.path.splitext(filename)
    filename = "{}{}".format(hashlib.sha1(
        str(instance.id).encode('utf8')).hexdigest()[:], '.png')
    return os.path.join('photos', filename)



def get_doc_path(instance, filename):
    filename, extension = os.path.splitext(filename)
    filename = "{}{}".format(hashlib.sha1(
        str(instance.id).encode('utf8')).hexdigest()[:], '.png')
    return os.path.join('doc', filename)



import random
def get_uploadedfile_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/document/<user_full_name>/<filename>
    return 'document/{}/{}'.format(instance.user.profile.get_full_name, filename)


class Profile(models.Model):
    """User profile model object linked to User object"""
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    avatar = models.FileField(upload_to=get_image_path, blank=True, null=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateField(default=datetime.today)
    updated_at = models.DateTimeField(auto_now=True)
    
    


    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        db_table = "profiles"

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    def resize_uploaded_img(self):
        try:
            size = (64, 64)
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)

            image = Image.open(self.avatar.path)
            output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
            mask.resize(size, Image.ANTIALIAS)
            output.putalpha(mask)
            output.save(self.avatar.path)
            # image.thumbnail((64, 64), Image.ANTIALIAS)
            # image.resize((60, 60), Image.ANTIALIAS)
            # image.save(self.avatar.path)
        except IOError as e:
            print("cannot create thumbnail for '%s'" % e)
        except Exception as e:
            print("cannot create thumbnail: '%s'" % e)
