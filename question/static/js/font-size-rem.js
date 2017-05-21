
$(function(){
    function getViewportSize () {
        return {
            width: window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth,
            height: window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
        };
    }

    $(".test").css({
        // "height":getViewportSize ().height,
        "width":getViewportSize ().width
    });

    $(window).resize(function(){
       $(".test").css({
            // "height":getViewportSize ().height,
            "width":getViewportSize ().width
        });
    })

    $(".answer-shadow").height(getViewportSize ().height);


    $(".test").find(".list-contents").click(function(){
        $(this).parents(".test").find(".answer-shadow").css("display","block");
        $(".test").css("height",getViewportSize ().height);

        var $scores = $(this).find(".scores").html();
        var $answer_number = $(this).find(".answer-number").html();
        var $urls = $(this).find(".url-hidden").html();
        $(".answer-shadow .answer .result-show h2").find(".total").text($scores);
        $(".answer-shadow .answer .result-show h3").find(".success-number").text($answer_number);


        $(".answer-shadow .answer .menu_container").find(".url-href").attr("href",$urls);
    });

    $(".answer-shadow").find(".close-btn").click(function(e){
        e.preventDefault();
        $(this).parents(".answer-shadow").css("display","none");
        $(".test").css("height","auto");
    });


})