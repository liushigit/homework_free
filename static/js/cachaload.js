$(function(){
    $('#id_captcha_1').after('<button class="btn btn-link js-captcha-refresh">看不清</button>');
    
    $('.js-captcha-refresh').click(function(){

        $.getJSON('/caprefresh/', {}, function(json){
            var img_url = json['new_cptch_image'];
            var cap_key = json['new_cptch_key'];
            $('img.captcha').attr('src', img_url);
            $('#id_captcha_0').attr('value', cap_key);
        });
        
        return false;
    });
});




