# -*- coding: utf-8 -*-

''' Adapted by 2013 Georges Toth <georges _at_ trypill _dot_ org>'''

"""Internationalization and Localization for CherryPy

**Tested with CherryPy 3.1.2**

This tool provides locales and loads translations based on the
HTTP-ACCEPT-LANGUAGE header. If no header is send or the given language
is not supported by the application, it falls back to
`tools.I18nTool.default`. Set `default` to the native language used in your
code for strings, so you must not provide a .mo file for it.

The tool uses `babel<http://babel.edgewall.org>`_ for localization and
handling translations. Within your Python code you can use four functions
defined in this module and the loaded locale provided as
`cherrypy.response.i18n.locale`.

Example::

    from i18ntool import ugettext as _, ungettext

    class MyController(object):
        @cherrypy.expose
        def index(self):
            loc = cherrypy.response.i18n.locale
            s1 = _(u'Translateable string')
            s2 = ungettext(u'There is one string.',
                           u'There are more strings.', 2)
            return u'<br />'.join([s1, s2, loc.display_name])

If you have code (e.g. database models) that is executed before the response
object is available, use the *_lazy functions to mark the strings
translateable. They will be translated later on, when the text is used (and
hopefully the response object is available then).

Example::

    from i18ntool import ugettext_lazy

    class Model:
        def __init__(self):
            name = ugettext_lazy(u'Name of the model')

For your templates read the documentation of your template engine how to
integrate babel with it. I think `Genshi<http://genshi.edgewall.org>`_ and
`Jinja 2<http://jinja.pocoo.org`_ support it out of the box.


Settings for the CherryPy configuration::

    [/]
    tools.I18nTool.on = True
    tools.I18nTool.default = Your language with territory (e.g. 'en_US')
    tools.I18nTool.mo_dir = Directory holding the locale directories
    tools.I18nTool.domain = Your gettext domain (e.g. application name)

The mo_dir must contain subdirectories named with the language prefix
for all translations, containing a LC_MESSAGES dir with the compiled
catalog file in it.

Example::

    [/]
    tools.I18nTool.on = True
    tools.I18nTool.default = 'en_US'
    tools.I18nTool.mo_dir = '/home/user/web/myapp/i18n'
    tools.I18nTool.domain = 'myapp'

    Now the tool will look for a file called myapp.mo in
    /home/user/web/myapp/i18n/en/LC_MESSACES/
    or generic: <mo_dir>/<language>/LC_MESSAGES/<domain>.mo

That's it.

:License: BSD
:Author: Thorsten Weimann <thorsten.weimann (at) gmx (dot) net>
:Date: 2010-02-08
"""

import os
import cherrypy
from babel.core import Locale, UnknownLocaleError
from babel.support import Translations, LazyProxy

try:
    # Python 2.6 and above
    from collections import namedtuple
    Lang = namedtuple('Lang', 'locale trans')
except ImportError:
    # Python 2.5
    class Lang(object):
        def __init__(self, locale, trans):
            self.locale = locale
            self.trans = trans


# Cache for Translations and Locale objects
_languages = {}


# Exception
class ImproperlyConfigured(Exception):
    """Raised if no known locale were found."""


# Public translation functions
def ugettext(message):
    """Standard translation function. You can use it in all your exposed
    methods and everywhere where the response object is available.

    :parameters:
        message : Unicode
            The message to translate.

    :returns: The translated message.
    :rtype: Unicode
    """
    return cherrypy.response.i18n.trans.ugettext(message)


def ugettext_lazy(message):
    """Like ugettext, but lazy.

    :returns: A proxy for the translation object.
    :rtype: LazyProxy
    """
    def get_translation():
        return cherrypy.response.i18n.trans.ugettext(message)
    return LazyProxy(get_translation)


def ungettext(singular, plural, num):
    """Like ugettext, but considers plural forms.

    :parameters:
        singular : Unicode
            The message to translate in singular form.
        plural : Unicode
            The message to translate in plural form.
        num : Integer
            Number to apply the plural formula on. If num is 1 or no
            translation is found, singular is returned.

    :returns: The translated message as singular or plural.
    :rtype: Unicode
    """
    return cherrypy.response.i18n.trans.ungettext(singular, plural, num)


