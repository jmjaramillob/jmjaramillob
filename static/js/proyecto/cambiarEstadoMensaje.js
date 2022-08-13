/**
 * Created by Win 10 on 2/11/2017.
 */

// Obtiene la descripcion del actor al pulsar el boton VER en la lista de actores

    $(document).ready(function () {
        $('#tabla_recibidos').on('click', 'a', function () {
            var id = $(this).attr("id");
            if(id != undefined)
            {
                if(id.indexOf("mensaje")!= -1)
                {
                    id = id.substring(7);
                    $.ajax(
                        {
                            data: {'id': id},
                            url: 'cambiar_estado_mensaje',
                            type: 'get',
                            success: function (data)
                            {
                                var object = JSON.parse(data);

                                if(object.error){
                                    alert("No se pudo cambiar el estado del mensaje");
                                }
                                else{
                                    location.reload(true);
                                }

                            }
                        });

                }
            }
        });
    });




