import _env  # noqa
from solo.config import DEBUG, CDN, APP
from os.path import dirname, basename, join

__HASH__ = {
    "new_pingstart/pingstart": 'AFl8BafEK8CCMG5cYC6CSQ',  # new_pingstart_pingstart
    "new_pingstart/bootstrap-datetimepicker.min": 'nTWTKDeXJJGIEPwCBsL8SQ',  # new_pingstart_bootstrap_datetimepicker
    "affiliateleadhug/style": 'Jhu30gPnEoRkIJxLFzhDeA',  # affiliateleadhug_style
    "leadhug/metisMenu.min": 'uz9vhvP-uUsrp7Q8nTFcVA',  # leadhug_metisMenu
    "new_pingstart/daterangepicker": 'GIXnux1pJQ_I3ZWyVXxnVA',  # new_pingstart_daterangepicker
    "affiliateleadhug/multiple-select": 'J0s_0yR8-ha9KZ3qLQozcQ',  # affiliateleadhug_multiple_select
    "leadhug/bootstrap-datetimepicker.min": 'T-OCxabzhdXE7XaWfuYN_w',  # leadhug_bootstrap_datetimepicker
    "affiliateleadhug/jquery.prompt": 'QdzmH70A7dZSD0Qp44QoPg',  # affiliateleadhug_jquery
    "affiliateleadhug/jquery.searchableSelect": 'DXz4ZzUyH7d_33OeK1aMpg',  # affiliateleadhug_jquery
    "lib/fancybox/helpers/jquery.fancybox-thumbs": 'Ut3YSp9CwdTNhtUYp_fovA',  # lib_fancybox_helpers_jquery
    "affiliateleadhug/bootstrap.min": '9v_ZH2qwHopljJdav8ql3g',  # affiliateleadhug_bootstrap
    "lib/fancybox/jquery.fancybox": 'bFWVHOHjEVcR9j-Zt1AfOg',  # lib_fancybox_jquery
    "lib/fancybox/helpers/jquery.fancybox-buttons": 'ysdVOMLj3fre-Dn-rKjjVg',  # lib_fancybox_helpers_jquery
    "leadhug/fm.selectator.jquery": 'sPNMR5ZIPjffcFTJe1wQuw',  # leadhug_fm_selectator
    "new_pingstart/bootstrap.min": 'oWvLxH9wNKoLtO0PeA1raQ',  # new_pingstart_bootstrap
    "affiliateleadhug/bootstrap": 'w67TyYcC9tizM0OK-YXa5g',  # affiliateleadhug_bootstrap
    "leadhug/style": 'pduogwc0YEtci2fvwVobcg',  # leadhug_style
    "soloanalysis/index.min": 'cC7T52aV14Z-oF4YHMa0Yw',  # soloanalysis_index
    "leadhug/token-input": 'Bh_SUVGVUP-3WvJd-k2muw',  # leadhug_token_input
    "affiliateleadhug/index.min": 'cC7T52aV14Z-oF4YHMa0Yw',  # affiliateleadhug_index
    "lib/bootstrap": 'W6N62RY2Q8MiUTZnVPCLKg',  # lib_bootstrap
    "leadhug/sb-admin-2": '2PGY5uzQvtbnt1vsqj9hPw',  # leadhug_sb_admin_2
    "affiliateleadhug/daterangepicker": 'GIXnux1pJQ_I3ZWyVXxnVA',  # affiliateleadhug_daterangepicker
    "soloanalysis/jquery.searchableSelect": 'DXz4ZzUyH7d_33OeK1aMpg',  # soloanalysis_jquery
    "leadhug/timeline": 'fMrfmUHe4wx20AHMkBunlQ',  # leadhug_timeline
    "lib/bootstrap.min": 'XVNXyzcE4fQ6H1v-0q6_Qg',  # lib_bootstrap
    "soloanalysis/bootstrap.min": 'dmDSnzSbmHYPAl3oHvIqwg',  # soloanalysis_bootstrap
    "leadhug/jquery.fileupload": 'T6JqyTNuIq_tJ7F3R_5z3g',  # leadhug_jquery
    "leadhug/font-awesome.min": 'TFTI9Zm2O4wH-5XRtQ37ow',  # leadhug_font_awesome
    "leadhug/index.min": '26gKG3LC9-lXWZGsoG5mBA',  # leadhug_index
    "soloanalysis/daterangepicker": 'GIXnux1pJQ_I3ZWyVXxnVA',  # soloanalysis_daterangepicker
    "leadhug/bootstrap.min": 'cheO7Q6kgmZVbgjO5uBTXw',  # leadhug_bootstrap
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
