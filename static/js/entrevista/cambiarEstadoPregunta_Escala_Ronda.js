/**
 * Created by Win 10 on 25/01/2019.
 */

// Cambia el estado de una pregunta, opcion de la escala o ronda del estudio haciendo clic en el icono.

    $(document).ready(function () {
        // para la tabla de preguntas
        $('#tabla_preguntas').on('click', 'a', function () {
            var id = $(this).attr("id");
            if(id != undefined)
            {
                if(id.indexOf("pregunta")!= -1)
                {
                    id = id.substring(8);
                    $.ajax(
                        {
                            data: {'id': id, 'tipo': 'pregunta'},
                            url: 'cambiar_estado',
                            type: 'get',
                            success: function (data)
                            {
                                var object = JSON.parse(data);

                                if(object.error){
                                    alert("No se pudo cambiar el estado de la pregunta");
                                }
                                else{
                                    location.reload(true);
                                }

                            }
                        });
                }
            }
        });
        // para la escala de likert
        $('#tabla_escala').on('click', 'a', function () {
            var id = $(this).attr("id");
            if(id != undefined)
            {
                if(id.indexOf("escala")!= -1)
                {
                    id = id.substring(6);
                    $.ajax(
                        {
                            data: {'id': id, 'tipo': 'escala'},
                            url: 'cambiar_estado',
                            type: 'get',
                            success: function (data)
                            {
                                var object = JSON.parse(data);

                                if(object.error){
                                    alert("No se pudo cambiar el estado de la opción de la escala");
                                }
                                else{
                                    location.reload(true);
                                }
                            }
                        });
                }
            }
        });
        // para la tabla de rondas
        $('#tabla_rondas').on('click', 'a', function () {
            var id = $(this).attr("id");
            if(id != undefined)
            {
                if(id.indexOf("ronda")!= -1)
                {
                    id = id.substring(5);
                    $.ajax(
                        {
                            data: {'id': id, 'tipo': 'ronda'},
                            url: 'cambiar_estado',
                            type: 'get',
                            success: function (data)
                            {
                                var object = JSON.parse(data);

                                if(object.error){
                                    alert("No se pudo cambiar el estado de la ronda");
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




