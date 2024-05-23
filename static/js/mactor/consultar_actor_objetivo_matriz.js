
// Obtiene la descripcion del actor u objetivo seleccionado

    $(document).ready(function () {
        $("input").click(function () {

            var name = $(this).attr("name");

            if(name!=undefined)
            {
                   if (name.indexOf("actor")!= -1)
                    {
                        name = name.substring(5);
                        $.ajax
                        ({
                            data: {'id': name},
                            url: 'consultar_actor',
                            type: 'get',
                            success: function (data) {
                                var object = JSON.parse(data);
                                var html = "";
                                if(object.descripcion != "")
                                {
                                   html = "<p>" + 'Nombre Corto:' + "</p><p>" + object.nombreCorto
                                    + "</p><br><p>" + 'Nombre Largo:' + "</p><p>" + object.nombreLargo
                                    + "</p><br><p>" + 'Descripción:' + "</p><p>" + object.descripcion + "</p><p>";
                                }
                                else
                                {
                                  html = "<p>" + 'Nombre Corto:' + "</p><p>" + object.nombreCorto
                                    + "</p><br><p>" + 'Nombre Largo:' + "</p><p>" + object.nombreLargo
                                    + "</p><p>";
                                }
                                $('#mod_body_actor').html(html);
                            }
                        });
                    }
                    // si se pulsa el input de un objetivo
                    else if(name.indexOf("objetivo")!= -1)
                        {
                            name = name.substring(8);

                            $.ajax
                            ({
                                data: {'id': name},
                                url: 'consultar_objetivo',
                                type: 'get',
                                success: function (data) {
                                    var object = JSON.parse(data);
                                    var html = "";
                                    if(object.descripcion != "")
                                    {
                                       html = "<p>" + 'Nombre Corto:' + "</p><p>" + object.nombreCorto
                                        + "</p><br><p>" + 'Nombre Largo:' + "</p><p>" + object.nombreLargo
                                        + "</p><br><p>" + 'Descripción:' + "</p><p>" + object.descripcion + "</p><p>";
                                    }
                                    else
                                    {
                                      html = "<p>" + 'Nombre Corto:' + "</p><p>" + object.nombreCorto
                                        + "</p><br><p>" + 'Nombre Largo:' + "</p><p>" + object.nombreLargo
                                        + "</p><p>";
                                    }
                                    $('#mod_body_objetivo').html(html);
                                    }
                                });

                        }
            }

        });
    });


