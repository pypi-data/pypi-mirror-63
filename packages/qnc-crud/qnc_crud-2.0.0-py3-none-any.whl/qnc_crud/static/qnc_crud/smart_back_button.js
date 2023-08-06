/*
    smart_back_button.js

    This script does two things:
        - provide can_go_back() test function
        - enables the creation of a "Back" button which includes the title of the previous page (and only appears when the user can actually go back in history).

    If you want to use the second feature, you must include this script on pages which render the back button (via [data-smart-back-button]), AND on any page which links to such a page.

    This script should be deferred (so that [data-smart-back-button] elements are ready).
*/

// Save title in session storage, so next page can use in back button
// Wait until load, in case any other js sets title dynamically
addEventListener('load', function() {
    var dtm = JSON.parse(sessionStorage['document_title_map'] || '{}');
    dtm[location.href.split('#')[0]] = document.title;
    sessionStorage['document_title_map'] = JSON.stringify(dtm);
});

// Show smart back button (immediately - don't wait for load)
// Only works if page can actually go back and previous page was same domain (and ran this script)
// Otherwise, back button will remain hidden
(function() {

    /* 
        Chrome bug/weird behaviour work around
        In various scenarios, Chrome changes document.referrer unexpectedly (perhaps other browsers, too)
        Ie. Page A -> Page B -> location.reload() >> referrer is now B rather than A
        There are other scenarios, involving history.back, which are even weirder (only seem to happen after repeating same process twice)

        Note that this process manipulates/uses the history.state object
        Other code can still use the history.state object, but only if it takes a similar approach of using a serialized object, and not wiping out our keys
    */
    var s = history.state || {};
    if (!s.hasOwnProperty('original_referrer')) {
        s.original_referrer = document.referrer;
        history.replaceState(s, '', '');
    }
    function get_original_referrer() {
        return history.state.original_referrer;
    }

    /*
        Detect if history.back() will work

        Note that if you open A in new tab, then go to B, then go BACK to A, history.length will still be 2 (ie. A and B).
        You cannot use history.length directly to know if history.back() will work.
        We need to store history.length ONLY when the page first loads, NOT from the user going back in history.
    */    
    var s = history.state || {};
    if (!s.hasOwnProperty('original_history_length')) {
        s.original_history_length = history.length;
        history.replaceState(s, '', '');
    }
    function can_go_back() {
        return history.state.original_history_length > 1
    }
    function can_go_back_to_same_domain() {
        if (!can_go_back()) return false

        // Now make sure referrer is same domain
        var o = location.origin;
        var ref = history.state.original_referrer;
        return ref.substring(0, o.length) == o;
    }

    function show_smart_back_buttons() {
        // Catch the case where the user decided to open the link to this page in a new window
        if (!can_go_back()) return

        var dtm = JSON.parse(sessionStorage['document_title_map'] || '{}');
        var prev_title = dtm[get_original_referrer()];
        if (prev_title == undefined) return

        var buttons = document.querySelectorAll('[data-smart-back-button]');
        for (var i = buttons.length - 1; i >= 0; i--) {
            var b = buttons[i];
            b.style.display = '';
            var textContainer = b.querySelector('[data-smart-back-button-title]');
            if (textContainer) {
                textContainer.innerText = prev_title;
            }
        }
    }
    show_smart_back_buttons();

    // make utility functions available globally:
    window.SmartBackButton = {
        can_go_back: can_go_back,
        can_go_back_to_same_domain: can_go_back_to_same_domain,
    };
})();