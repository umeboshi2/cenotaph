import os
from cornice.resource import resource, view
from datetime import datetime

#from bumblr.blogmanager import TumblrBlogManager
from bumblr.managers.blogs import BlogManager

from wibblr.views.base import BaseView

APIROOT = '/rest/v0'

rscroot = os.path.join(APIROOT, 'main')
dept_path = os.path.join(rscroot, 'department')
person_path = os.path.join(rscroot, 'person')
meeting_path = os.path.join(rscroot, 'meeting')
itemaction_path = os.path.join(rscroot, 'itemaction')
action_path = os.path.join(rscroot, 'action')

def convert_range_to_datetime(start, end):
    "start and end are timestamps"
    start = datetime.fromtimestamp(float(start))
    end = datetime.fromtimestamp(float(end))
    return start, end
    



# json view for calendar
class MainCalendarViewer(BaseView):
    def __init__(self, request):
        super(MainCalendarViewer, self).__init__(request)
        self.mgr = BlogManager(self.request.db)
        caltype = self.request.matchdict['caltype']
        if caltype == 'blogs':
            self.get_ranged_blogs()
        elif caltype == 'posts':
            self.get_ranged_posts()
            
    def _get_start_end_from_request(self):
        start = self.request.GET['start']
        #year, month, day = [int(p) for p in start.split('-')]
        #start = datetime(year, month, day)
        end = self.request.GET['end']
        #year, month, day = [int(p) for p in end.split('-')]
        #end = datetime(year, month, day)
        return convert_range_to_datetime(start, end)

    # json responses should not be lists
    # this method is for the fullcalendar
    # widget. Fullcalendar v2 uses yyyy-mm-dd
    # for start and end parameters, rather than
    # timestamps.
    def get_ranged_blogs(self):
        start, end = self._get_start_end_from_request()
        blogs = self.mgr.get_ranged_blogs(start, end,
                                          timestamps=False)
        blist = list()
        for b in blogs:
            bdata = b.serialize()
            bdata['title'] = b.info.name
            bdata['start'] = datetime.isoformat(b.updated_remote)
            bdata['allDay'] = False
            bdata['url'] = '#wibblr/viewblogposts/%s' % b.info.name
            blist.append(bdata)
        headers = [('Access-Control-Allow-Origin', '*')]
        self.request.response.headerlist.extend(headers) 
        self.response = blist
        
    def get_ranged_posts(self):
        start = self.request.GET['start']
        end = self.request.GET['end']
        posts = self.mgr.posts.get_ranged_posts(start, end)
        blist = list()
        for p in posts:
            bdata = p.serialize()
            bdata['title'] = p.blog_name
            bdata['start'] = p.timestamp
            bdata['allDay'] = False
            blist.append(bdata)
        headers = [('Access-Control-Allow-Origin', '*')]
        self.request.response.headerlist.extend(headers) 
        self.response = blist
        
