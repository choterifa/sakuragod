//< !--Codigo para obtner los datos del fomr segun si id(Editar)-- >
const abrirModal = document.getElementById('abrirModal')
if (abrirModal) {
    abrirModal.addEventListener('show.bs.modal', event => {
        // Button that triggered the modal
        const button = event.relatedTarget
        //Obtneer los datos del boton con los id
        const id = button.getAttribute('data-bs-id')
        const name = button.getAttribute('data-bs-nombre')
        const compra = button.getAttribute('data-bs-compra')
        const venta = button.getAttribute('data-bs-venta')
        const ganancia = button.getAttribute('data-bs-ganancia')
        const existencias = button.getAttribute('data-bs-existencias')
        const existencias_deseadas = button.getAttribute('data-bs-existencias-deseadas')
        const proveedor = button.getAttribute('data-bs-proveedor')
        const categoria = button.getAttribute('data-bs-categoria')

        // Seleccionar los id para actulizarlos en el modal
        const modalNombre = abrirModal.querySelector('#nombre')
        const modalCompra = abrirModal.querySelector('#precio_compra')
        const modalVenta = abrirModal.querySelector('#precio_venta')
        const modalGanancia = abrirModal.querySelector('#ganancia')
        const modalExistencias = abrirModal.querySelector('#existencias')
        const modalExistencias_deseadas = abrirModal.querySelector('#existencias_deseadas')
        const modalProveedor = abrirModal.querySelector('#proveedor')
        const modalCategoria = abrirModal.querySelector('#categoria')

        // Acutualizar el modal con los datos de los atributos.
        modalNombre.value = name
        modalCompra.value = compra
        modalVenta.value = venta
        modalGanancia.value = ganancia
        modalExistencias.value = existencias
        modalExistencias_deseadas.value = existencias_deseadas
        modalProveedor.value = proveedor
        modalCategoria.value = categoria

        //Titulo segun la funcion
        if (id) {
            abrirModal.querySelector('.modal-title').textContent = 'Editar Producto';
            console.log(id)
            abrirModal.querySelector('#taskForm').setAttribute('action', '{{ url_for("editar_producto", id=0) }}'.replace('0', id));
            //Enviar a editar
        } else {
            abrirModal.querySelector('.modal-title').textContent = 'Agregar Producto';
        }
    })
}