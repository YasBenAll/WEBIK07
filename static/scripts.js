// Upload.html
    function bigImg(img) {
      img.style.height = 1.5*img.naturalHeight.toString() + "px";
      img.style.width = 1.5*img.naturalWidth.toString() + "px";
    }

    function normalImg(img) {
      img.style.height = img.naturalHeight.toString() + "px";
      img.style.width = img.naturalWidth.toString() + "px";
    }

// Feed.html

    $(document).ready(function(){
        $("#like").on("click", function(){
            $.ajax({type : "POST",
                url : "{{ url_for('feed') }}",
                data: JSON.stringify("like"),
                contentType: 'application/json;charset=UTF-8',
            });
            $.get("/feedcontent", function(picture) {
                $("#content").html(picture);
            });
        });
        $("#dislike").on("click", function(){
            $.ajax({type : "POST",
                url : "{{ url_for('feed') }}",
                data: JSON.stringify("dislike"),
                contentType: 'application/json;charset=UTF-8',
            });
            $.get("/feedcontent", function(picture) {
                $("#content").html(picture);
            });
        });
        $("#ongepast").on("click", function(){
            $.ajax({type : "POST",
                url : "{{ url_for('feed') }}",
                data: JSON.stringify("ongepast"),
                contentType: 'application/json;charset=UTF-8',
            });
            $.get("/feedcontent", function(picture) {
                $("#content").html(picture);
            });
        });
        $("#volg").on("click", function(){
            $.ajax({type : "POST",
                url : "{{ url_for('feed') }}",
                data: JSON.stringify("volg"),
                contentType: 'application/json;charset=UTF-8',
            });
            $.get("/feedcontent", function(picture) {
                $("#content").html(picture);
            });
        });
    });

    $(document).ready(function(){
        document.onkeyup = checkKey;

        function checkKey(e) {

            console.log("a")

            e = e || window.event;


                if (e.keyCode == '37'){

                    console.log('test')
                     $.ajax({type : "POST",
                            url : "{{ url_for('feed') }}",
                            data: JSON.stringify("dislike"),
                            contentType: 'application/json;charset=UTF-8',
                        });
                        console.log("hallo");
                        $.get("/feedcontent", function(picture) {
                            $("#content").html(picture);
                        });
                }

                if (e.keyCode == '39'){
                    console.log("right");
                    $.ajax({type : "POST",
                        url : "{{ url_for('feed') }}",
                        data: JSON.stringify("like"),
                        contentType: 'application/json;charset=UTF-8',
                    });
                    $.get("/feedcontent", function(picture) {
                        $("#content").html(picture);
                    });
                }


            }
        });

// register.html

