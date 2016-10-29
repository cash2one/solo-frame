# -*- encoding:utf-8 -*-
from hmako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1470125371.744369
_enable_loop = True
_template_filename = '/home/jay/hgPro/solo-frame/html/new_pingstart/login/Login.html'
_template_uri = '/new_pingstart/login/Login.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        css = context.get('css', UNDEFINED)
        js = context.get('js', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<!--<meta name="viewport" content="width=device-width, initial-scale=1">-->\n<meta http-equiv="X-UA-Compatible" content="IE=edge">\n<title></title>\n<!--<link rel="icon" href=""/>-->\n<link href="')
        # SOURCE LINE 9
        __M_writer(filters.legacy_html_escape(str(css.new_pingstart_bootstrap_min)))
        __M_writer('" rel="stylesheet">\n<link href="')
        # SOURCE LINE 10
        __M_writer(filters.legacy_html_escape(str(css.new_pingstart_pingstart)))
        __M_writer('" rel="stylesheet">\n<!--<![endif]&ndash;&gt;-->\n</head>\n<body id="body_login">\n<!--begin:\xe5\xaf\xbc\xe8\x88\xaa\xe6\x9d\xa1-->\n<div id="nav-top" style="height: 60px">\n<div class="container" style="background: #1c5ea9;height:60px" ms-controller="login" >\n<img id="logo_pic" src="https://s3-us-west-2.amazonaws.com/adplatformstatis/pingstart/img/pingstart.com/_img/pingstart_logo.png" alt="">\n<span data-toggle="modal" data-target="#exampleModal" id="sign_in" style="margin-top: 6px;cursor: pointer">Welcome</span>\n<div class="modal" id="exampleModal" data-keyboard="false" data-backdrop="false">\n<div class="modal-dialog register">\n<div class="modal-content">\n<div class="modal-header" style="border-bottom: 0px;background:#4a5056">\n<h2 class="modal-title text-center" id="exampleModalLabel">sign in</h2>\n</div>\n<div class="register_body">\n<form role="form" autocomplete="on">\n<div class="email" id="email">\n<input type="email" placeholder="Email" ms-duplex="o[\'email\']" name="email" class="form-control">\n</div>\n<div class="password" id="password">\n<input type="password" placeholder="Password" ms-duplex="o[\'password\']" name="password" class="form-control">\n</div>\n<div class="captcha_code" id="captcha_code">\n<input id="red_border" type="text" placeholder="Captcha" ms-duplex="o[\'captcha_code\']" class="form-control">\n<div class="get_captcha_code" ms-click="get_captcha()" id="img_parent">\n<img id="code_img" ms-attr-src="captcha_img">\n</div>\n<input type="hidden" ms-duplex="o[\'captcha_key\']">\n</div>\n<div class="row">\n<div class="col-xs-12">\n<button type="button" id="btn_login" class="btn btn-block" ms-click="login">sign in</button>\n</div>\n</div>\n</form>\n</div>\n<div class="modal-footer register_footer" id="sign-text">\n<a id="btn_forget" href="javascript:" ms-click="forget_password">Forgot your password?</a>\n<a id="btn_reg" href="/signup">Sign up now</a>\n</div>\n</div>\n</div>\n</div>\n</div>\n</div>\n<!--begin:footer-->\n<div class="lg_ft" id="copy">\n<div class="container">\n<p>\n&copy;2016.PingStart.All rights reserved Contact Us;support @ pingstart.com\n</p>\n</div>\n</div>\n<!--end:\xe9\xa1\xb5\xe8\x84\x9a-->\n<script src="')
        # SOURCE LINE 67
        __M_writer(filters.legacy_html_escape(str(js.new_pingstart_jquery_min)))
        __M_writer('"></script>\n<script src="')
        # SOURCE LINE 68
        __M_writer(filters.legacy_html_escape(str(js.new_pingstart_bootstrap_min)))
        __M_writer('"></script>\n<script src="')
        # SOURCE LINE 69
        __M_writer(filters.legacy_html_escape(str(js.new_pingstart_avalon)))
        __M_writer('"></script>\n<script src="')
        # SOURCE LINE 70
        __M_writer(filters.legacy_html_escape(str(js.new_pingstart_html5shiv_min)))
        __M_writer('"></script>\n<script src="')
        # SOURCE LINE 71
        __M_writer(filters.legacy_html_escape(str(js.new_pingstart_respond_min)))
        __M_writer('"></script>\n<script src="')
        # SOURCE LINE 72
        __M_writer(filters.legacy_html_escape(str(js.new_pingstart_jq_ext)))
        __M_writer('"></script>\n<script src="')
        # SOURCE LINE 73
        __M_writer(filters.legacy_html_escape(str(js.new_pingstart_pingstart_login)))
        __M_writer('"></script>\n<script>\n$("#sign_in").click();\n</script>\n</body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


