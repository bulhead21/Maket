
$().ready(function () {
  //мобильное меню
    $('#mobile-menu-btn').click( function(event){
        event.preventDefault();
        $('#mobile-menu').fadeIn();
        $('#mm__wrapper')
            .css('visibility', 'visible')
            .css('transform', 'translateX(0)');
        $("body").css("overflow","hidden");
    });
  //закрытие мобильного меню
    $('.mm__close').click( function(){
        $('#mobile-menu').fadeOut();
        $('#mm__wrapper')
            .css('visibility', 'hidden')
            .css('transform', 'translateX(-100%)');
        $("body").css("overflow","auto");
    });
    });
