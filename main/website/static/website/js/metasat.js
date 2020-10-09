
$(document).ready(function(){
    
    var currentTab = localStorage.getItem('currentTab');
    console.log(currentTab);
    var currentElement = localStorage.getItem('currentElement');

    if (currentElement != "noelement") {
        var windowSize = $(window).width();
        if(windowSize < 768){
            $("#family").removeClass('active');
            $("#segment").removeClass('active');
            $("#alpha").removeClass('active');
            $("#search").removeClass('active');
            $('.'+currentTab+'-tab').removeClass("active");//
            $('.'+currentTab+'-tab').attr("aria-selected", "false");
        }
    }

    $(".letter").on("keyup", function(){
        if (event.keyCode === 13) {
            thisletter = event.target.innerHTML;
            event.preventDefault();
            document.getElementById(thisletter).scrollIntoView(true);
            $("#letter"+thisletter).focus();
        }
    });

    $(".letter").on("click", function(){
        thisletter = event.target.innerHTML;
        event.preventDefault();
        document.getElementById(thisletter).scrollIntoView(true);
        $("#letter"+thisletter).focus();
    });


    // $(".mobileletter").on("keyup", function(){
    //     if (event.keyCode === 13) {
    //         thisletter = event.target.innerHTML;
    //         event.preventDefault();
    //         document.getElementById("m"+thisletter).scrollIntoView(true);
    //         $("#mletter"+thisletter).focus();
    //     }
    // });


    // $(".mobileletter").on("click", function(){
    //     thisletter = event.target.innerHTML;
    //     event.preventDefault();
    //     document.getElementById("m"+thisletter).scrollIntoView(true);
    //     $("#mletter"+thisletter).focus();
    // });

    $(".totopimg").on("keyup", function(){
        if (event.keyCode === 13) {
            event.preventDefault();
            document.getElementById("alpha-tab").scrollIntoView(true); 
            $("#alpha-tab").focus();
        }
    });


    $(".totopimg").on("click", function(){
        event.preventDefault();
        document.getElementById("alpha-tab").scrollIntoView(true);
        $("#alpha-tab").focus();
    });


    $(".totopimgm").on("click", function(){
            event.preventDefault();
            document.getElementById("topm").scrollIntoView(true); 
            $("#alpha-tab").focus();
    });


    $('.alpha-tab').click(function (e) {
        localStorage.setItem('currentTab', 'alpha');
        localStorage.setItem('inactive1', 'family');
        localStorage.setItem('inactive2', 'segment');

        if ($(this).hasClass("active")) {
            console.log("has class");
           
            $("#alpha").removeClass('active');
            e.preventDefault();
            e.stopPropagation();
            $('.alpha-tab').removeClass("active");//
            $('.alpha-tab').attr("aria-selected", "false");
        }
    });

    $('.family-tab').click(function (e) {
        localStorage.setItem('currentTab', 'family');
        localStorage.setItem('inactive1', 'segment');
        localStorage.setItem('inactive2', 'alpha');
        localStorage.setItem('inactive3', 'search');

        if ($(this).hasClass("active")) {
           
            $("#family").removeClass('active');
            e.preventDefault();
            e.stopPropagation();
            $('.family-tab').removeClass("active");//
            $('.family-tab').attr("aria-selected", "false");
        }
    });

    $('.segment-tab').click(function (e) {
        localStorage.setItem('currentTab', 'segment');
        localStorage.setItem('inactive1', 'family');
        localStorage.setItem('inactive2', 'alpha');
        localStorage.setItem('inactive3', 'search');

        if ($(this).hasClass("active")) {
           
            $("#segment").removeClass('active');
            e.preventDefault();
            e.stopPropagation();
            $('.segment-tab').removeClass("active");//
            $('.segment-tab').attr("aria-selected", "false");
        }
    });

    $('.search-tab').click(function (e) {
        localStorage.setItem('currentTab', 'search');
        localStorage.setItem('inactive1', 'family');
        localStorage.setItem('inactive2', 'alpha');
        localStorage.setItem('inactive3', 'segment');

        if ($(this).hasClass("active")) {
           
            $("#search").removeClass('active');
            e.preventDefault();
            e.stopPropagation();
            $('.search-tab').removeClass("active");//
            $('.search-tab').attr("aria-selected", "false");
        }
    });

    $(window).on('resize', function(e){
        var windowSize = $(window).width(); // Could've done $(this).width()

        if(windowSize > 768){
            var currentTab = localStorage.getItem('currentTab');
            var inactive1 = localStorage.getItem('inactive1');
            var inactive2 = localStorage.getItem('inactive2');
            var inactive3 = localStorage.getItem('inactive3');

            $("#"+currentTab).addClass('active');
            e.preventDefault();
            e.stopPropagation();
            $('.'+inactive1+'-tab2').removeClass("active");
            $('.'+inactive2+'-tab2').removeClass("active");
            $('.'+inactive3+'-tab2').removeClass("active");
            $('.'+currentTab+'-tab2').addClass("active");//
            $('.'+currentTab+'-tab2').attr("aria-selected", "true");
            $('.'+inactive1+'-tab').removeClass("active");
            $('.'+inactive2+'-tab').removeClass("active");
            $('.'+inactive3+'-tab').removeClass("active");
            $('.'+currentTab+'-tab').addClass("active");//
            $('.'+currentTab+'-tab').attr("aria-selected", "true");
            $('.'+currentTab).addClass("active");//
            $('.'+currentTab).attr("aria-selected", "true");
        }
    });

});