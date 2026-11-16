from django.db import models


class CustomerReview(models.Model):
    username = models.CharField(
        max_length=80,
        blank=True,
        default='',
        help_text='Optional internal note (not shown on the website).',
    )
    image = models.ImageField(upload_to='reviews/')
    text = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(
        default=False,
        help_text='Must be checked for the review to appear on the homepage.',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Customer review'
        verbose_name_plural = 'Customer reviews'

    def __str__(self):
        if self.username:
            return self.username
        return f'Review #{self.pk}'
