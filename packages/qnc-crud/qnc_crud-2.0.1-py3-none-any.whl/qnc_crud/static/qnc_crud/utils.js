'use strict';
/*
    Some basic js utilities for behaviours/patterns that I've come across many times.
    
    All of the functionality in this file is "opt-in" via custom html attributes.
    You should be able to include it on every page of your site.

    NOTE - these helpers rely on jQuery!
    jQuery is mostly used for its delegated event listeners. 
    If we want to drop jQuery requirement, we could implement our function to implement this pattern (would be trivial if we polyfilled element.matches and element.closest). 

    TODO - we should probably change all of the data-* attributes to qnc-*
    I've started using qnc-* attributes for new features, but old ones still use data-*
*/


/*
    [data-link] -> make any element work like a link, as much as possible

    particulary useful on table rows

    use with tabindex="0"
    we also recommend setting draggable=true
    usage: <tr data-link="some_url/" tabindex="0" draggable></tr>

    Note: draggable makes text-selection impossible, so you may not want to set that attribute.
    Since we copy href on dragstart, though, it does enable useful "link-like" features:
        - drag link into text editor or email client
        - drag to url bar to open without referrer *
        - drag to tab bar to open in new tab *

        * chrome features, may or may not be implemented in other browsers
*/
$(document).on('click', '[data-link]', function(e) {
    // If they selected text in the "link", don't treat as a click
    if (getSelection() && !getSelection().isCollapsed) return
    // Only primary mouse button
    if (event.button != 0) return

    var url = this.getAttribute('data-link');
    if (e.metaKey || e.ctrlKey) {
        window.open(url, '_blank');
    }
    else {
        location = url;
    }
});
$(document).on('keypress', '[data-link]', function(e) {
    if (e.key != 'Enter') return

    // If they selected text in the "link", don't treat as a click
    if (getSelection() && !getSelection().isCollapsed) return
    var url = this.getAttribute('data-link');
    if (e.metaKey || e.ctrlKey) {
        window.open(url, '_blank');
    }
    else {
        location = url;
    }
});
// on drag, set data transfer to href of link
$(document).on('dragstart', '[data-link]', function(e) {
    var temp_link = document.createElement('a');
    temp_link.href = this.getAttribute('data-link');
    e.originalEvent.dataTransfer.setData('text', temp_link.href);
});


/*
    [data-relace-location] -> buttons that replace current history entry, rather than create a new one (like a link)
    
    Useful in multi-step forms/wizards, where you want to be able go "back" from any point to the page that launched the form

    Recommendation:
    If page A has a "replace link" to page B, then page B should have another "replace link" back to A (since the back button won't work).
*/
$(document).on('click', '[data-replace-location]', function(e) {
    // Before we call location.replace, update current url to our referrer
    // This is necessary for smart_back_button.js to work properly

    // resolve url relative to current page, before we update url
    var a = document.createElement('a');
    a.href = this.getAttribute('data-replace-location');
    var url = a.href;

    // try/catch, in case referrer is cross-origin
    try {
        history.replaceState(null, '', document.referrer);
    }
    catch (e) {}

    // replaceState is asynchronous, have to run in next iteration of run-loop for new page to have the updated referrer
    setTimeout(function() {
        location.replace(url);
    }, 0);
});

// [data-confirm] -> confirm before performing button actions
// Note that we attach handler on capturing phase, so that it runs as early as possible
document.addEventListener('click', function(e) {
    var $b = $(e.target).closest('[data-confirm-first]');
    if (!$b.length) return;

    if (!window.confirm($b[0].getAttribute('data-confirm-first'))) {
        e.preventDefault();
        e.stopPropagation();
    }
}, true);

// dynamically add row to formset (django)
// requires adding attributes to button, row template, row container/parent
$(document).on('click', '[data-add-row-to-formset]', function() {
    // Set this attribute to the form prefix on the add button
    var form_prefix = this.getAttribute('data-add-row-to-formset');
    // You have to add a template element (recommend <script type="text/template">)
    var $template = $('[data-formset-template="'+form_prefix+'"]');
    // You have to set this on the container of the formset forms 
    var $container = $('[data-formset-container="'+form_prefix+'"]');
    // This is an input in the management form
    var $form_count_input = $('#id_'+form_prefix+'-TOTAL_FORMS');

    $container.append($template.html().replace(/__prefix__/g, $form_count_input.val()));
    $form_count_input.val(1+parseInt($form_count_input.val()));
});

