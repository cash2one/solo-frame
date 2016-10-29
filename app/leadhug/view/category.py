# coding:utf-8
from yajl import loads
from _route import route
from app.leadhug.view._base import JsonLoginView, LoginView
from app.leadhug.model.category import Category
from app.leadhug.model.offers import Offers

from solo.lib.jsob import JsOb


@route('/category/create')
class CreateCategory(LoginView):

    def get(self):
        self.render(err=False)

    def post(self):
        name = self.get_argument('name')
        if not name:
            self.render(err=u'Category Name can\'t be empty!')
        elif Category.count(dict(name=name, status={'$ne': '0'})):
            self.render(err=u'Name already be used!')
        else:
            status = self.get_argument('status')
            Category._save(name=name, status=status)
            self.redirect("/category/manage")


@route('/category/delete/(\d+)')
class DeleteCategory(LoginView):

    def get(self, cat_id):
        cat = Category.find_one(dict(_id=int(cat_id)))
        cat.deleted = True
        cat.save()
        self.redirect("/category/manage")


@route('/category/modify/(\d+)')
class ModifyCategory(LoginView):

    def get(self, cat_id):
        category = Category.find_one(dict(_id=int(cat_id)))
        self.render(
            category=category,
        )

    def post(self, cat_id):
        err = False
        content = loads(self.request.body)
        name = content.get('name')
        status = content.get('status')
        category = Category.find_one(dict(_id=int(cat_id)))
        if not name:
            err = u'Category Name can\'t be empty!'
        elif name != category.name and Category.count(dict(name=name, status={'$ne': '0'})):
            err = u'Name already be used!'
        else:
            Category._update(cat_id, name=name, status=status)

        self.finish(dict(err=err))


# @route('/category/manage')
# class ManageCategory(LoginView):

#     def get(self):
#         status = self.get_argument('status', '')
#         cats = Category.find(dict(status={"$ne": '0'} if not status or status == '0' else status))
#         for cat in cats:
#             cat['offer_count'] = Offers.count(dict(category=str(cat._id)))
#             cat.status = 'Active' if cat.status == '1' else 'Pending'

#         if not status and status != '0':
#             self.render(
#                 cat=cats
#             )
#         else:
#             self.finish(dict(cat=cats))

@route('/category/manage')
class ManageCategory(LoginView):

    def get(self):
        # status = self.get_argument('status', '')
        # limit = self.get_argument('limit','100')
        # cats = Category.find(dict(status={"$ne": '0'} if not status or status == '0' else status),skip=0,limit=limit)
        # for cat in cats:
        #     cat['offer_count'] = Offers.count(dict(category=str(cat._id)))
        #     cat.status = 'Active' if cat.status == '1' else 'Pending'

        # cats_count = cats.count()
        # if not status and status != '0':
        self.render(cat={})
        
        # else:
        #self.finish(dict(cat={}))

    def post(self):
        content = loads(self.request.body)
        status = content.get("status","")
        limit = int(content.get("limit"))
        page = int(content.get("page"))
        skip = (page - 1) * limit
           
        cats = Category.find(dict(status={"$ne": '0'} if not status or status == '0' else status),
                                    skip = skip,limit = limit)
        cat_count = Category.count(dict(status={"$ne": '0'} if not status or status == '0' else status),
                                    skip = skip,limit = limit)
        for cat in cats:
            cat['offer_count'] = Offers.count(dict(category=str(cat._id)))
            cat.status = 'Active' if cat.status == '1' else 'Pending'   
        self.finish(dict(cat=cats,cat_count=cat_count))



