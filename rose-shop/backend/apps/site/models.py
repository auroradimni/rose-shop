from django.db import models


class SiteSettings(models.Model):
    """Singleton — images + contact info for the storefront."""

    about_image = models.ImageField(
        upload_to='site/about/',
        blank=True,
        null=True,
        help_text='Home About section + About Us page (1080×1350 px recommended).',
    )
    contact_image = models.ImageField(
        upload_to='site/contact/',
        blank=True,
        null=True,
        help_text='Contact Us page left column (1080×1350 px portrait recommended).',
    )
    phone = models.CharField(
        max_length=40,
        blank=True,
        help_text='Shop phone, e.g. +355 69 704 2889. Shown in footer and Contact page.',
    )
    instagram = models.CharField(
        max_length=80,
        blank=True,
        default='finessia.al',
        help_text='Instagram username only (no @), e.g. finessia.al',
    )
    tiktok = models.CharField(
        max_length=80,
        blank=True,
        default='finessia.al',
        help_text='TikTok username only (no @), e.g. finessia.al',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Site settings'
