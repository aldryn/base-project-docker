# -*- coding: utf-8 -*-
from copy import deepcopy
import os
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.db.transaction import commit_on_success
from django.db.utils import DatabaseError
from django.utils.translation import activate
from optparse import make_option
from south.management.commands.migrate import Command as Migrate
from south.management.commands.syncdb import Command as SyncDB
from south.models import MigrationHistory
import requests
from cmscloud.serialize import Loader


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--key', action='store', dest='key'),
    ) 
    def handle_noargs(self, **options):
        key = options.pop('key', '')
        syncdb_opts = deepcopy(options)
        syncdb_opts['migrate_all'] = False
        syncdb_opts['interactive'] = False
        syncdb_opts['migrate'] = False
        migrate_opts = deepcopy(options)
        migrate_opts['fake'] = False
        migrate_opts['interactive'] = False
        self.stdout.write("Detecting database status\n")
        try:
            with commit_on_success():
                MigrationHistory.objects.count()
        except DatabaseError:
            self.stdout.write("No database yet, running full syncdb\n")
            syncdb_opts['migrate_all'] = True
            migrate_opts['fake'] = True
        syncdb = SyncDB()
        syncdb.stdout = self.stdout
        syncdb.stderr = self.stderr
        syncdb.handle_noargs(**syncdb_opts)
        migrate = Migrate()
        migrate.stdout = self.stdout
        migrate.stderr = self.stderr
        migrate.handle(**migrate_opts)
        datayaml = os.path.join(settings.PROJECT_DIR, 'data.yaml')
        if os.path.exists(datayaml):
            activate(settings.CMS_LANGUAGES[0][0])
            os.chdir(settings.PROJECT_DIR)
            loader = Loader()
            loader.load(datayaml)
        if key:
            requests.post('https://control.djeese.com/api/internal/v1/heroku-sync-command/', data={'key': key})
