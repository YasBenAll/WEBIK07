    function bigImg(img) {
      img.style.height = 1.5*img.naturalHeight.toString() + "px";
      img.style.width = 1.5*img.naturalWidth.toString() + "px";
    }

    function normalImg(img) {
      img.style.height = img.naturalHeight.toString() + "px";
      img.style.width = img.naturalWidth.toString() + "px";
    }

    function sendData(giphname, description) {
        var giphData = { name: giphname, id: "send_giphy", description: description}
        $.ajax({type : "POST",
            url : "{{ url_for('upload') }}",
            data: JSON.stringify(giphData),
            contentType: 'application/json;charset=UTF-8'
        });
        window.location.replace(" {{ url_for('feed') }}")
    }