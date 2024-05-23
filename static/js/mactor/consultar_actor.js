/**
 * Created by Win 10 on 2/11/2017.
 */

// Obtiene la descripcion del actor al pulsar el boton VER en la lista de actores

    $(document).ready(function () {
        $("a").click(function () {
            var id = $(this).attr("id");
            if(id != undefined)
            {
                $.ajax(
                    {
                        data: {'id': id},
                        url: 'consultar_actor',
                        type: 'get',
                        success: function (data)
                        {
                            var object = JSON.parse(data);
                            var html = "";
                            if(object.descripcion != "")
                            {
                                html = "<p>" + 'Nombre Corto:' + "</p><p>" + object.nombreCorto +
                                    "</p><br><p>" + 'Nombre Largo:' + "</p><p>" + object.nombreLargo +
                                    "</p><br><p>" + 'Descripción:' + "</p><p>" + object.descripcion + "</p><p>";
                            }
                            else
                            {
                               html = "<p>" + 'Nombre Corto:' + "</p><p>" + object.nombreCorto +
                                    "</p><br><p>" + 'Nombre Largo:' + "</p><p>" + object.nombreLargo +
                                    "</p><br><p>";
                            }
                            $('#mod_body_actor').html(html);
                        }
                    });
            }
        });
    });




