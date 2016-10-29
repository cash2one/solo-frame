(function(){
    Pingstart= {

        date_fmat: function (fmt) {
            var o = {
                "M+": this.getMonth() + 1, //月份
                "d+": this.getDate(), //日
                "h+": this.getHours() % 12 == 0 ? 12 : this.getHours() % 12, //小时
                "H+": this.getHours(), //小时
                "m+": this.getMinutes(), //分
                "s+": this.getSeconds(), //秒
                "q+": Math.floor((this.getMonth() + 3) / 3), //季度
                "S": this.getMilliseconds() //毫秒
            };
            var week = {
                "0": "/u65e5",
                "1": "/u4e00",
                "2": "/u4e8c",
                "3": "/u4e09",
                "4": "/u56db",
                "5": "/u4e94",
                "6": "/u516d"
            };
            if (/(y+)/.test(fmt)) {
                fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
            }
            if (/(E+)/.test(fmt)) {
                fmt = fmt.replace(RegExp.$1, ((RegExp.$1.length > 1) ? (RegExp.$1.length > 2 ? "/u661f/u671f" : "/u5468") : "") + week[this.getDay() + ""]);
            }
            for (var k in o) {
                if (new RegExp("(" + k + ")").test(fmt)) {
                    fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
                }
            }
            return fmt;
        },

        getBeforeDate: function (n) {
            var n = n;
            var d = new Date();
            var year = d.getFullYear();
            var mon = d.getMonth() + 1;
            var day = d.getDate();
            if (day <= n) {
                if (mon > 1) {
                    mon = mon - 1;
                }
                else {
                    year = year - 1;
                    mon = 12;
                }
            }
            d.setDate(d.getDate() - n);
            year = d.getFullYear();
            mon = d.getMonth() + 1;
            day = d.getDate();
            s = year + "-" + (mon < 10 ? ('0' + mon) : mon) + "-" + (day < 10 ? ('0' + day) : day);
            return s;
        },

        sort: function(model, li, key1, key2){
            model[li].sort(function(a, b){
                 var _desc, a1, b1;
                if (model.desc){
                    _desc = 1;
                } else {
                    _desc = -1;
                }
                if(!key2){
                    a1 = a[key1];
                    b1 = b[key1];
                }else{
                    a1 = a[key1][key2];
                    b1 = b[key1][key2];
                }
                if (a1 == '*'){
                    a1 = 0
                };
                if (b1 == '*'){
                    b1 = 0
                }
                if (b1 == a1){
                    return 0;
                }
                if (b1 > a1){
                    return _desc * 1;
                }
                if (b1 < a1){
                    return _desc * -1;
                }
            });
            model.desc = !model.desc
        }
    }
    return Pingstart;
})();