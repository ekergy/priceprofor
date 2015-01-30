var cSc
var cScBot

$(document).on('scroll', gestorScroll)

$('.navigation a').on('click', scrollSeccion)

function gestorScroll ()
{
	cSc = $(document).scrollTop();
	console.log(cSc);
	cScBot = ($(document).scrollTop() + $(window).height());
	console.log(cScBot);
	$('section').each(posicionFondo);

	if (cSc < $('section#feature').offset().top) {
                    $('a').find('div').css({background: 'rgba(211,215,237,.5)'});
                    $('a').eq(0).find('div').css({background: 'rgba(73,121,63,.7)'});
                  }
    else if (cSc < $('section#services').offset().top){
                    $('a').find('div').css({background: 'rgba(211,215,237,.5)'});
                    $('a').eq(1).find('div').css({background: 'rgba(73,121,63,.7)'});
                  }
    else if (cSc < $('section#featureBis').offset().top){
                    $('a').find('div').css({background: 'rgba(211,215,237,.5)'});
                    $('a').eq(2).find('div').css({background: 'rgba(73,121,63,.7)'});
                  }
    else if (cScBot < $('section#footer').offset().top){
                    $('a').find('div').css({background: 'rgba(211,215,237,.5)'});
                    $('a').eq(3).find('div').css({background: 'rgba(73,121,63,.7)'});
                  }
            else {
                    $('a').find('div').css({background: 'rgba(211,215,237,.5)'});
                    $('a').eq(4).find('div').css({background: 'rgba(73,121,63,.7)'});
                  };
}

function posicionFondo (i)
{
    var distanciaSuperior = $(this).offset().top;
    $(this).css({ backgroundPosition: 'center '+ ((cSc-distanciaSuperior)*0.4) +'px' });
}

function scrollSeccion ()
{
    var seccion = $(this).attr('href');
    var posY = $(seccion).offset().top;
    $('html, body').animate({ scrollTop: posY },{easing:'easeInOutExpo', duration:900});
    return false;
}

