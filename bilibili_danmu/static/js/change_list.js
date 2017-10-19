/**
 * Created by Gzp on 2017/4/8.
 */
$.format = function (source, params) {
    if (arguments.length == 1)
        return function () {
            var args = $.makeArray(arguments);
            args.unshift(source);
            return $.format.apply(this, args);
        };
    if (arguments.length > 2 && params.constructor != Array) {
        params = $.makeArray(arguments).slice(1);
    }
    if (params.constructor != Array) {
        params = [params];
    }
    $.each(params, function (i, n) {
        source = source.replace(new RegExp("\\{" + i + "\\}", "g"), n);
    });
    return source;
};

$(document).ready(function () {

    var tr = '<tr class="{0}">' +
        '<td class="action-checkbox">' +
        '<input type="checkbox" name="_selected_action" value="{1}" class="action-select"></td>' +
        '<th class="field-id"><a href="/admin/bilibili_danmu/tt234024/{1}/change/">{1}</a></th>' +
        '<td class="field-name"><a href="/admin/bilibili_danmu/tt234024/{1}/change/">{2}</a></td>' +
        '<td class="field-comment">{3}</td><td class="field-time">{4}</td></tr>';

    var ajax_url = $('.field-id')[0].children[0].href + 'ajax/get_data';
    var data_line = [];
    var old_ajax_url = '';


    var timer1 = window.setInterval(request_new_data, 1000);
    var timer2 = window.setInterval(auto_refresh, 1000);

    function request_new_data() {
        if (old_ajax_url != ajax_url) {
            old_ajax_url = ajax_url;
        $.ajax({
            url: ajax_url,
            type: 'GET',
            dataType: "JSON",
            timeout: 3000,
            async: true,
            cache: false,
            beforeSend: LoadFunction, //加载执行方法
            error: erryFunction,   //错误执行方法
            success: succFunction //成功执行方法
        })
        function LoadFunction() {
        }

        function erryFunction() {
            console.log('Ajax error!')
            old_ajax_url = '';
        }

        function succFunction(data) {
            // console.log(data.length);
            var json = eval(data); //数组
            $.each(json, function (index, item) {
                //循环获取数据
                data_line.unshift(item)
            });
            if (json.length == undefined){
                old_ajax_url = '';
            }
        }
        }
    }

    function auto_refresh() {
        var data = '';
        var tr_class = '';
        var tbody = $('tbody')[0];
        while (data_line.length > 0) {
            data = data_line.pop();
            tr_class = $(tbody.children[0]).attr('class');
            if (tr_class == 'row1'){
                tr_class = 'row2';
            }else{
                tr_class = 'row1';
            }
            var html = $.format(tr, tr_class, data.id, data.name, data.comment, data.time);
            if (tbody.children.length < 100) {
                $(tbody).prepend(html)

            } else {
                $(tbody).prepend(html)
                $(tbody).children("tr:last-child").remove()
            }
        }
        ajax_url = $('.field-id')[0].children[0].href + 'ajax/get_data';
    }

});
