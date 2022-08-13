/**
 * Created by Win 10 on 01/01/2020.
 */

// Importa ideas de un estudio lluvia de ideas o abaco de regnier

    $(document).ready(function () {
        $('#tabla_estudios_registrados').on('click', 'a', function () {
            var id = $(this).attr("id");
            var idEstudio = $('input[name="idEstudio"]').val();
            if(id != undefined)
            {
                if(id.indexOf("abaco")!= -1 || id.indexOf("brain")!= -1)
                {
                    $.ajax(
                        {
                            data: {'id': id, 'idEstudio': idEstudio},
                            url: 'importar_ideas',
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




