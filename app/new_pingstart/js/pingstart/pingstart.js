/**
 * Created by Administrator on 2016/4/11 0011.
 */
//(function () {
//    var s = document.createElement("script");
//    s.onload = function () {
//        bootlint.showLintReportForCurrentDocument([]);
//    };
//    s.src = "/js/new_pingstart/bootlint.js";
//    document.body.appendChild(s)
//})();

$(function(){
    $('#btn_overview').click(function(){
        $('#overview').show();
        $('#stats').hide();
        $('#btn_stats h4').removeClass("text-color");
        $('#btn_overview h4').addClass("text-color");
    });
    $('#btn_stats').click(function(){
        $('#overview').hide();
        $('#stats').show();
        $("#btn_overview h4").removeClass("text-color");
        $('#btn_stats h4').addClass("text-color");
    });
    $('#date').click(function(){
        $(this).addClass("data_style");
        $("#country").removeClass("data_style");
        $("#slot").removeClass("data_style");
        $("#report_stats_select").attr("disabled", false);
    });
    $('#country').click(function(){
        $(this).addClass("data_style");
        $("#date").removeClass("data_style");
        $("#slot").removeClass("data_style");
        $("#report_stats_select").attr("disabled", false);
    });
    $("#slot").click(function(){
        $(this).addClass("data_style");
        $("#date").removeClass("data_style");
        $("#country").removeClass("data_style");
        $("#report_stats_select").attr("disabled", true);
    });
});

$(function() {
    $('#btn_overview').click();
    $("#btn-box li span").click(function(){
        $("#btn-box li span").removeClass("btn_bg_color");
        $(this).addClass("btn_bg_color");
    });

        function cb(start, end) {
            $('#reportrange span').html(start.format('YYYY-MM-DD') + ' -- ' + end.format('YYYY-MM-DD'));
        }
        cb(moment().subtract(7, 'days'), moment().subtract(1, 'days'));

        $('#reportrange').daterangepicker({
            "opens": "right",
            ranges: {
               'Today': [moment(), moment()],
               'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
               'Last 7 Days': [moment().subtract(6, 'days'), moment()],
               'Last 30 Days': [moment().subtract(29, 'days'), moment()],
               'This Month': [moment().startOf('month'), moment().endOf('month')],
               'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }
        }, cb);

});
