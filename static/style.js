function slideToggleCommentForm(){
  jQuery("#comment_form").slideToggle();
  jQuery("#add_comment").slideToggle();
}

function addPostComment(){
  var comment={
    content: jQuery("#id_content").val(),
    name: jQuery("#id_name").val(),
    email: jQuery("#id_email").val(),
  }
  jQuery.post("/blog/",comment,
    function(request){
      jQuery("#comment_errors").empty();
      if(Response.success=="True"){
        jQuery("#submit_comment").attr('disabled','disabled');
        jQuery("#no_comments").empty();
        jQuery("#comments").prepend(response.html).slideDown();
        new_comment=jQuery("#comments").children(":first");
        new_comment.addClass('new_comment');
        jQuery("#comment_form").slideToggle();

      }
      else{
        jQuery("#comment_errors").append(response.html);
      }     
    },"json");
}


jQuery("#submit_comment").click(addPostComment);
jQuery("#comment_form").addClass('hidden');
jQuery("#add_comment").click(slideToggleCommentForm);
jQuery("#add_comment").addClass('visible');
jQuery("#cancel_comment").click(slideToggleCommentForm);

$('.message a').click(function(){
  $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});