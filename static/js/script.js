function confirmDelete(id) {
    var confirmDelete = confirm("Are you sure you want to delete this record?");
    if (confirmDelete) {
        window.location.href = "/delete/" + id;
    }
}
