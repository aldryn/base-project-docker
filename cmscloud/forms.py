# -*- coding: utf-8 -*-
import hashlib
import hmac
from django import forms
from django.conf import settings
from django.utils.crypto import constant_time_compare


class DeleteForm(forms.Form):
    signature = forms.CharField(required=True)
    path = forms.CharField(required=True)

    def clean(self):
        data = super(DeleteForm, self).clean()
        path = data.get('path')
        signature = data.get('signature')
        generated_signature = hmac.new(
            str(settings.CMSCLOUD_SYNC_KEY), path, hashlib.sha1).hexdigest()
        if not constant_time_compare(signature, generated_signature):
            raise forms.ValidationError("Invalid signature")
        return data


class AddForm(DeleteForm):
    content = forms.FileField(required=True, allow_empty_file=True)

    def clean(self):
        data = super(DeleteForm, self).clean()
        path = data.get('path')
        uploaded_file = data.get('content')
        signature = data.get('signature')
        if path and uploaded_file and signature:  # otherwise there were some errors
            signature_hmac = hmac.new(
                str(settings.CMSCLOUD_SYNC_KEY), path, hashlib.sha1)
            for chunk in uploaded_file.chunks():
                signature_hmac.update(chunk)
            generated_signature = signature_hmac.hexdigest()
            if not constant_time_compare(signature, generated_signature):
                raise forms.ValidationError("Invalid signature")
        return data


class RunCommandForm(forms.Form):
    signature = forms.CharField(required=True)
    command = forms.CharField(required=True)

    def clean(self):
        data = super(RunCommandForm, self).clean()
        command = data.get('command')
        signature = data.get('signature')
        generated_signature = hmac.new(
            str(settings.CMSCLOUD_SYNC_KEY), command, hashlib.sha1).hexdigest()
        if not constant_time_compare(signature, generated_signature):
            raise forms.ValidationError("Invalid signature")
        return data
