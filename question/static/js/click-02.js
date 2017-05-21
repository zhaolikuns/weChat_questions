/**
 * Created by User on 2017/3/15.
 */

// JavaScript Document
$(function() {

        var $index = 0;
	    var $qindex = 0;
        var $priceNumber =  $(".price-number");
        var total = $('.tc_wt_box').length;

        $(".price-number").html();
        $(".total-number").html($('.tc_wt_box').length);
        var questionsIteratorIndex;

        var $slidesList = $(".answer").find(".tc_wt_box");

        $slidesList.hide().first().fadeIn(500).find(".prev,.submit-btn").addClass("on");
        $priceNumber.html($index+1)

        // 点击选择单选框
        $('.answer .tc_wt_box ul li').on("touchstart",function(e) {

            // var _index = $(this).parents('.tc_wt_box').index();
            // console.log(_index + "----")
            // var _next = $(this).parents('.tc_wt_box').hide().next('.tc_wt_box').show();
            //
            //
            // $(this).parents('.tc_wt_box').hide().next('.tc_wt_box').show();
            //
            // $(".price-number").html(_index+2);

            e.preventDefault();

             var thisLi = $(this);
                if (thisLi.hasClass('checked')) {
                    thisLi.removeClass('checked');
                } else {
                    // thisLi.parents('.answer').find('li').removeClass('checked');
                    thisLi.addClass('checked');
                }


        });



    // 点击下一题
    $(".test").find('.next').on("touchstart",function(e) {

            e.preventDefault();

            console.log($(this).parents('.tc_wt_box').index())
            // $index++;
            $priceNumber.html($(this).parents('.tc_wt_box').index()-3);
            $(this).parents(".tc_wt_box:not(total)").fadeOut(500,
            function() {
                $(this).next().fadeIn();
            });
            $qindex = $index;
        });

    // 点击上一题
    $(".test").find('.prev').on("touchstart",function(e) {
        e.preventDefault();
        console.log($(this).parents('.tc_wt_box').index())

        $priceNumber.html($(this).parents('.tc_wt_box').index()-5);
         $(this).parents('.tc_wt_box').fadeOut(500,
            function() {
                $(this).prev().fadeIn(500);
         });
        $qindex = $index;
    });








});