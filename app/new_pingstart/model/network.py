# coding=utf-8
from __future__ import division
from collections import OrderedDict
from decimal import Decimal
import _env  # noqa
from solo.web.mongo import Doc
from app.web.model.gid import gid
from app.new_pingstart.model import GidKey


class NetWork(Doc):

    structure = dict(
        _id=int,
        user_id=int,
        name=str,
        sdk=[{
            'platform': str,
            'doc_link': str,
            'sdk_link': str
        }],
        adapter=str,
        adapter_model=dict(
                Banner=str,
                Interstitial=str,
                Native=str
            ),
        auth_manager=str,
        login_auth_args=list,
        args=list,
        deleted=bool,
    )

    default_values = {
        'deleted': False
    }

    @classmethod
    def pingstart(cls, user_id):
        return cls.find_one(dict(name='PingStart', user_id=int(user_id)))

    @classmethod
    def create(cls,user_id, name=None, sdk=None, auth_manager=None, adapter=None, args=None):
        network = NetWork(dict(
            _id=int(gid(GidKey.network_key)),
            user_id=int(user_id),
            name=name,
            sdk=sdk or [],
            adapter=adapter or [],
            args=args or [],
            auth_manager=auth_manager or ''
        ), True).save()
        return network

    @classmethod
    def _init(cls, user_id):
        init_networks = [
            dict(
                _id=int(gid(GidKey.network_key)),
                user_id=int(user_id),
                name='PingStart',
                sdk=[
                    dict(
                        platform='Android',
                        doc_link='',
                        sdk_link=''
                    )
                ],
                adapter='https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER',
                adapter_model=dict(
                    Banner='com.pingstart.adsdk.adapter.AdBanner',
                    Interstitial='com.pingstart.adsdk.adapter.AdInterstitial',
                    Native='com.pingstart.adsdk.adapter.AdNative'
                ),
                args=['publisher_id', 'slot_id'],
                login_auth_args=[],
                auth_manager='',
                deleted=False
            ),
            dict(
                _id=int(gid(GidKey.network_key)),
                user_id=int(user_id),
                name='Vungle',
                sdk=[
                    dict(
                        platform='Android',
                        doc_link='https://support.vungle.com/hc/zh-cn/articles/204463100-Advanced-Settings-for-Vungle-Android-SDK',
                        sdk_link='https://v.vungle.com/sdk'
                    )
                ],
                adapter='https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER',
                adapter_model=dict(
                    Banner='',
                    Interstitial='com.pingstart.mobileads.VungleInterstitial',
                    Native=''
                ),
                args=['app_id'],
                login_auth_args=['API_ID', 'API_KEY'],
                auth_manager='',
                deleted=False
            ),
            dict(
                _id=int(gid(GidKey.network_key)),
                user_id=int(user_id),
                name='AdColony',
                sdk=[
                    dict(
                        platform='Android',
                        doc_link='https://adcolony-www-common.s3.amazonaws.com/pub-adapter/android/AdColonyAdapterIntegrationGuide.pdf',
                        sdk_link='https://github.com/AdColony/'
                    )
                ],
                adapter='https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER',
                adapter_model=dict(
                    Banner='',
                    Interstitial='com.pingstart.mobileads.AdColonyInterstitial',
                    Native=''
                ),
                args=['app_id', 'zone_id', 'client_options', 'all_zone_ids'],
                login_auth_args=['API_KEY', 'User', 'Password'],
                auth_manager='',
                deleted=False
            ),
            dict(
                _id=int(gid(GidKey.network_key)),
                user_id=int(user_id),
                name='AdMob',
                sdk=[
                    dict(
                        platform='Android',
                        doc_link='https://developers.google.com/admob/android/interstitial?hl=en#helpful_resources',
                        sdk_link='https://developers.google.com/admob/android/download'
                    )
                ],
                adapter='https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER',
                adapter_model=dict(
                    Banner='com.pingstart.mobileads.AdMobBanner',
                    Interstitial='com.pingstart.mobileads.AdMobInterstitial',
                    Native='com.pingstart.mobileads.AdMobNative'
                ),
                args=['ad_unit_id'],
                login_auth_args=['Json_Token'],
                auth_manager='',
                deleted=False
            ),
            dict(
                _id=int(gid(GidKey.network_key)),
                user_id=int(user_id),
                name='Facebook Audience Network',
                sdk=[
                    dict(
                        platform='Android',
                        doc_link='https://developers.facebook.com/docs/audience-network/android/interstitial',
                        sdk_link='https://developers.facebook.com/docs/android'
                    )
                ],
                adapter='https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER',
                adapter_model=dict(
                    Banner='com.pingstart.mobileads.FacebookBanner',
                    Interstitial='com.pingstart.mobileads.FacebookInterstitial',
                    Native='com.pingstart.mobileads.FacebookNative'
                ),
                args=['placement_id'],
                login_auth_args=['access_token', 'app_id', 'app_secret'],
                auth_manager='',
                deleted=False
            ),
            dict(
                _id=int(gid(GidKey.network_key)),
                user_id=int(user_id),
                name='MoPub',
                sdk=[
                    dict(
                        platform='Android',
                        doc_link='https://dev.twitter.com/mopub/android',
                        sdk_link='https://dev.twitter.com/mopub/android/getting-started'
                    )
                ],
                adapter='https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER',
                adapter_model=dict(
                    Banner='com.pingstart.mobileads.MopubBanner',
                    Interstitial='com.pingstart.mobileads.MopubInterstitial',
                    Native=''
                ),
                args=['ad_unit_id'],
                login_auth_args=['username', 'password'],
                auth_manager='',
                deleted=False
            ),
        ]

        for network in init_networks:
            NetWork(network, True).save()


if __name__ == '__main__':
    # user_id = 1
    # name='PingStart'
    # sdk=dict(platform='Ios', doc_link='http://baidu.com', sdk_link='http://google.com')
    # adapter='http://bing.com'
    # auth_manager='name=a;password=12345;'
    # NetWork.create(user_id, name, sdk, adapter, auth_manager)
    # print 'ok'
    NetWork._init(3)


