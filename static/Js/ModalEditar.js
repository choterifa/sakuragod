
//< !--Codigo para obtner los datos del fomr segun si id(Editar)-- >
const abrirModal = document.getElementById('abrirModal')
if (abrirModal) {
    abrirModal.addEventListener('show.bs.modal', event => {
        // Button that triggered the modal
        const button = event.relatedTarget
        //Obtneer los datos del 
        const id = button.getAttribute('data-bs-id')
        const name = button.getAttribute('data-bs-nombre')
        const compra = button.getAttribute('data-bs-compra')
        const venta = button.getAttribute('data-bs-venta')
        const existencias = button.getAttribute('data-bs-existencias')

        // Seleccionar los que se acutilzaran
        const modalNombre = abrirModal.querySelector('#nombre')
        const modalCompra = abrirModal.querySelector('#precio_compra')
        const modalVenta = abrirModal.querySelector('#precio_venta')
        const modalExistencias = abrirModal.querySelector('#existencias')

        // Acutualizar el modal con los datos.
        modalNombre.value = name
        modalCompra.value = compra
        modalVenta.value = venta
        modalExistencias.value = existencias

        //Titulo segun la funcion
        if (id) {
            abrirModal.querySelector('.modal-title').textContent = 'Editar Producto';
            //Enviar a editar
            abrirModal.querySelector('#taskForm').setAttribute('action', '{{ url_for("edit_task", id=0) }}'.replace('0', id));
        } else {
            abrirModal.querySelector('.modal-title').textContent = 'Agregar Producto';
        }
    })
}