var main = function() {
  
  $(".container-radius").hover(function(event) {
    $('.image',this).addClass('active-slide').animate({
      height: "50%"
    });
  },function(event) {
    $('.image',this).removeClass('active-slide').animate({
      height: "15px"
    });
  });

 
}

$(document).ready(main);