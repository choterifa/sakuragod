function buscarClientes() {
    var input, filter, table, tr, td, i, j, txtValue;
    input = document.getElementById("buscarInput");
    filter = input.value.toLowerCase();
    table = document.getElementById("clientesTabla");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        tr[i].style.display = "none";  // Oculta la fila inicialmente
        td = tr[i].getElementsByTagName("td");
        for (j = 0; j < td.length; j++) {
            if (td[j]) {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toLowerCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";  // Muestra la fila si se encuentra el texto
                    break;  // Si se encuentra una coincidencia, no es necesario seguir verificando las otras celdas
                }
            }
        }
    }
}