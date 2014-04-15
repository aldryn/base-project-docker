# -*- coding: utf-8 -*-
import fcntl
import hashlib
import hmac
import os
import tarfile

from django.core.files.temp import NamedTemporaryFile
from django.utils.crypto import constant_time_compare
from itsdangerous import URLSafeTimedSerializer
import requests


SYNC_ALREADY_PERFORMED_FILEPATH = os.path.join(
    os.path.dirname(__file__), '.already_performed_initial_sync')
CHUNK_SIZE = 64 * 1024  # 64KB


def sync_changed_files(sync_key, last_commit_hash, sync_url, project_dir):
    if not os.path.exists(SYNC_ALREADY_PERFORMED_FILEPATH):
        lock_file = open(SYNC_ALREADY_PERFORMED_FILEPATH, 'w')
        fd = lock_file.fileno()
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError as e:
            print "other process is already running the sync:\n%s" % repr(e)
        else:
            lock_file.write(last_commit_hash)
            temp_file = NamedTemporaryFile(prefix='sync_changed_files', suffix='.tar.gz')
            signer = URLSafeTimedSerializer(sync_key)
            signed_data = signer.dumps(last_commit_hash)
            data = {'last_commit_hash': signed_data}
            response = requests.post(sync_url, data=data, stream=True)
            if response.ok:
                data_signature = hmac.new(key=str(sync_key), digestmod=hashlib.sha1)
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    data_signature.update(chunk)
                    temp_file.write(chunk)
                temp_file.seek(0)
                data_signature = data_signature.hexdigest()
                header_signature = response.headers.get('aldryn-sync-signature')
                if not constant_time_compare(header_signature, data_signature):
                    # TODO log failed attempt to corrupt the website's data
                    raise RuntimeError(
                        'Sync signatures does not match:\ndata:\t%s\nheader:\t%s' %
                        (data_signature, header_signature))
                tarball = tarfile.open(mode='r:gz', fileobj=temp_file)
                for member in tarball.getmembers():
                    path = member.name
                    if path.startswith(('static/', 'templates/')):
                        full_path = os.path.join(project_dir, path)
                        directory = os.path.dirname(full_path)
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        tarball.extract(member, project_dir)
                tarball.close()
            else:
                response.raise_for_status()
        finally:
            lock_file.close()
            temp_file.close()
