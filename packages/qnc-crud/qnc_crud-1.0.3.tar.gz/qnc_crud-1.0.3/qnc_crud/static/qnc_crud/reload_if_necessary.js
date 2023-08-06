'use strict';
/*
    This script should be added to your template via qnc_crud/reload_if_necessary.html (which sets a timestamp on the script element)
    See that file for a description of the effects of this script.
*/
(function() {
    // Any time user POSTs a form, update local storage so that we know data might have changed
    // This value will be accessible in all windows/tabs
    addEventListener('submit', function(e) {
        if (e.target.method == 'post') {
            localStorage.last_form_post = Date.now();
        }
    });

    function reload_if_necessary() {
        var last_update = localStorage.last_form_post;
        if (!last_update) return

        var rendered = document.getElementById('reload_if_necessary_script').getAttribute('data-rendered');
        if (rendered > last_update) return // page is not stale

        document.body.innerHTML = '';
        window.location.reload();
    }
    
    // if page was loaded from http cache, might be stale
    reload_if_necessary();
    // if page was loaded from "bf cache", might be stale
    addEventListener('pageshow', reload_if_necessary);


    // Reminder - storage events are NOT fired in the window where localStorage was updated - they are fired in all OTHER windows
    var other_window_posted_form_since_load = false;
    addEventListener('storage', function(e) {
        // Note - we DON'T reload immediately - no sense in reloading windows the user might never look at again
        // Also, this could cause issues if currently unfocused windows have unload/beforeunload listeners
        if (e.key == 'last_form_post') {
            other_window_posted_form_since_load = true;
        }
    });
    function reload_if_updated_from_other_window() {
        if (other_window_posted_form_since_load) location.reload();
    }
    // if another tab was in foreground and user clicked back to this tab, might be stale
    document.addEventListener('visibilitychange', reload_if_updated_from_other_window);
    // if user had multiple windows open and navigated back to this one, might be stale
    addEventListener('focus', reload_if_updated_from_other_window);
})();