// for use with ajax_all_forms.js -------------------------------------------------------------------------------
// submit filter forms on any change
$(document).on('change', '[data-ajax-submit-on-change]', null, function(e) {
    ajax_submit_form(e.target.form);
});
// Some browsers don't trigger change event when pressing enter from text input, so listen to that, too
$(document).on('keyup', '[data-ajax-submit-on-change]', null, function(e) {
    if (e.key === 'Enter') {
        ajax_submit_form(e.target.form);
    }
});
// re-focus element (if it gets re-created) after form submission
(function() {
    var refocus_id = null;
    document.addEventListener('ajax_form_will_submit', function() {
        refocus_id = document.activeElement && document.activeElement.hasAttribute('qnc-ajax-form-refocus') && document.activeElement.id;
    });
    document.addEventListener('ajax_form_submission_complete', function() {
        var e = refocus_id && document.getElementById(refocus_id);
        e && e.focus();
    });
})();


/*
    Pop-ups/drop-downs

    Note - it might have made sense to implement this using the details element, but that has a couple issues:
        - screen reader support is still poor (even ChromeVox does a poor job)
        - not supported in IE, so polyfill is required
        - behaviour isn't quite the same as standard details element

    Required markup:
        - a button (or buttons) with qnc-popup-toggler="pop_up_id"
        - a container with qnc-popup="pop_up_id"

    What it does:
        - toggles aria-expanded on the toggle button
        - toggles display: none/block on the container
        - focuses first focusable element in popup upon open
        - closes popup when clicking outside of it
        - closes popup when moving focus outside of it
        - initializes pop-ups based on value of aria-expanded, assuming false if absent


    Note that this has no impact on the styles of elements, other than the display value of the popup container.
    We recommend using some class to set display: none; on your popup containers, to prevent them appearing for an instant at initial load. Ie:
        [qnc-popup] {display: none;}

    TODO: should we include qnc_crud_utils.css to go along with this?
    Or convert forms.css to a general qnc_crud.css?

*/
(function() {
    var open_pid = null;
    function set_open_pid(pid) {
        if (pid === open_pid) return
        open_pid = pid;

        if (pid === null) {
            $('[qnc-popup]').hide();
            $('[qnc-popup-toggler]').attr('aria-expanded', 'false');
        }
        else {
            $('[qnc-popup='+pid+']').show();
            $('[qnc-popup]:not([qnc-popup='+pid+'])').hide();
            $('[qnc-popup-toggler='+pid+']').attr('aria-expanded', 'true');
            $('[qnc-popup-toggler]:not([qnc-popup-toggler='+pid+'])').attr('aria-expanded', 'false');

            // Focus first focusable child
            var children = $('[qnc-popup='+pid+']').find('*');
            for (var i = 0; i < children.length; i++) {
                if (children[i].tabIndex >= 0) {
                    children[i].focus();
                    break;
                }
            }
        }
    }
    $(document).on('click', function(e) {
        // if they clicked in a pop-up, do nothing
        if ($(e.target).closest('[qnc-popup]').length > 0) return

        // if they did not click an open button, close any open pop-up
        var $open_button = $(e.target).closest('[qnc-popup-toggler]');
        if ($open_button.length == 0) {
            set_open_pid(null);
            return
        }

        // They did click an open button
        // TOGGLE the pop-up it controls, hide any other open one
        var pid = $open_button[0].getAttribute('qnc-popup-toggler');
        if (pid !== open_pid) {
            set_open_pid(pid);
        }
        else {
            set_open_pid(null);
        }
    });
    $(document).on('focusin', function(e) {
        // No pop-up open
        if (open_pid === null) return
        // Focus remained in pop-up
        if ($(e.target).closest('[qnc-popup]').length > 0) return

        // Close the pop-up
        // There MAY be a simultaneous click event, which also closes the pop-up
        // Let the click handler run first, then close (if still necessary)
        setTimeout(function() {
            set_open_pid(null);
        }, 0);
    });
    // Initialize pop-ups
    var _open = $('[qnc-popup-toggler][aria-expanded]').attr('[qnc-popup-toggler');
    set_open_pid(_open === undefined ? null : _open);
})();