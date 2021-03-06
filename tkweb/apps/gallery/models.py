# encoding: utf8
from __future__ import absolute_import, unicode_literals, division

from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import format_html
from model_utils.managers import InheritanceManager
from sorl.thumbnail import get_thumbnail
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
import os
import logging
from tkweb.apps.gallery.utils import file_name, get_exif_date, get_gfyear, slugify

FORCEDORDERMAX = 10000

logger = logging.getLogger(__name__)

@python_2_unicode_compatible
class Album(models.Model):
    class Meta:
        ordering = ['gfyear', '-eventalbum', 'oldFolder', 'publish_date']
        unique_together = (('gfyear', 'slug'),)

    title = models.CharField(max_length=200, verbose_name='Titel')
    publish_date = models.DateField(blank=True, null=True, default=date.today,
                                    verbose_name='Udgivelsesdato')
    eventalbum = models.BooleanField(default=True, verbose_name='Arrangement')
    gfyear = models.PositiveSmallIntegerField(default=get_gfyear,
                                              verbose_name='Årgang')
    slug = models.SlugField(verbose_name='Kort titel')
    description = models.TextField(blank=True, verbose_name='Beskrivelse')

    oldFolder = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return '%s: %s' % (self.gfyear, self.title)

    def clean(self):
        for m in self.basemedia.all():
            m.isCoverFile = False
            m.save()

        f = self.basemedia.first()
        if f:
            f.isCoverFile = True
            f.save()

@python_2_unicode_compatible
class BaseMedia(models.Model):
    class Meta:
        ordering = ['forcedOrder', 'date', 'slug']
        unique_together = (('album', 'slug'),)

        # Use the pre-1.6 save(). This is a workaround for
        # https://github.com/TK-IT/web/issues/72 This can be removed when the
        # upstream bug https://code.djangoproject.com/ticket/21670 is closed
        select_on_save = True

    IMAGE = 'I'
    VIDEO = 'V'
    AUDIO = 'A'
    OTHER = 'O'
    TYPE_CHOICES = (
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (AUDIO, 'Audio'),
        (OTHER, 'Other'),
    )
    type = models.CharField(max_length=1,
                                      choices=TYPE_CHOICES,
                                      default=OTHER)

    objects = InheritanceManager()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='basemedia')

    date = models.DateTimeField(null=True, blank=True, verbose_name='Dato')
    notPublic = models.BooleanField(default=False, verbose_name='Skjult')
    caption = models.CharField(
        max_length=200, blank=True, verbose_name='Overskrift')

    slug = models.SlugField(null=True, blank=True, verbose_name='Kort titel')

    forcedOrder = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(-FORCEDORDERMAX),
                    MaxValueValidator(FORCEDORDERMAX)],
        verbose_name='Rækkefølge')
    isCoverFile = models.NullBooleanField(null=True,
                                          verbose_name='Vis på forsiden')

    def admin_thumbnail(self):
        if self.type == BaseMedia.IMAGE:
            return self.image.admin_thumbnail()

    admin_thumbnail.short_description = 'Thumbnail'

    def __str__(self):
        return '%s' % (self.slug)

class Image(BaseMedia):
    class Meta:
        # Use the pre-1.6 save(). This is a workaround for
        # https://github.com/TK-IT/web/issues/72 This can be removed when the
        # upstream bug https://code.djangoproject.com/ticket/21670 is closed
        select_on_save = True


    file = VersatileImageField(upload_to=file_name)

    def admin_thumbnail(self):
        return format_html('<img src="{}" />',
                           get_thumbnail(self.file, '150x150').url)

    admin_thumbnail.short_description = 'Thumbnail'

    def clean(self):
        self.type = BaseMedia.IMAGE

        if self.date == None:
            self.date = get_exif_date(self.file)

        if self.slug == None:
            if self.date == None:
                self.slug = slugify(os.path.splitext(os.path.basename(self.file.name))[0])
            else:
                self.slug = self.date.strftime('%Y%m%d%H%M%S_%f')[:len("YYYYmmddHHMMSS_ff")]


class GenericFile(BaseMedia):
    class Meta:
        # Use the pre-1.6 save(). This is a workaround for
        # https://github.com/TK-IT/web/issues/72 This can be removed when the
        # upstream bug https://code.djangoproject.com/ticket/21670 is closed
        select_on_save = True


    originalFile = models.FileField(upload_to=file_name, blank=True)
    file = models.FileField(upload_to=file_name)

    def clean(self):
        if self.slug == None:
            if self.date == None:
                sep = os.path.splitext(os.path.basename(self.file.name))
                self.slug = slugify(sep[0]) + sep[1]
                self.forcedOrder = FORCEDORDERMAX
            else:
                self.slug = self.date.strftime('%Y%m%d%H%M%S_%f')[:len("YYYYmmddHHMMSS_ff")]


@receiver(models.signals.post_save, sender=BaseMedia)
@receiver(models.signals.post_save, sender=Image)
@receiver(models.signals.post_save, sender=GenericFile)
def cleanAlbum(sender, instance, **kwargs):
    if instance.isCoverFile is None:
        instance.album.full_clean()


@receiver(models.signals.post_save, sender=Image)
def generateImageThumbnails(sender, instance, **kwargs):
    image_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='gallery',
        image_attr='file',
    )

    num_created, failed_to_create = image_warmer.warm()
    logger.debug('generateImageThumbnails: %d thumbnails created. Missing %s' % (
                 num_created, failed_to_create))


@receiver(models.signals.post_delete, sender=Image)
def deleteImageThumbnails(sender, instance, **kwargs):
    """
    Delete all thumbnails generated by the VersatileImageField.
    """
    logger.debug('deleteImageThumbnails: called with instance: %s.' % (
        instance))
    instance.file.delete_sized_images()
    logger.debug('deleteImageThumbnails: deleting images')
