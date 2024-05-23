/**
 * Created by Win 10 on 27/05/2018.
 */

//Date picker
        $('#id_fecha_inicio').datepicker({
          autoclose: true,
          sideBySide: true,
          format: 'dd/mm/yyyy',
          startDate: '{{ hoy|date:"d/m/Y"}}'
        });

        var fecha = '{{ fecha_ultima_ronda|date:"d/m/Y"}}';

        $('#id_fecha_final').datepicker({
          autoclose: true,
          sideBySide: true,
          format: 'dd/mm/yyyy',
          startDate: '{{ hoy|date:"d/m/Y"}}'
        });
