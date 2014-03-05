# -*- coding: utf-8 -*-
"""
Access Control Middleware
"""
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect


CONTENT = """<!DOCTYPE html>
<!--[if lt IE 7 ]> <html lang="en" class="no-js ie6"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie7"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie8"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!-->
<html lang="en" class="no-js">
<!--<![endif]-->
<head>
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <title>Your site is ready</title>
  <link rel="shortcut icon" href="https://static.aldryn.com/favicon.ico">
  <link rel="apple-touch-icon" href="https://static.aldryn.com/apple-touch-icon.png">
  <link rel="stylesheet" href="https://static.aldryn.com/stylesheets/style.css?v=2"><!--[if lte IE 9]>
  <link rel="stylesheet" href="https://static.aldryn.com/stylesheets/ie.css" type="text/css" media="screen" />
  <![endif]--><!--[if lt IE 8]>
  <script src='https://static.aldryn.com/javascripts/libs/modernizr.min.js'></script>
  <script src="http://ie7-js.googlecode.com/svn/version/2.1(beta4)/IE9.js"></script>
  <![endif]-->
</head>
<body>
  <div id="reg-bg"></div>
  <div id="login" class="window center">
    <section>
      <div id="logo">
        <a href="http://www.django-cms.org" class="logo dark">django-cms.org</a>
      </div>
      <div class="register-icon success-icon"></div>
      <h3>Your site is ready</h3>
      <p>Just click on the login button to access it:</p>
      <p style="margin-top:20px"><a class="button blue" href="/login/">Login</a></p>
    </section>
    <section class="inverted">
      <h4>Get your free account today! <a href="/register/">Sign up</a></h4>
    </section>
  </div>
  <script type="text/javascript">
        var _gaq = _gaq || [];
        _gaq.push(['_setAccount', 'UA-26813318-4']);
        _gaq.push(['_trackPageview']);
        (function() {
          var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
          ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
          var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
        })();
  </script> <!-- SnapEngage -->
  <script type="text/javascript">
    document.write(unescape("%3Cscript src='" + ((document.location.protocol=="https:")?"https://www.snapengage.com":"http://www.snapengage.com") + "/snapabug.js' type='text/javascript'%3E%3C/script%3E"));
  </script>
  <script type="text/javascript">
    SnapABug.setButton("https://static.aldryn.com/images/snapengage_help.png");
    SnapABug.addButton("568d7304-737a-41d8-9a29-eec2e8bcb699","1","50%");
  </script> <!--[if lt IE 9 ]>
                <script src="//ajax.googleapis.com/ajax/libs/chrome-frame/1.0.2/CFInstall.min.js"></script>
                <script>window.attachEvent("onload",function(){CFInstall.check({mode:"overlay"})})</script>
        <![endif]-->
</body>
</html>
"""


class AccessControlMiddleware(object):
    def process_request(self, request):
        if (request.user.is_authenticated() or
                request.path.startswith(('/login/', '/admin/~cmscloud-api/'))):
            return None

        token = request.GET.get(settings.SHARING_VIEW_ONLY_TOKEN_KEY_NAME, None)
        if settings.SHARING_VIEW_ONLY_SECRET_TOKEN == token:
            request.session[settings.SHARING_VIEW_ONLY_TOKEN_KEY_NAME] = token
            return HttpResponseRedirect('/')

        demo_access_token = request.GET.get(settings.DEMO_ACCESS_TOKEN_KEY_NAME, None)
        if settings.DEMO_ACCESS_SECRET_STRING == demo_access_token:
            request.session[settings.DEMO_ACCESS_TOKEN_KEY_NAME] = demo_access_token
            try:
                user = User.objects.get(username='aldryn demo')
            except User.DoesNotExist:
                user = User(username='aldryn demo', is_staff=True)
                user.save()
            user.backend = "%s.%s" % (ModelBackend.__module__, ModelBackend.__name__)
            login(request, user)
            return HttpResponseRedirect('/')

        return HttpResponse(CONTENT)


# copied from django 1.7a2: https://github.com/django/django/blob/1.7a2/django/contrib/sites/middleware.py
from django.contrib.sites.models import Site


class CurrentSiteMiddleware(object):
    """
    Middleware that sets `site` attribute to request object.
    """

    def process_request(self, request):
        request.site = Site.objects.get_current()
