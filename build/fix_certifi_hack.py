# Workaround for openssl<1.0.2 not supporting 2048bit certificates correctly
# (newest certifi packages only provide 2048bit certs by default)
# This is a nasty place to put this code, but other places did not work.
# e.g setting REQUESTS_CA_BUNDLE globally breaks pip install, since it also
# uses a vendored in version of requests under the hood.
import sys
import os


if 'REQUESTS_CA_BUNDLE' not in os.environ:
    try:
        import certifi
    except ImportError:
        # certifi not installed - no need to do any thing.
        # requests will use the outdated bundled certs.
        # Not ideal, but nothing we can do.
        pass
    else:
        import ssl
        from distutils.version import LooseVersion
        v_installed = ssl.OPENSSL_VERSION.split(" ")[1]
        v_2048bit_capable = '1.0.2'
        if LooseVersion(v_installed) < LooseVersion(v_2048bit_capable):
            # OpenSSL<1.0.2 can't handle 2048bit certs. Use the less secure,
            # but up-to-date and working 1024bit certs from certifi.
            os.environ['REQUESTS_CA_BUNDLE'] = certifi.old_where()
        else:
            # we have OpenSSL>=1.0.2, so using the default up-to-date 2048bit
            # certs will not be a problem.
            pass
