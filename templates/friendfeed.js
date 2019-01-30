        $(document).ready(function(){
            $("#like").on("click", function(){
                $.ajax({type : "POST",
                    url : "{{ url_for('feed') }}",
                    data: JSON.stringify("like"),
                    contentType: 'application/json;charset=UTF-8',
                    async: false,
                    cache: false,
                    success: function () {
                        $.get("/friendfeedcontent", function(picture) {
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
                        $.get("/friendfeedcontent", function(picture) {
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
                        $.get("/friendfeedcontent", function(picture) {
                        $("#content").html(picture);
                        });
                    }
                });
            });
        });


        document.onkeyup = checkKey;

        function checkKey(e) {

            e = e || window.event;

            $(document).ready(function(){
                if (e.keyCode == '37'){
                        $.ajax({type : "POST",
                            url : "{{ url_for('feed') }}",
                            data: JSON.stringify("like"),
                            contentType: 'application/json;charset=UTF-8',
                            async: false,
                            cache: false,
                            success: function () {
                                $.get("/friendfeedcontent", function(picture) {
                                $("#content").html(picture);
                                });
                            }
                        });
                }
                if (e.keyCode == '39'){
                        $.ajax({type : "POST",
                            url : "{{ url_for('feed') }}",
                            data: JSON.stringify("dislike"),
                            contentType: 'application/json;charset=UTF-8',
                            async: false,
                            cache: false,
                            success: function () {
                                $.get("/friendfeedcontent", function(picture) {
                                $("#content").html(picture);
                                });
                            }
                        });
                }
            });
        }