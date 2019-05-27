$(document).ready(function(){

	var show_modal = function(){
		btn = $(this)
		$.ajax({
			type: "get",
			url: btn.attr("data-url"),
			dataType: "json",
			beforeSend:function(){
			},
			success:function(data){
				$("#post_new_modal .modal-content").html(data.html_form)
				$("#post_new_modal").modal("show");
			}
		})
	}

	var post_save = function(){
		var form = $(this);
		$.ajax({
			type: form.attr("method"),
			url: form.attr("data-url"),
			data: form.serialize(),
			dataType: "json",
			beforeSend:function(){
				console.log(form.serialize())
			},
			success:function(data){
				if (data.form_is_valid){
					$(".post-content").html(data.post_content);
					$("#post_new_modal").modal("hide");
					// update post_
				}
				else{
					$("#post_new_modal .modal-content").html(data.html_form)
				}

			}
		})
		return false
	}
	var show_post_comment = function(){
		btn = $(this)
		$.ajax({
			type: "get",
			url: btn.attr("data-url"),
			dataType: "json",
			beforeSend:function(){
			},
			success:function(data){
				$("#post_new_modal .modal-content").html(data.html_form)
				$("#post_new_modal").modal("show");
			}
		})
	}
	var commit = function(form){
		$.ajax({
			type: form.attr("method"),
			url: form.attr("data-url"),
			data: form.serialize(),
			dataType: "json",
			beforeSend:function(){
				
			},
			success:function(data){
				if (data.form_is_valid){
					$("#post_new_modal .modal-content").html(data.html_form);
				}
				else{
					alert("Form data is invalid. Try Again")
				}
			}
		})
	}
	var comment_save = function(e){
		e.preventDefault()
		var form = $(this);
		if(form.attr("id")=="comment_remove_form" 
			|| form.attr("id")=="comment_flag_form"
			|| form.attr("id")=="comment_remove_flag_form"){
			if(confirm("Confirm this action?")){
				commit(form)
			}
		}
		else{
			commit(form)
		}
		return false
	}

	// login
	$(".show-login-modal").click(show_modal)

	// create post
	$(".show-post-new-modal").click(show_modal)
	$("#post_new_modal").on("submit","#post_new_form", post_save)

	// update post
	$(".post-content").on("click",".show-post-update-modal", show_modal)
	$("#post_new_modal").on("submit","#post_update_form", post_save)

	// delete post
	$(".post-content").on("click",".show-post-delete-modal", show_modal)
	$("#post_new_modal").on("submit","#post_delete_form", post_save)

	// publish post
	$(".post-content").on("click",".show-post-publish-modal", show_modal)
	$("#post_new_modal").on("submit","#post_publish_form", post_save)

	// create comment
	$(".post-content").on("click",".show-post-comment-modal", show_post_comment)
	$("#post_new_modal").on("submit","#comment_new_form", comment_save)

	// delete post
	$(".modal-content").on("submit","#comment_remove_form", comment_save)
	$(".modal-content").on("submit","#comment_flag_form", comment_save)
	$(".modal-content").on("submit","#comment_remove_flag_form", comment_save)

})
