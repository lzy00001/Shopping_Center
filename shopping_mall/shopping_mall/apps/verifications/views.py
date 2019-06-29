from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection

from rest_framework.views import APIView




# url('^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),
# 图片验证码逻辑不需要查询数据库,也不需要进行序列化操作，所以不需要使用序列化器，所以继承APIView最合适
from shopping_mall.libs.captcha.captcha import captcha
from verifications import constants


class ImageCodeView(APIView):
    """图片验证码"""
    def get(self, request, image_code_id):
        # 接受参数       （获取图片验证码）
        # 校验参数       （校验图片验证码）
        # 由于参数image_code_id在url路由中正则可以校验,所以不用考虑接受参数和校验参数

        # 生成图片验证码
        text, image = captcha.generate_captcha()

        # 保存图片验证码到redis中～文本格式
        # 1.连接redis
        redis_conn = get_redis_connection('verify_codes')
        # 2.保存图片验证码到redis中
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 返回图片验证码     （返回图片验证码获取成功响应）
        return HttpResponse(image, content_type="images/jpg")