# -*- coding: utf-8 -*-
import hashlib
import hmac
from django import forms
from django.conf import settings
from django.utils.crypto import constant_time_compare


class DeleteForm(forms.Form):
    signature = forms.CharField(required=True)
    path = forms.CharField(required=True)

    def clean_path(self):
        path = self.cleaned_data.get('path', '')
        if not path.startswith(('static/', 'templates/')):
            raise forms.ValidationError("Invalid path")
        return path

    def clean(self):
        data = super(DeleteForm, self).clean()
        path = data['path']
        signature = data['signature']
        generated_signature = hmac.new(str(settings.CMSCLOUD_SYNC_KEY), path, hashlib.sha1).hexdigest()
        if not constant_time_compare(signature, generated_signature):
            raise forms.ValidationError("Invalid signature")
        return data


class AddForm(DeleteForm):
    content = forms.FileField(required=True)

    def clean(self):
        data = super(DeleteForm, self).clean()
        path = data['path']
        signature_hmac = hmac.new(str(settings.CMSCLOUD_SYNC_KEY), path, hashlib.sha1)
        uploaded_file = data['content']
        for chunk in uploaded_file.chunks():
            signature_hmac.update(chunk)
        generated_signature = signature_hmac.hexdigest()
        signature = data['signature']
        if not constant_time_compare(signature, generated_signature):
            raise forms.ValidationError("Invalid signature")
        return data

