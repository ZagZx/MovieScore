import Swal from "sweetalert2";

export const alert = Swal.mixin({
    // buttonsStyling: false,
    customClass: {
        // container: "!bg-background",
        title: "!text-foreground",
        htmlContainer: "!text-foreground-muted",
        popup: "!bg-background",
        confirmButton: "!bg-primary hover:!bg-primary-hover !text-primary-foreground",
        cancelButton: "!bg-secondary hover:!bg-secondary-hover !text-secondary-foreground"
    }
})