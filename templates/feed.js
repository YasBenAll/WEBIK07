    $(document).ready(function(){
        $("#like").on("click", function(){
            $.ajax({type : "POST",
                url : "{{ url_for('feed') }}",
                data: JSON.stringify("like"),
                contentType: 'application/json;charset=UTF-8',
                async: false,
                cache: false,
                success: function () {
                    $.get("/feedcontent", function(picture) {
                    $("#content").html(picture);
                    });
                }
            });
        });
        $("#dislike").on("click", function(){
            $.ajax({type : "POST",
                url : "{{ url_for('feed') }}",
                data: JSON.stringify("dislike"),
                contentType: 'application/json;charset=UTF-8',
                async: false,
                cache: false,
                success: function () {
                    $.get("/feedcontent", function(picture) {
                    $("#content").html(picture);
                    });
                }
            });
        });
        $("#ongepast").on("click", function(){
            $.ajax({type : "POST",
                url : "{{ url_for('feed') }}",
                data: JSON.stringify("ongepast"),
                contentType: 'application/json;charset=UTF-8',
                async: false,
                cache: false,
                success: function () {
                    $.get("/feedcontent", function(picture) {
                    $("#content").html(picture);
                    });
                }
            });
        });
        $("#volg").on("click", function(){
            $.ajax({type : "POST",
                url : "{{ url_for('feed') }}",
                data: JSON.stringify("volg"),
                contentType: 'application/json;charset=UTF-8',
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
                        async: false,
                        cache: false,
                        success: function () {
                            $.get("/feedcontent", function(picture) {
                            $("#content").html(picture);
                                });
                        }
                     });
                }
                if (e.keyCode == '39'){
                    console.log("right");
                    $.ajax({type : "POST",
                        url : "{{ url_for('feed') }}",
                        data: JSON.stringify("like"),
                        contentType: 'application/json;charset=UTF-8',
                        async: false,
                        cache: false,
                        success: function () {
                            $.get("/feedcontent", function(picture) {
                            $("#content").html(picture);
                            });
                        }
                    });
                }
        }
    });