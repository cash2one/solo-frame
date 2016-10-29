from pymongo import Connection
con = Connection()
db = con.pingstart
table = db.user
values = table.find()

n_db = con.new_pingstart
n_table = n_db.user


for value in values:
    val = {}
    val["_id"] = value["_id"]
    val["company"] = value["company"]
    val["status"] = value["status"]
    val["regist_time"] = value["regist_time"]
    val["password"] = value["password"]
    val["email"] = value["email"]
    val["username"] = value.get("username", val["email"])
    val["last_update"] = str(value["regist_time"])
    val["last_login"] = str(value["regist_time"])
    val["deleted"] = False
    n_table.save(val)


table = con.pingstart.slot_income
values = table.find()

n_table = con.new_pingstart.dateReport
for value in values:
    val = {}
    val["_id"] = value["_id"]
    val["impression"] = value["impression"]
    val["conversion"] = value["conversion"]
    val["show_conversion"] = value["show_conversion"]
    val["revenue"] = value["income"]
    val["show_revenue"] = value["show_income"]
    val["slot_id"] = value["slotId"]
    val["network"] = "PingStart"
    val["request"] = value["request"]
    val["click"] = value["click"]
    val["show_click"] = value["show_click"]
    val["createdTime"] = value["createdTime"]
    n_table.save(val)

n_table = con.new_pingstart.netWork
users = con.pingstart.user.find()
i = 1
networks = [
    {"user_id": 1, "name": "PingStart", "deleted": False, "adapter": "https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER", "args": [ "publisher_id", "slot_id" ], "login_auth_args" : [ ], "auth_manager" : "", "adapter_model" : { "Banner" : "com.pingstart.adsdk.adapter.AdBanner", "Interstitial" : "com.pingstart.adsdk.adapter.AdInterstitial", "Native" : "com.pingstart.adsdk.adapter.AdNative" }, "sdk" : [ { "platform" : "Android", "doc_link" : "", "sdk_link" : "" }]},
    { "user_id" : 1, "name" : "Vungle", "deleted" : False, "adapter" : "https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER", "args" : [ "app_id" ], "login_auth_args" : [ "API_ID", "API_KEY" ], "auth_manager" : "", "adapter_model" : { "Banner" : "", "Interstitial" : "com.pingstart.mobileads.VungleInterstitial", "Native" : "" }, "sdk" : [ { "platform" : "Android", "doc_link" : "https://support.vungle.com/hc/zh-cn/articles/204463100-Advanced-Settings-for-Vungle-Android-SDK", "sdk_link" : "https://v.vungle.com/sdk" }]},
    { "user_id" : 1, "name" : "AdColony", "deleted" : False, "adapter" : "https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER", "args" : [ "app_id", "zone_id", "client_options", "all_zone_ids" ], "login_auth_args" : [ "API_KEY", "User", "Password" ], "auth_manager" : "", "adapter_model" : { "Banner" : "", "Interstitial" : "com.pingstart.mobileads.AdColonyInterstitial", "Native" : "" }, "sdk" : [ { "platform" : "Android", "doc_link" : "https://adcolony-www-common.s3.amazonaws.com/pub-adapter/android/AdColonyAdapterIntegrationGuide.pdf", "sdk_link" : "https://github.com/AdColony/" } ] },
    { "user_id" : 1, "name" : "AdMob", "deleted" : False, "adapter" : "https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER", "args" : [ "ad_unit_id" ], "login_auth_args" : [ "Json_Token" ], "auth_manager" : "", "adapter_model" : { "Banner" : "com.pingstart.mobileads.AdMobBanner", "Interstitial" : "com.pingstart.mobileads.AdMobInterstitial", "Native" : "com.pingstart.mobileads.AdMobNative" }, "sdk" : [ { "platform" : "Android", "doc_link" : "https://developers.google.com/admob/android/interstitial?hl=en#helpful_resources", "sdk_link" : "https://developers.google.com/admob/android/download" } ] },
    {"user_id" : 1, "name" : "Facebook Audience Network", "deleted" : False, "adapter" : "https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER", "args" : [ "placement_id" ], "login_auth_args" : [ "access_token", "app_id", "app_secret" ], "auth_manager" : "", "adapter_model" : { "Banner" : "com.pingstart.mobileads.FacebookBanner", "Interstitial" : "com.pingstart.mobileads.FacebookInterstitial", "Native" : "com.pingstart.mobileads.FacebookNative" }, "sdk" : [ { "platform" : "Android", "doc_link" : "https://developers.facebook.com/docs/audience-network/android/interstitial", "sdk_link" : "https://developers.facebook.com/docs/android" } ] },
    {"user_id" : 1, "name" : "MoPub", "deleted" : False, "adapter" : "https://github.com/PingStart/PingStart_SDK_Example/tree/master/ADAPTER", "args" : [ "ad_unit_id" ], "login_auth_args" : [ "username", "password" ], "auth_manager" : "", "adapter_model" : { "Banner" : "com.pingstart.mobileads.MopubBanner", "Interstitial" : "com.pingstart.mobileads.MopubInterstitial", "Native" : "" }, "sdk" : [ { "platform" : "Android", "doc_link" : "https://dev.twitter.com/mopub/android", "sdk_link" : "https://dev.twitter.com/mopub/android/getting-started" } ] }]

for user in users:
    user_id = user["_id"]
    for net in networks:
        net["_id"] = i
        net["user_id"] = user_id
        i = i + 1
        n_table.save(net)

slots = con.pingstart.slots.find()
n_slot = con.new_pingstart.slots

for slot in slots:
    n = con.new_pingstart.netWork.find_one({"user_id": slot["appId"], "name": "PingStart"})
    val = {}
    val["_id"] = slot["_id"]
    val["status"] = slot["status"]
    val["category"] = slot["category"]
    val["slotType"] = slot["slotType"]
    val["name"] = slot["name"]
    val["keyword"] = slot["keyword"]
    val["appName"] = slot["appName"]
    val["deleted"] = False
    val["last_operated"] = ""
    val["platform"] = slot["platform"]
    val["version"] = slot["version"]
    val["appId"] = slot["appId"]
    val["first_filing"] = slot.get("first_filing", 1)
    val["network"] = []
    network_detail = {}
    network_detail["is_paused"] = False
    network_detail["is_auth"] = True
    network_detail["adapter"] = "com.pingstart.adsdk.adapter.AdNative"
    network_detail["placement_id"] = "publisher_id="+str(val["appId"])+";slot_id="+str(slot["_id"])
    network_detail["priority"] = 1
    network_detail["network_name"] = "PingStart"
    network_detail["network_id"] = n["_id"]
    val["network"].append(network_detail)
    print val
    n_slot.save(val)
