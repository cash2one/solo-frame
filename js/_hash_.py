import _env  # noqa
from solo.config import DEBUG, CDN, APP
from os.path import dirname, basename, join

__HASH__ = {
    "leadhug/leadhug/offers": 'pR-Rr8Ot81tWVhXt2XnPNg',  # leadhug_leadhug_offers
    "new_pingstart/tableExport": 's5MbHWu_PNYcHnZ9TouIwQ',  # new_pingstart_tableExport
    "leadhug/FileSaver": 'ECUFUhmqQfCteQ5ntJgL9w',  # leadhug_FileSaver
    "affiliateleadhug/highcharts": 'llLN6dckfGPkKYJoetHoqg',  # affiliateleadhug_highcharts
    "affiliateleadhug/extendPagination": 'zauC_FvWX-WmpNRpnuQpTA',  # affiliateleadhug_extendPagination
    "lib/avalon": 'z6MfMIaegadKREzWG_5xHg',  # lib_avalon
    "new_pingstart/respond.min": '4YanSPrbXeX_nY4e9qwkeA',  # new_pingstart_respond
    "affiliateleadhug/fm.selectator.jquery": 'I8wkVSmRZYS5LPO2xuRMxg',  # affiliateleadhug_fm_selectator
    "new_pingstart/highcharts": '77-6aIlu_8Xz4Q5eJHfqPA',  # new_pingstart_highcharts
    "leadhug/leadhug/_mail": '3Mu-C2k9qxRbaLLG6e0hQA',  # leadhug_leadhug__mail
    "affiliateleadhug/affliate_leadhug/postback": 'VCt2TR_dyLU-xcCL09KctA',  # affiliateleadhug_affliate_leadhug_postback
    "new_pingstart/extendPagination": 'zauC_FvWX-WmpNRpnuQpTA',  # new_pingstart_extendPagination
    "new_pingstart/pingstart/pingstart": 'mjmpWR-RtPV4UtkiSOSLOw',  # new_pingstart_pingstart_pingstart
    "leadhug/jq-ext": 'Zm07LVP6wHI6FT6_3zygfw',  # leadhug_jq_ext
    "affiliateleadhug/affliate_leadhug/report": 'apv9-7otp3XsWax0eSV1zA',  # affiliateleadhug_affliate_leadhug_report
    "new_pingstart/pingstart/network": '4vpWhUyfLB3Pj7IMjZxE9g',  # new_pingstart_pingstart_network
    "leadhug/avalon": 'z6MfMIaegadKREzWG_5xHg',  # leadhug_avalon
    "new_pingstart/pingstart/report": 'sWBxKpi_lxxMxVS4HPcpRg',  # new_pingstart_pingstart_report
    "leadhug/upload/jquery.ui.widget": 'Bvyp75X81mS1P9EGgblKXQ',  # leadhug_upload_jquery_ui
    "affiliateleadhug/Blob": '6-jYiO__oIROcCZP3wh5CQ',  # affiliateleadhug_Blob
    "affiliateleadhug/bootstrap-datetimepicker.min": 'TBEECiILeGMzyoanE--jiA',  # affiliateleadhug_bootstrap_datetimepicker
    "new_pingstart/bootstrap-datetimepicker.min": 'TBEECiILeGMzyoanE--jiA',  # new_pingstart_bootstrap_datetimepicker
    "leadhug/extendPagination": 'T--Td-rB1I_TMTpCyY3_ZQ',  # leadhug_extendPagination
    "leadhug/leadhug/category": '1rLBL9uBhn6bX_NKrkm06g',  # leadhug_leadhug_category
    "affiliateleadhug/jquery.min": 'SjVhJrlXPre9Hpp0lHN0EA',  # affiliateleadhug_jquery
    "affiliateleadhug/data": 'MTPqV5nWWm9TadYPJAbZhA',  # affiliateleadhug_data
    "leadhug/jquery-ui.min": 'yLS6AKrtMwU8otABSZW5EA',  # leadhug_jquery_ui
    "affiliateleadhug/exporting": 'luEkUSzqCORtkiJJ1msCdg',  # affiliateleadhug_exporting
    "affiliateleadhug/copy": 'zxsXLPIq-8BoE1D4WtJxxw',  # affiliateleadhug_copy
    "affiliateleadhug/affliate_leadhug/payments": 'gbz8ZOpdLDBeILtYjWfIdQ',  # affiliateleadhug_affliate_leadhug_payments
    "new_pingstart/pingstart/login": 'MucFgot9C-ec3IgenC3qNA',  # new_pingstart_pingstart_login
    "new_pingstart/Blob": '6-jYiO__oIROcCZP3wh5CQ',  # new_pingstart_Blob
    "leadhug/upload/jquery.fileupload": 'zmFAv3D0PELrMp1A5nAn4w',  # leadhug_upload_jquery
    "lib/jquery.fancybox": 'Qf2b_vkVkUEH9WxsV6wmjw',  # lib_jquery
    "soloanalysis/analysis/dashboard": 'I_F6Z2TuPKIdKEug7o3iZg',  # soloanalysis_analysis_dashboard
    "new_pingstart/bootstrap.min": 'S-zckQRiPokfu504u6Ab5A',  # new_pingstart_bootstrap
    "soloanalysis/Blob": '6-jYiO__oIROcCZP3wh5CQ',  # soloanalysis_Blob
    "new_pingstart/bootlint": 'yVwPShl2qTzBcvycRml2wQ',  # new_pingstart_bootlint
    "soloanalysis/moment.min": 'mrs5-3YjO8iApFHP1wdX3w',  # soloanalysis_moment
    "leadhug/upload/jquery.uploadfile.min": 'XjfHeOwGKUxxsUFLqTuErA',  # leadhug_upload_jquery_uploadfile
    "affiliateleadhug/affliate_leadhug/index.min": 'Wh8mztYap-X8ejGJ-ygF6Q',  # affiliateleadhug_affliate_leadhug_index
    "soloanalysis/jquery-1.12.1.min": 'idgab-q54pet-gTYFsbOdw',  # soloanalysis_jquery_1_12_1
    "leadhug/fm.selectator.jquery": 'I8wkVSmRZYS5LPO2xuRMxg',  # leadhug_fm_selectator
    "leadhug/moment.min": 'Z3hG_hHu_TMBTBq2un1uaA',  # leadhug_moment
    "leadhug/tableExport": 's5MbHWu_PNYcHnZ9TouIwQ',  # leadhug_tableExport
    "affiliateleadhug/clipboard.min": 'Mh0AsN35Y_y-D8h-9GE_uQ',  # affiliateleadhug_clipboard
    "leadhug/metisMenu.min": 'nVls2tam4lDO1GeF0ErfTg',  # leadhug_metisMenu
    "leadhug/jquery.tokeninput": 'Pd4qkT0a6HfJKRo1_sXriQ',  # leadhug_jquery
    "affiliateleadhug/jquery-1.12.1.min": 'idgab-q54pet-gTYFsbOdw',  # affiliateleadhug_jquery_1_12_1
    "soloanalysis/jq-ext": 'Z_G-oenyCa6-GAJjeQGtRA',  # soloanalysis_jq_ext
    "leadhug/leadhug/user": 'k7M_6MyOlHaBbWu6zhn0bg',  # leadhug_leadhug_user
    "leadhug/leadhug/advertiser": 'Z868bTNTRj1VoCtHKd-nrA',  # leadhug_leadhug_advertiser
    "soloanalysis/exporting": 'luEkUSzqCORtkiJJ1msCdg',  # soloanalysis_exporting
    "affiliateleadhug/html5shiv": 'DOjzVYkcJsKPBX4ZXpfc1Q',  # affiliateleadhug_html5shiv
    "leadhug/jqPaginator": '0CWAB2enRZvkKsUSjCa-Jg',  # leadhug_jqPaginator
    "affiliateleadhug/affliate_leadhug/export": 'SQ92GEzbxmmVAVFLQdiAEg',  # affiliateleadhug_affliate_leadhug_export
    "affiliateleadhug/jq-ext": 'Z_G-oenyCa6-GAJjeQGtRA',  # affiliateleadhug_jq_ext
    "affiliateleadhug/bootstrap.min": 'S-zckQRiPokfu504u6Ab5A',  # affiliateleadhug_bootstrap
    "leadhug/bootstrap.min": 'xbWy-hm9Zv8jIR2fhE4BMQ',  # leadhug_bootstrap
    "affiliateleadhug/index.min": 'Wh8mztYap-X8ejGJ-ygF6Q',  # affiliateleadhug_index
    "lib/jquery.1.12.0.min": 'n3xlyEyOjD4xeUXo_YmJmw',  # lib_jquery_1_12_0
    "leadhug/leadhug/ajaxform": 'rcdjaEwbZRh02Rsx9z7tzQ',  # leadhug_leadhug_ajaxform
    "new_pingstart/jquery.min": 'E8ClBVzKeyRjsvc3AZYLng',  # new_pingstart_jquery
    "affiliateleadhug/moment.min": 'mrs5-3YjO8iApFHP1wdX3w',  # affiliateleadhug_moment
    "leadhug/leadhug/offer_affiliate": 'WaGWxQlqqlRyDbDUX9AAFQ',  # leadhug_leadhug_offer_affiliate
    "affiliateleadhug/multiple-select": 'ajFx6qcidcML2Bm09aiNow',  # affiliateleadhug_multiple_select
    "new_pingstart/exporting": 'mVnbDr3jlHBasf6dqAyfSA',  # new_pingstart_exporting
    "new_pingstart/jquery.blockUI": 'BtO1izYKOCyvGb_Tpak6ug',  # new_pingstart_jquery
    "leadhug/toastr": 'gOnkqpQBPIBBWDh-h2vjsg',  # leadhug_toastr
    "leadhug/upload/jquery.iframe-transport": 'mCjCNWoMY71LgLOhwmmOGQ',  # leadhug_upload_jquery
    "affiliateleadhug/jquery.prompt": 'GAFn5k9UNFGlUb06Og4u5Q',  # affiliateleadhug_jquery
    "affiliateleadhug/affliate_leadhug/offer": 'A7YjV7BpTfSw4UtfFc3_Fw',  # affiliateleadhug_affliate_leadhug_offer
    "affiliateleadhug/jquery.blockUI": 'BtO1izYKOCyvGb_Tpak6ug',  # affiliateleadhug_jquery
    "lib/jq-ext": 'Zm07LVP6wHI6FT6_3zygfw',  # lib_jq_ext
    "new_pingstart/jq-ext": 'Zm07LVP6wHI6FT6_3zygfw',  # new_pingstart_jq_ext
    "leadhug/stupidtable.min": 'sbcXnVVWaxj5eVvWPcQHZw',  # leadhug_stupidtable
    "new_pingstart/date": 'cR-Mo7GBNWddYfA9tH0T2Q',  # new_pingstart_date
    "affiliateleadhug/affliate_leadhug/dashboard": 'B-c6r8FS1w2eGmyG46fEdA',  # affiliateleadhug_affliate_leadhug_dashboard
    "affiliateleadhug/affliate_leadhug/account": 'hUY8Js0qKEquWFM84sQWag',  # affiliateleadhug_affliate_leadhug_account
    "affiliateleadhug/jquery-ui.min": 'yLS6AKrtMwU8otABSZW5EA',  # affiliateleadhug_jquery_ui
    "new_pingstart/pingstart/forget_password": 'eNgHJNWMUKMZ0CGkHp2o_w',  # new_pingstart_pingstart_forget_password
    "affiliateleadhug/toastr": 'gOnkqpQBPIBBWDh-h2vjsg',  # affiliateleadhug_toastr
    "affiliateleadhug/jqPaginator": '0CWAB2enRZvkKsUSjCa-Jg',  # affiliateleadhug_jqPaginator
    "new_pingstart/pingstart/user": 'UnHu7qn6uzXhU4iJLW2cqg',  # new_pingstart_pingstart_user
    "soloanalysis/dateFormat": '1YcTZBqoaGVlYaYWcvD1tA',  # soloanalysis_dateFormat
    "soloanalysis/avalon": 'z6MfMIaegadKREzWG_5xHg',  # soloanalysis_avalon
    "leadhug/html5shiv": 'DOjzVYkcJsKPBX4ZXpfc1Q',  # leadhug_html5shiv
    "soloanalysis/bootstrap": 'gBUELQtKwSWGevWwlrF1zg',  # soloanalysis_bootstrap
    "leadhug/sb-admin-2": 'vd-vZTElK6XIyc7c8RBWjQ',  # leadhug_sb_admin_2
    "new_pingstart/FileSaver": 'ECUFUhmqQfCteQ5ntJgL9w',  # new_pingstart_FileSaver
    "soloanalysis/highcharts": 'llLN6dckfGPkKYJoetHoqg',  # soloanalysis_highcharts
    "leadhug/jquery.tablesorter": 'nUTiTFPoOhY7eKKotLUAuw',  # leadhug_jquery
    "leadhug/Blob": '6-jYiO__oIROcCZP3wh5CQ',  # leadhug_Blob
    "leadhug/jquery.min": 'SjVhJrlXPre9Hpp0lHN0EA',  # leadhug_jquery
    "new_pingstart/avalon": 'z6MfMIaegadKREzWG_5xHg',  # new_pingstart_avalon
    "new_pingstart/html5shiv.min": 'MEQjQXWskfSbA_-ZnFkrhQ',  # new_pingstart_html5shiv
    "leadhug/jquery.blockUI": 'BtO1izYKOCyvGb_Tpak6ug',  # leadhug_jquery
    "leadhug/index": 'TAbAJMxwIYBlFABl-3_e5A',  # leadhug_index
    "new_pingstart/pingstart/signup": 'bhCCi1CKxgilBeuAM3edYw',  # new_pingstart_pingstart_signup
    "soloanalysis/daterangepicker": 'YuG2fjpxnygU9j5dN3HnWA',  # soloanalysis_daterangepicker
    "soloanalysis/extendPagination": 'zauC_FvWX-WmpNRpnuQpTA',  # soloanalysis_extendPagination
    "affiliateleadhug/stupidtable.min": 'sbcXnVVWaxj5eVvWPcQHZw',  # affiliateleadhug_stupidtable
    "affiliateleadhug/jquery1.7": 'uNZNC8FCs_ZwzAYRsK68rg',  # affiliateleadhug_jquery1
    "leadhug/leadhug/affiliate": 'JnSk3kxsxo3tPPYdLeIIXw',  # leadhug_leadhug_affiliate
    "leadhug/leadhug/report": '0ylWQDEbYpc7oVX_Y1UB8g',  # leadhug_leadhug_report
    "new_pingstart/moment.min": 'GDOGhQR7uZiBXQ_OIlZl9A',  # new_pingstart_moment
    "leadhug/leadhug/invoice": '-esU79VznYZmkkq0HKDmSA',  # leadhug_leadhug_invoice
    "affiliateleadhug/tableExport": 's5MbHWu_PNYcHnZ9TouIwQ',  # affiliateleadhug_tableExport
    "new_pingstart/daterangepicker": 'YuG2fjpxnygU9j5dN3HnWA',  # new_pingstart_daterangepicker
    "affiliateleadhug/jquery.tablesorter": 'nUTiTFPoOhY7eKKotLUAuw',  # affiliateleadhug_jquery
    "affiliateleadhug/jquery.searchableSelect": 'wHcWf-iXTLxX6MMdqLrQ5A',  # affiliateleadhug_jquery
    "affiliateleadhug/edit": 'Nf_kPkb3gtl38obBYT1RTw',  # affiliateleadhug_edit
    "affiliateleadhug/affliate_leadhug/verification": 'NeD2qBYkjGxyvJYkoaBGyQ',  # affiliateleadhug_affliate_leadhug_verification
    "leadhug/pingstart": 'hdCd8owTeO6N3lqESd4jgA',  # leadhug_pingstart
    "affiliateleadhug/daterangepicker": 'YuG2fjpxnygU9j5dN3HnWA',  # affiliateleadhug_daterangepicker
    "leadhug/jquery-1.11.2.min": 'V5Dq1607onOXrt-j0mO4Zw',  # leadhug_jquery_1_11_2
    "leadhug/respond.min": 'r8GYSj0XEQRJ3JDPIt4MJw',  # leadhug_respond
    "affiliateleadhug/FileSaver": 'ECUFUhmqQfCteQ5ntJgL9w',  # affiliateleadhug_FileSaver
    "affiliateleadhug/avalon": 'z6MfMIaegadKREzWG_5xHg',  # affiliateleadhug_avalon
    "soloanalysis/line": '4B7f3bLeutjvNhEFhNGWiA',  # soloanalysis_line
    "new_pingstart/pingstart/slot": 'I3Z6g-L-ZUTV_b5gIAPzxA',  # new_pingstart_pingstart_slot
    "leadhug/leadhug/verification": 'NeD2qBYkjGxyvJYkoaBGyQ',  # leadhug_leadhug_verification
    "leadhug/bootstrap-datetimepicker.min": 'TBEECiILeGMzyoanE--jiA',  # leadhug_bootstrap_datetimepicker
}

__vars__ = vars()


def _():
    for file_name, hash in __HASH__.iteritems():

        if DEBUG:
            suffix = basename(dirname(__file__))
            value = "/%s/%s.%s" % (suffix, file_name, suffix)
        else:
            suffix = basename(dirname(__file__))
            value = "//%s/%s" % (CDN.HOST, join(CDN.PREFIX, APP, suffix, dirname(file_name), hash))

        name = file_name.replace('.', '_').replace('-', '_').replace('/', '_')

        __vars__[name] = value

_()

del __vars__["_"]
