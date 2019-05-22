$(document).ready(function(){

	var show_modal = function(){
		btn = $(this)
		$.ajax({
			type: "get",
			url: btn.attr("data-url"),
			dataType: "json",
			// data: {
			// 	title: $("#id_title").val(),
			// 	text: $("#id_text").val(),
			// 	csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
			// },
			beforeSend:function(){
				$("#post_new_modal").modal("show");
			},
			success:function(data){
				$("#post_new_modal .modal-content").html(data.html_form)
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
				console.log(form.attr("data-url"))
			},
			success:function(data){
				if (data.form_is_valid){
					$(".post-content").html(data.post_content);
					$("#post_new_modal").modal("hide");
					// update post
				}
				else{
					$("#post_new_modal .modal-content").html(data.html_form)
				}

			}
		})
		return false
	}
	$(document).on("click",".publish-btn",function(e){
		pk = $(this).attr("id")
		$.ajax({
			type: "GET",
			url: "",
			data: {
				'pk': pk,
			},
			success:function(){
				alert("Post Published!");
				$("#post_"+pk).fadeOut(300);
			}
		})
	})

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
})
