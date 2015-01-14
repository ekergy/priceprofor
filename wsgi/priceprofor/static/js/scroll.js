var cSc;

$('.navigation a').on('click', scrollSeccion)

function scrollSeccion ()
{
    var seccion = $(this).attr('href');
    var posY = $(seccion).offset().top;
    $('html, body').animate({ scrollTop: posY },{easing:'easeInOutExpo', duration:900});
    return false;
}