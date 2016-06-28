$(document).ready(function() {

	$('form').on('submit', function(event) {

			event.preventDefault();

			var formData = new FormData($('form')[0]);

			$.ajax({
				xhr : function() {
					var xhr = new window.XMLHttpRequest();

					xhr.upload.addEventListener('progress', function(e) {

						if (e.lengthComputable) {
							console.log('Percentage Uploaded: ' + (e.loaded / e.total))
							var percent = Math.round(e.loaded / e.total * 100)

							$('#progress-bar').css('width', percent + '%');
							$('button').removeClass("btn btn-primary").addClass("btn btn-primary disabled");
						}

					});

					return xhr;
				},
				type : 'POST',
				url : '/new',
				data : formData,
				processData : false,
				contentType : false,
				success : function() {
					$('#submit-modal').modal('toggle');
				}
			});
	});
});