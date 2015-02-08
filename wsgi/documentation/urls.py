from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'documentation.views.index', name='documentation'),
    url(r'^gen$', 'documentation.views.generate', name='documentation'),
    url(r'^(?P<file>[a-z0-9._/-]*.html)$', 'documentation.views.renderHTML', name='documentation'),
    url(r'^(?P<file>[a-z0-9._/]*.css)$', 'documentation.views.renderCSS', name='documentation'),
    url(r'^(?P<file>[a-z0-9._/]*.js)$', 'documentation.views.renderJS', name='documentation'),
    url(r'^(?P<file>[a-z0-9._/]*.png)$', 'documentation.views.renderObj', name='documentation'),
    url(r'^(?P<file>[a-z0-9._/]*.gif)$', 'documentation.views.renderObj', name='documentation'),
)