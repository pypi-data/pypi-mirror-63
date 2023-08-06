import gettext
import locale
import os

from . import package_dir

__all__ = ['_', 'translate']

loc = locale.getdefaultlocale()
lan = loc[0]
locale_dir = os.path.join(package_dir, '../locale')

if gettext.find('asaloader', localedir=locale_dir, languages=[lan]):
    translate = gettext.translation('asaloader', localedir=locale_dir, languages=[lan])
    _ = translate.gettext
else:
    translate = None
    _ = lambda s: s
