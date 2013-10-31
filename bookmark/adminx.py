import xadmin
from xadmin import views
from models import *
from xadmin.layout import *

from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction

from bookmark.models import Bookmark, List, Feedback
from eventlog.models import Log

xadmin.site.register(Bookmark)
xadmin.site.register(List)
xadmin.site.register(Log)
xadmin.site.register(Feedback)