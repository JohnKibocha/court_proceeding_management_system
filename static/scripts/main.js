
// Toast messages logic
class Toast {
    constructor(message) {
        this.message = message;
    }

    show() {
        const toast = document.createElement('div');
        toast.textContent = this.message;
        toast.className = 'toast';
        document.body.appendChild(toast);

        setTimeout(() => {
            document.body.removeChild(toast);
        }, 3000);
    }
}

// Confirm Dialogs
// delete
function confirmDeleteDialog(event, url) {
    // Prevent the default action from occurring
    event.preventDefault();

    swal({
        title: "Are you sure?",
        text: "Once deleted, you will not be able to reverse this action!",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                window.location.href = url;
            } else {
                swal({
                    title: "Your action was cancelled!", icon: "info",
                });
            }
        });
}

// update
function confirmUpdateDialog(event, url) {
    // Prevent the default action from occurring
    event.preventDefault();

    swal({
        title: "Are you sure?",
        text: "Once updated, you will not be able to reverse this action!",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willUpdate) => {
            if (willUpdate) {
                window.location.href = url;
            } else {
                swal({
                    title: "Your action was cancelled!", icon: "info",
                });
            }
        });
}

// Logout
function confirmLogoutDialog(event, url) {
    // Prevent the default action from occurring
    event.preventDefault();

    swal({
        title: "Are you sure?", text: "You are about to logout!", icon: "warning", buttons: true, dangerMode: true,
    })
        .then((willLogout) => {
            if (willLogout) {
                window.location.href = url;
            } else {
                swal({
                    title: "You are still logged in!", icon: "info",
                });
            }
        });
}

// Default
function confirmDialog(event, url, message) {
    // Prevent the default action from occurring
    event.preventDefault();

    swal({
        title: "Are you sure?", text: message, icon: "warning", buttons: true, dangerMode: true,
    })
        .then((willConfirm) => {
            if (willConfirm) {
                window.location.href = url;
            } else {
                swal({
                    title: "Your action was cancelled!", icon: "info",
                });
            }
        });
}

// Other Dialogs
// warning dialogs
function warningDialog(message) {
    swal({
        title: "Warning!", text: message, icon: "warning", button: "Ok",
    });
}

// error
function errorDialog(message) {
    swal({
        title: "Sorry!", text: message, icon: "error", button: "Ok",
    });
}

// success
function successDialog(message) {
    swal({
        title: "Success!", text: message, icon: "success", button: "Ok",
    });
}

// info
function infoDialog(message) {
    swal({
        title: "Info!", text: message, icon: "info", button: "Ok",
    });
}


