        function sendData(giphname, giphitself) {
            console.log("SENDDATA")
            var description = document.getElementsByName("description")[0].value;
            var giphData = { name: giphname, id: "send_giphy", description: description, submit: "no"};
            $.ajax({type : "POST",
                url : "{{ url_for('upload_gif') }}",
                data: JSON.stringify(giphData),
                contentType: 'application/json;charset=UTF-8',
                success: function (response) {
                console.log("GOOD")
                },
                error: function (response) {
                    alert("?");
                    window.location.replace(" {{ url_for('upload_gif') }}");
                }
            });
            $(giphitself).addClass("overlay")
        }

        $("#uploadbutton").on("click", function(){
            var description = document.getElementsByName("description")[0].value;
            var giphData = { submit: "submit_giphy", id: "no", description: description};
            $.ajax({type : "POST",
                url : "{{ url_for('upload_gif') }}",
                data: JSON.stringify(giphData),
                contentType: 'application/json;charset=UTF-8',
                success: function (response) {
                },
                error: function (response) {
                    alert("Could not find gif.");
                    window.location.replace(" {{ url_for('upload_gif') }}");

                }
            });
            window.location.replace(" {{ url_for('feed') }}");
            console.log("upload")
        });

    $(document).ready(function () {
        $("#giphysubmit").on("click", function(){
            var giphData = {submit: "giphysubmit",
                            id: "no",
                            keyword: $("#giphy")[0].value,
                            description: $("#description")[0].value}
                            ;
            $.ajax({type : "POST",
                url : "{{ url_for('upload_gif') }}",
                data: JSON.stringify(giphData),
                contentType: 'application/json;charset=UTF-8',
                success: function (response) {
                    response = $.parseJSON( response );
                    response["urldata"].forEach(function(gif_url) {
                    $("#gifs").append("<br>" +
                        '<img src='+gif_url+' id = "send_giphy" onmouseover="bigImg(this)" onmouseout="normalImg(this)" onclick ="sendData(src, this)" >' +
                        "<br>")
                });
                },
                error: function (response) {
                    alert("Bad request. Please try again.");
                window.location.replace(" {{ url_for('upload_gif') }}");
                }
            });
        });
    });