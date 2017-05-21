/**
 * Created by User on 2017/3/15.
 */

// JavaScript Document
$(function() {

        // 点击里显示遮罩层
        $(".test").find(".list-contents").on("touchend",function(){
            // e.preventDefault();
            $(this).parents(".test").find(".answer-shadow").css("display","block");
            $("body").css({"overflow":"hidden"});

            var $scores = $(this).find(".scores").html();
            $(".answer-shadow .answer .result-show h2").find(".total").text($scores);
        });


        // 点击close遮罩层隐藏
        $(".answer-shadow").find(".close-btn").on("touchstart",function(){

            $(this).parents(".answer-shadow").css("display","none");
            $("body").css("overflow","auto");

        });




});

        // var ObjLists = document.querySelectorAll(".list-contents");
        // var ObjTest = document.getElementById("test");
        // var ObjAnswerShadow = document.getElementById("answer-shadow");
        // for ( var i =0;i<ObjLists.length;i++ ){
        //     ObjLists[i].index = i;
        //     ObjLists[i].addEventListener("touchend",function(e){
        //         e.preventDefault();
        //         ObjAnswerShadow.css("display","block");
        //         document.body.css("overflow","hidden");
        //     },false);
        // }


        function stopTouchendPropagationAfterScroll(){
            var locked = false;

            window.addEventListener('touchmove', function(ev){
                locked || (locked = true, window.addEventListener('touchend', stopTouchendPropagation, true));
            }, true);
            function stopTouchendPropagation(ev){
                ev.stopPropagation();
                window.removeEventListener('touchend', stopTouchendPropagation, true);
                locked = false;
            }
        }
        stopTouchendPropagationAfterScroll();