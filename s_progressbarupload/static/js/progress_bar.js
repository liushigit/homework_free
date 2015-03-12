$(document).ready(function(){
  uuid = $('#progressBar').data('progress_bar_uuid');
  // form submission
  $('form').submit(function(){
     this.target = "file-upload";
    // Prevent multiple submits
    if ($.data(this, 'submitted')){
        return false;
    }
    // Append X-Progress-ID uuid form action
    this.action += (this.action.indexOf('?') == -1 ? '?' : '&') + 'X-Progress-ID=' + uuid;
    // Update progress bar
    function update_progress_info() {
      $.getJSON(upload_progress_url, {'X-Progress-ID': uuid}, function(data, status) {
        //console.log(data);
        
        if (data.failed) {
            console.log("failed");
            $('.navbar').after('<div class="container"><div class="fade in alert alert-danger alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>上传失败。文件不能超过5M</div></div>');
            return;    
        }
        
        if (data.success) {
            console.log("success");
            data = undefined;
            $('.navbar').after('<div class="container"><div class="fade in alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>上传成功</div></div>');
            $("form").fadeOut(1000, function(){
                $(this).remove();
            });
        }
        
        if(data){
          console.log(data);
          $('#progressBar').removeAttr('hidden');  // show progress bar if there are datas
          var progress = parseInt(data.uploaded, 10)/parseInt(data.length, 10)*100;
          $('#progressBar').attr('value', progress);
          window.setTimeout(update_progress_info, 200);
        } else {
          $('#progressBar').attr('hidden', '');  // hide progress bar if no datas
        }
        
      });
    }

    window.setTimeout(update_progress_info, 1000);
    $.data(this, 'submitted', true); // mark form as submitted.
    return true;
  });
});
