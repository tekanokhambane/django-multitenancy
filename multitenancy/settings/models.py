from django.db import models

# Create your models here.

class BaseSetting(models.Model):
    company_name = models.CharField(max_length=250, null=False, blank=False)
    logo = models.ImageField()

    class Meta:
        abstract = True
    
    def __str__(self) -> str:
        return self.company_name
    # Override to fetch ForeignKey values in the same query when
    # retrieving settings (e.g. via `for_request()`)
    select_related = None


    @classmethod
    def base_queryset(cls):
        """
        Returns a queryset of objects of this type to use as a base.
        You can use the `select_related` attribute on your class to
        specify a list of foreign key field names, which the method
        will attempt to select additional related-object data for
        when the query is executed.
        If your needs are more complex than this, you can override
        this method on your custom class.
        """
        queryset = cls.objects.all()
        if cls.select_related is not None:
            queryset = queryset.select_related(*cls.select_related)
        return queryset

    @classmethod
    def _get_or_create(cls):
        """
        Internal convenience method to get or create the first instance.
        We cannot hardcode `pk=1`, for example, as not all database backends
        use sequential IDs (e.g. Postgres).
        """

        first_obj = cls.base_queryset().first()
        if first_obj is None:
            return cls.objects.create()
        return first_obj
