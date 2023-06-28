from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        #1.排除不需要登陆就能访问的页面
        if request.path_info in ['/login/', '/image/code/']:
            return

        #2.读取当前访问的用户的session信息，如果能读到，说明已登陆过，就可以继续向后走
        info_dict = request.session.get('info')
        if info_dict:
            return

        #2.没有登陆过，重新回到登陆页面
        return redirect('/login/')
