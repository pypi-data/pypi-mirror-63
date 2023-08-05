from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.db import models
from django.forms import widgets
from django.http import JsonResponse


class DjangoLinkAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        """
        http://stackoverflow.com/questions/2431727/django-admin-hide-a-model
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    @property
    def media(self):
        original_media = super(DjangoLinkAdmin, self).media
        css = {
            'all': (
                settings.STATIC_URL + 'admin/ckeditor_link/css/link_admin.css',
            )
        }
        new_media = widgets.Media(css=css)
        return original_media + new_media

    def get_urls(self):
        """
        add verify url.
        """
        my_urls = [
            url(
                r'^verify/$',
                self.admin_site.admin_view(self.verify),
                name=self._get_verify_url_name()
            ),
        ]
        return my_urls + super(DjangoLinkAdmin, self).get_urls()

    def _get_verify_url_name(self):
        return '{0}_{1}_verify'.format(self.model._meta.app_label,
                                       self.model._meta.model_name)

    def verify(self, request):
        """
        verify data with modelform, send through data.
        :param request:
        :return:
        """
        form = self.get_form(request, )(request.POST)
        if form.is_valid():
            verified_data = form.cleaned_data
            obj = self.model(**verified_data)
            link_value = ''
            # prepopulate href
            if (getattr(obj, 'get_link', None)):
                link_value = obj.get_link()
            # basic serialize only
            for key, value in verified_data.items():
                if isinstance(value, models.Model):
                    verified_data[key] = value.id
            return_data = {"valid": 'true', 'data': verified_data, 'link_value': link_value}
        else:
            errors = form.errors
            return_data = {"valid": 'false', 'errors': errors}
        return JsonResponse(return_data)

    def save_model(self, request, obj, form, change):
        """
        no save!
        """
        return False

    def get_changeform_initial_data(self, request):
        initial = super(DjangoLinkAdmin, self).get_changeform_initial_data(request)
        if request.GET.get('page', None):
            initial['cms_page'] = request.GET.get('page')
        return initial
