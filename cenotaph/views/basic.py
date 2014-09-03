import os
from cornice.resource import resource, view

#from bumblr.blogmanager import TumblrBlogManager
#from bumblr.postmanager import TumblrPostManager
from bumblr.managers.posts import PostManager
from bumblr.managers.blogs import BlogManager

from cenotaph.views.base import BaseManagementResource
from cenotaph.views.base import DBResource

APIROOT = '/rest/v0'

rscroot = os.path.join(APIROOT, 'basic')
blog_path  = os.path.join(rscroot, 'blog')
post_path = os.path.join(rscroot, 'post')
photo_path = os.path.join(rscroot, 'photo')

def _make_resource(rpath, ident='id'):
    path = os.path.join(rpath, '{%s}' % ident)
    return dict(collection_path=rpath, path=path, cors_origins=('*',))


@resource(**_make_resource(blog_path, ident='name'))
class BasicBlogResource(BaseManagementResource):
    mgrclass = BlogManager
    def serialize_object(self, obj):
        data = obj.serialize()
        data['info'] = obj.info.serialize()
        return data
        
    
    def get(self):
        name = self.request.matchdict['name']
        return self.serialize_object(self.mgr.get_by_name(name))
    
    
@resource(**_make_resource(post_path))
class BasicPostResource(BaseManagementResource):
    mgrclass = PostManager
    

collection_path = os.path.join(blog_path, '{name}', 'post')
blogpost_path = os.path.join(collection_path, '{post_id}')
@resource(collection_path=collection_path, path=blogpost_path,
          cors_origins=('*',))
class BlogPostResource(DBResource):
    def __init__(self, request):
        super(BlogPostResource, self).__init__(request)
        self.mgr = BlogManager(self.db)
        self.mgr.posts.photos.set_local_path('/images')
        self.limit = 20
        self.max_limit = 100

    def collection_query(self):
        pass
    
    def serialize_object(self, dbobj):
        data = dbobj.serialize()
        if hasattr(dbobj, 'photos'):
            data['photos'] = list()
            photos = dbobj.photos
            for p in photos:
                filename = os.path.join('/images', p.filename)
                data['photos'].append(dict(url=p.url, filename=filename))
        return data
                
        
    def collection_get(self):
        offset = 0
        limit = self.limit
        GET = self.request.GET
        if 'offset' in GET:
            offset = int(GET['offset'])
        if 'limit' in GET:
            limit = int(GET['limit'])
            if limit > self.max_limit:
                limit = self.max_limit
        blog_name = self.request.matchdict['name']
        blogpost_query = self.mgr.get_blog_posts_query(blog_name)
        total_count = blogpost_query.count()
        posts = self.mgr.get_blog_posts(blog_name, offset=offset, limit=limit)
        print "Blog %s has %d posts." % (blog_name, total_count)
        for post in posts:
            photos = self.mgr.get_post_photos_and_paths(post.id)
            photos = [u for u,s,p in photos]
            #photos = [dict(url=u.url, filename=u.filename) for u,s,p in photos]
            post.photos = photos
        #import pdb ; pdb.set_trace()
        objects = posts
        return dict(total_count=total_count,
                    data=[self.serialize_object(o) for o in objects])
    


