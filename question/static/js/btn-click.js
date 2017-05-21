/**
 * Created by budaowen on 17/3/16.
 */


$(function(){

    var $answer = $(".answer");
    var $tc_wt_box = $(".answer > .tc_wt_box");
    var $menu_container = $(".menu_container");
    var $btn_answer = $(".btn_answer",$menu_container);

    var i = 1;

    $(".total-number").html($('.tc_wt_box').length)
    //问题答案点击
    function change(now) {
        $('.test .tc_wt_box').eq(now).show().find('h2').animate({
            'margin-top': '1.69333rem',
            'opacity': '1'
        },600,function() {
                    $('.test .tc_wt_box').eq(now).find('li').each(function(i) {
                        $(this).delay(i * 100);
                        $(this).show(350);
                    });
                });

        $(".prev,.submit-btn").addClass("on");
        $(".next").addClass("on-center");

        // 数字记录仪
        $(".price-number").html(now+1);
    }
    change(0);


    // 点击上一个按钮
    $('.prev').click(function(){

        i--;
        if(i<0){
            i = 1;
            $tc_wt_box.eq(i).show().find('h2').animate({
                'margin-top': '1.69333rem',
                'opacity': '1'
                },600,function() {
                        $('.test .tc_wt_box').eq(now).find('li').each(function(i) {
                            $(this).delay(i * 100);
                            $(this).show(350);
                        });
            });
        }
    });


    // 点击下一个按钮
    $('.next').click(function(){

        i++;

        $(".answer > .tc_wt_box").eq(i).css("display","block").siblings(".tc_wt_box").css("display","none");
        $(".price-number").html(i);

        // $(".prev").eq(i).removeClass("on");
        // $(".next").eq(i).removeClass("on-center");
        //
        //  if(i>$('.tc_wt_box').length){
        //      i = $('.tc_wt_box').length;
        //     $tc_wt_box.eq(i).show().siblings().hidden;
        //     $(".prev").eq(i).removeClass("on");
        //     $(".next").eq(i).removeClass("on");
        //  }


    });

})