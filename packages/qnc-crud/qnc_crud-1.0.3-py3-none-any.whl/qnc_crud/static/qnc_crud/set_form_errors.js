function set_form_errors(form, form_errors, error_map) {
    /*
        form: a form element
        forms_errors: an ERROR_LIST of form-level errors
        error_map:
            maps an id to an ERROR_LIST
            error messages should be concatenated and put into element with that id
            any input(s) with aria-errormessage equal to that id should have aria-invalid set appropriately (true if error list is non-empty, false otherwise)

        ERROR_LIST: either a string, or array of strings

        Note - if you do not specify all error message containers in error_map, then we will not clear error messages that are not specified. You must call clear_form_errors() first, if you want to clear them.
    */

    function make_error_string(error_list) {
        if (Array.isArray(error_list)) return error_list.join('. ');
        return error_list
    }

    // Form-level errors
    var fe = form.querySelector('[data-form-errors]');
    if (fe) fe.innerText = make_error_string(form_errors);

    // Element-level errors
    for (var id in error_map) {
        if (!error_map.hasOwnProperty(id)) continue

        var errors = error_map[id];
        var e = document.getElementById(id);
        if (e) e.innerText = make_error_string(errors);

        var form_elements = document.querySelectorAll('[aria-errormessage="'+id+'"]');
        for (var i = form_elements.length - 1; i >= 0; i--) {
            form_elements[i].setAttribute('aria-invalid', errors.length ? 'true' : 'false');
        }
    }

    function get_item_to_focus() {
        if (document.activeElement && document.activeElement.form == form && document.activeElement.getAttribute('aria-invalid') == 'true') {
            return null;
        }
        // Notice - if you want form-level errors to be focused after submit, you should tabindex attribute
        // (you can set tabindex="-1" to prevent keyboard focus but still allow programmatic focus)
        if (fe && fe.getAttribute('tabindex') && fe.innerText.trim() != '') return fe;
        
        for (var i = 0; i < form.elements.length; i++) {
            if (form.elements[i].getAttribute('aria-invalid') == 'true') return form.elements[i];
        }
    }
    var x = get_item_to_focus();
    x && x.focus();
}
function clear_form_errors(form) {
    // form-level errors
    var fe = form.querySelector('data-form-errors');
    if (fe) fe.innerText = '';

    // element-level errors
    // Note - we don't use querySelectorAll, in case the page is using [form="form_id"] on inputs that are outside of the form in the DOM
    for (var i = form.elements.length - 1; i >= 0; i--) {
        var e = form.elements[i];
        e.setAttribute('aria-invalid', 'false');

        var error_container_id = e.getAttribute('aria-errormessage');
        if (!error_container_id) continue
        var error_container = document.getElementById(error_container_id);
        if (!error_container) continue
        error_container.innerText = ''; 
    }
}
