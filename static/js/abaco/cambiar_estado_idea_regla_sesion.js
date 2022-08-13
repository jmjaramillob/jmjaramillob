/**
 * Created by Win 10 on 28/01/2019.
 */

// Cambia el estado de una idea o sesión al dar clic en el icono que representa esta cualidad.

    $(document).ready(function () {
        // para la tabla de todas las ideas
        $('#tabla_ideas').on('click', 'a', function () {
            var id = $(this).attr("id");
            if(id != undefined)
            {
                if(id.indexOf("idea")!= -1)
                {
                    id = id.substring(4);
                    $.ajax(
                        {
                            data: {'id': id, 'tipo': 'idea'},
                            url: 'cambiar_estado',
                            type: 'get',
                            success: function (data)
                            {
                                var object = JSON.parse(data);

                                if(object.error){
                                    alert("No se pudo cambiar el estado de la idea");
                                }
                                else{
                                    location.reload(true);
                                }

                            }
                        });
                }
            }
        });
        // para la tabla de las ideas a evaluar
        $('#tabla_ideas_evaluacion').on('click', 'a', function () {
            var id = $(this).attr("id");
            if(id != undefined)
            {
                if(id.indexOf("idea")!= -1)
                {
                    id = id.substring(4);
                    $.ajax(
                        {
                            data: {'id': id, 'tipo': 'idea'},
                            url: 'cambiar_estado',
                            type: 'get',
                            success: function (data)
                            {
                                var object = JSON.parse(data);

                                if(object.error){
                                    alert("No se pudo cambiar el estado de la idea");
                                }
                                else{
                                    location.reload(true);
                                }

                            }
                        });
                }
            }
        });
        // para la tabla de las ideas que ha creado el usuario
        $('#tabla_mis_ideas').on('click', 'a', function () {
            var id = $(this).attr("id");
            if(id != undefined)
            {
                if(id.indexOf("idea")!= -1)
                {
                    id = id.substring(4);
                    $.ajax(
                        {
                            data: {'id': id, 'tipo': 'idea'},
                            url: 'cambiar_estado',
                            type: 'get',
                            success: function (data)
                            {
                                var object = JSON.parse(data);

                                if(object.error){
                                    alert("No se pudo cambiar el estado de la idea");
                                }
                                else{
                                    location.reload(true);
                                }

                            }
                        });
                }
            }
        });
        // para la tabla de reglas
        $('#tabla_reglas').on('click', 'a', function () {
            var id = $(this).attr("id");
            if(id != undefined)
            {
                if(id.indexOf("regla")!= -1)
                {
                    id = id.substring(5);
                    $.ajax(
                        {
                            data: {'id': id, 'tipo': 'regla'},
                            url: 'cambiar_estado',
                            type: 'get',
                            success: function (data)
                            {
                                var object = JSON.parse(data);

                                if(object.error){
                                    alert("No se pudo cambiar el estado de la sesión");
                                }
                                else{
                                    location.reload(true);
                                }
                            }
                        });
                }
            }
        });
        // para la tabla de sesiones
        $('#tabla_sesiones').on('click', 'a', function () {
            var id = $(this).attr("id");
            if(id != undefined)
            {
                if(id.indexOf("sesion")!= -1)
                {
                    id = id.substring(6);
                    $.ajax(
                        {
                            data: {'id': id, 'tipo': 'sesion'},
                            url: 'cambiar_estado',
                            type: 'get',
                            success: function (data)
                            {
                                var object = JSON.parse(data);

                                if(object.error){
                                    alert("No se pudo cambiar el estado de la sesión");
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




