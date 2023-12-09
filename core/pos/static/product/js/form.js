
$(function () {

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $("#id_costo_total, #id_precio_venta").prop('readonly', true);

    function calcularTotal() {
            // Obtener los valores de los inputs
            var costoM2 = parseFloat($("#id_costo_m2").val()) || 0;
            var costoColocacion = parseFloat($("#id_costo_colocacion").val()) || 0;
            var costoFlete = parseFloat($("#id_costo_flete").val()) || 0;
            var otrosCostos = parseFloat($("#id_otros_costos").val()) || 0;
            var gananciaEstimada = parseFloat($("#id_ganancia_estimada").val()) || 0;

            // Calcular el total del costo;
            var total = costoColocacion + costoFlete + otrosCostos + costoM2;

            // Calculo de Ganancia
            var total_ganancia = total * gananciaEstimada / 100 + total;

            // Mostrar el total en el elemento con ID "total"
            $("#id_costo_total").val(total.toFixed(2));

            // Muestrar precio de venta total
            $("#id_precio_venta").val(total_ganancia.toFixed(2));
        }

        // Llamar a la función al cambiar cualquiera de los tres inputs
        $("#id_costo_colocacion, #id_costo_flete, #id_otros_costos, #id_costo_m2, #id_ganancia_estimada")
        .on("input", calcularTotal);
});