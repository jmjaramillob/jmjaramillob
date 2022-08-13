/**
 * Created by Win 10 on 01/01/2020.
 */

// Importa los objetivos de un estudio mactor disponible en el banco de estudios

    $(document).ready(function () {
        $('#tabla_estudios_registrados').on('click', 'a', function () {
            var id = $(this).attr("id");
            var idEstudio = $('input[name="idEstudio"]').val();
            if(id != undefined)
            {
                if(id.indexOf("mactor")!= -1)
                {
                    id = id.substring(6);
                    $.ajax(
                        {
                            data: {'id': id, 'idEstudio': idEstudio},
                            url: 'importar_objetivos',
                            type: 'get',
                            success: function (data)
                            {
                                var object = JSON.parse(data);
                                if(object){
                                    location.reload(true);
                                }
                            }
                        });

                }
            }
        });
    });




