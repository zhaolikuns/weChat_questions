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
        // $('.answer .tc_wt_box ul li').on("touchstart",function() {
        //     var _index = $(this).parents('.tc_wt_box').index();
        //     var _next = $(this).parents('.tc_wt_box').hide().next('.tc_wt_box').show();
        //     $(".price-number").html(_index+2);
        //
        //
        //      var thisLi = $(this);
        //         if (thisLi.hasClass('checked')) {
        //             thisLi.removeClass('checked');
        //         } else {
        //             thisLi.parents('.answer').find('li').removeClass('checked');
        //             thisLi.addClass('checked');
        //         }
        // });



    // 点击下一题
    $(".test").find('.next').on("touchstart",function() {
            $index++
            $priceNumber.html($index+1);
            $(this).parents(".tc_wt_box:not(total)").fadeOut(500,
            function() {
                $(this).next().fadeIn();
            });
            $qindex = $index;
        });

    // 点击上一题
    $(".test").find('.prev').on("touchstart",function() {
        $index--;
          // var _index = $(this).parents('.tc_wt_box').index();
          //   alert(1);
        // _index--;
        $priceNumber.html($index+1);
         $(this).parents('.tc_wt_box').fadeOut(500,
            function() {
                $(this).prev().fadeIn(500);
         });
        $qindex = $index;
    });





});