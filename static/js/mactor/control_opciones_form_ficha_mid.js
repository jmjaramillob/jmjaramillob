/*permite que al seleccionar una opcion en el primer select, en el segundo solo se muestren activas aquellas que
aun no se han registrado. Esto para los formularios de fichas de estrategias */

$('#id_idActorY').on('change', Desactivar);
        function  Desactivar()
        {
            // se obtiene el id del actor
            var id = $(this).val();
            // se envian mediante ajax los parametros
            $.ajax({
                data : {'id' : id},
                url : 'ficha-ajax',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);

                    // determina cuales optiones deben ser visualizados (los no registrados)
                    for (var j=0;j<object.lista.length; j++)
                    {
                        // esconde las opciones correspondientes a las influencias registradas
                        var option = $("#id_idActorX").find("option[value='"+object.lista[j]+"']");
                        option.prop("hidden",true);

                    }
                    // se activa el segundo select
                        document.getElementById("id_idActorX").disabled = false;
                }
            });
        }





