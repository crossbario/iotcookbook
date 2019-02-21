(function() {
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    ctx.strokeStyle = "#FF0000";
    ctx.lineWidth = 2;


    function connect() {
        var connection = new autobahn.Connection({url: 'ws://127.0.0.1:8080/ws', realm: 'realm1'});
        connection.onopen = function (session) {
            function onframe(args) {
            var image = new Image();
            image.onload = function() {
                ctx.drawImage(image, 0, 0);
            }
            image.src = "data:image/jpg;base64," + args[0].substring(1);
        }

        function onfaces(args) {
            for (var i = 0; i < args[0].length; i++) {
                face = args[0][i];
                ctx.strokeRect(face[0], face[1], face[2], face[3]);
            }
        }

        session.subscribe('io.crossbar.demo.frames', onframe);
        session.subscribe('io.crossbar.demo.faces', onfaces);
    };

    connection.open();

}

connect();

})()
