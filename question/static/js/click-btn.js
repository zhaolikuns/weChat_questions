/**
 * Created by User on 2017/3/15.
 */

// JavaScript Document
$(function() {

        var $index = 0;
	    var $qindex = 0;
        var $priceNumber =  $(".price-number");
        var total = $('.tc_wt_box').length;

        // $(".price-number").html();
        // $(".total-number").html($('.tc_wt_box').length);
        var questionsIteratorIndex;

        var $slidesList = $(".answer").find(".tc_wt_box");

        $slidesList.hide().first().fadeIn(500).find(".prev,.submit-btn").addClass("on");
        // $priceNumber.html($index+1)






    // 点击下一题
    $(".test").find('.next').on("touchstart",function(e) {

            e.preventDefault();

            console.log($(this).parents('.tc_wt_box').index())
            // $index++;
            // $priceNumber.html($(this).parents('.tc_wt_box').index()-3);
            $(this).parents(".tc_wt_box:not(total)").fadeOut(500,
            function() {
                $(this).next().fadeIn();
            });
            $qindex = $index;
        });

    // 点击上一题
    $(".test").find('.prev').on("touchstart",function(e) {

            e.preventDefault();

        // $index--;
        // $priceNumber   .html($index+2);
        //  $(this).parents('.tc_wt_box').fadeOut(500,
        //     function() {
        //         $(this).prev().fadeIn(500);
        //  });
        // $qindex = $index;
        console.log($(this).parents('.tc_wt_box').index())

        // $priceNumber.html($(this).parents('.tc_wt_box').index()-5);
         $(this).parents('.tc_wt_box').fadeOut(500,
            function() {
                $(this).prev().fadeIn(500);
         });
        $qindex = $index;
    });


    $(".menu_container").find(".btn-submit").click(function(){

        if( $(this).parents('.tc_wt_box').find('input.agreeRule').is(":checked") === false){
            alert("请答完全部的题目");
            return false;
        }

    });





});