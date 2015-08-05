#!/bin/bash
# unfortunatly deleting orphaned plugins fails for plugins of Addons that are no longer installed.
# and that can happen quickly if you uninstall an Addon. We need to implement a cleaner uninstall
# first.
#echo "cms: deleting orphaned plugins"
#python manage.py cms delete_orphaned_plugins --noinput
echo "cms: fixing mptt-tree"
python manage.py cms fix-mptt --noinput
