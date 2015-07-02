import urlparse
import urllib


urlparse.uses_netloc.append('s3')
urlparse.uses_netloc.append('djfs')

SCHEMES = {
    's3': 'aldrynstorage.S3MediaStorage',
    'djfs': 'fs.django_storage.DjeeseFSStorage',
}


def parse_storage_url(url):
    config = {}
    url = urlparse.urlparse(url)

    scheme = url.scheme.split('+', 1)

    config['DEFAULT_FILE_STORAGE'] = SCHEMES[scheme[0]]

    if scheme[0] == 's3':
        config.update({
            'AWS_MEDIA_ACCESS_KEY_ID': urllib.unquote(url.username or ''),
            'AWS_MEDIA_SECRET_ACCESS_KEY': urllib.unquote(url.password or ''),
            # Ignore the .s3.amazonaws.com part
            'AWS_MEDIA_STORAGE_BUCKET_NAME': url.hostname.split('.', 1)[0],
            'AWS_MEDIA_BUCKET_PREFIX': url.path.lstrip('/'),
        })
    elif scheme[0] == 'djfs':
        hostname = ('{}:{}'.format(url.hostname, url.port)
                    if url.port else url.hostname)
        config.update({
            'DJEESE_STORAGE_ID': url.username or '',
            'DJEESE_STORAGE_KEY': url.password or '',
            'DJEESE_STORAGE_HOST': urlparse.urlunparse((
                scheme[1],
                hostname,
                url.path,
                url.params,
                url.query,
                url.fragment,
            )),
        })

    return config