def ungettext_lazy(singular, plural, num):
    """Like ungettext, but lazy.

    :returns: A proxy for the translation object.
    :rtype: LazyProxy
    """
    def get_translation():
        return cherrypy.response.i18n.trans.ungettext(singular, plural, num)
    return LazyProxy(get_translation)


def set_header_language():
    """Sets the Content-Language response header (if not already set) to the
    language of `cherrypy.response.i18n.locale`.
    """
    if 'Content-Language' not in cherrypy.response.headers and hasattr(cherrypy.response, 'i18n'):
            cherrypy.response.headers['Content-Language'] = str(
                cherrypy.response.i18n.locale)


class I18nTool(cherrypy.Tool):
    """Tool to integrate babel translations in CherryPy."""

    def __init__(self, root_path):
        self._name = 'I18nTool'
        self._point = 'before_handler'
        self._root_path = root_path
        # Make sure, session tool (priority 50) is loaded before
        self._priority = 100

    def _setup(self):
        #c = cherrypy.request.config
        #if c.get('tools.staticdir.on', False) or \
        #   c.get('tools.staticfile.on', False):
        #    return
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('before_finalize', set_header_language)

    def callable(self, **kw):
        """Main function which will be invoked during the request by `I18nTool`.
        If the SessionTool is on and has a lang key, this language get the
        highest priority. Default language get the lowest priority.
        The `Lang` object will be saved as `cherrypy.response.i18n` and the
        language string will also saved as `cherrypy.session['_lang_']` (if
        SessionTool is on).

        :parameters:
            mo_dir : String
                `to ols.I18nTool.mo_dir`
            default : String
                `tools.I18nTool.default`
            domain : String
                `tools.I18nTool.domain`
        """
        mo_dir = kw.get('mo_dir', None)
        default = kw.get('default', None)
        domain = kw.get('domain', None)

        langs = [x.value.replace('-', '_') for x in
                 cherrypy.request.headers.elements('Accept-Language')]
        sessions_on = cherrypy.request.config.get('tools.sessions.on', False)
        if sessions_on and cherrypy.session.get('language', ''):
            langs.insert(0, cherrypy.session.get('language', '__'))
        langs.append(default)

        loc = self.load_translation(langs, mo_dir, domain)
        cherrypy.response.i18n = loc
        if sessions_on:
            cherrypy.session['_lang_'] = str(loc.locale)

    def load_translation(self, langs, dirname, domain):
        """Loads the first existing translations for known locale and saves the
        `Lang` object in a global cache for faster lookup on the next request.

        :parameters:
            langs : List
                List of languages as returned by `parse_accept_language_header`.
            dirname : String
                Directory of the translations (`tools.I18nTool.mo_dir`).
            domain : String
                Gettext domain of the catalog (`tools.I18nTool.domain`).

        :returns: Lang object with two attributes (Lang.trans = the translations
                  object, Lang.locale = the corresponding Locale object).
        :rtype: Lang
        :raises: ImproperlyConfigured if no locale where known.
        """
        locale = None
        for lang in langs:
            short = lang[:2].lower()
            try:
                locale = Locale.parse(lang)
                if (domain, short) in _languages:
                    return _languages[(domain, short)]
                trans = Translations.load(dirname, short, domain)
            except (ValueError, UnknownLocaleError) as e:
                print e
                continue
            # If the translation was found, exit loop
            if isinstance(trans, Translations):
                break
        if locale is None:
            raise ImproperlyConfigured('Default locale not known.')
        _languages[(domain, short)] = res = Lang(locale, trans)
        return res

    def set_custom_language(self, language):
        config = cherrypy.request.config
        langs = [language, cherrypy.request.config.get('tools.I18nTool.default', '')]
        mo_dir = os.path.join(self._root_path, cherrypy.request.config.get('tools.I18nTool.mo_dir', ''))
        mo_dir = cherrypy.request.config.get('tools.I18nTool.mo_dir', '')
        domain = cherrypy.request.config.get('tools.I18nTool.domain', '')
        cherrypy.response.i18n = self.load_translation(langs, mo_dir, domain)
