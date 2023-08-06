/*
    reload_restoration.js

    Reload the state of various interactive elements when a page is reloaded (ie. upon back/forward navigation, location.reload(), etc.).

    Note that this has no effect when a page is loaded from an in-memory "bfcache". If such caches become ubiqitous, and cache enough history entries, then it may be worth dropping this script.

    Note that we save page document state incrementally, as the user interacts with page elements. It might be easier to put the entire saving process into a single unload listener, but that would break bfcache.

    This script relies on the js history api (specifically, history.state). We follow a "cooperative" pattern of modifying history.state, where we assume it's always an object, and we only update the "qnc_reload_data" key (we never replace the entire object). This will work alongside other scripts which use history.state, assuming they also follow this cooperative pattern.
*/
(function() {
    // helper functions
    function set_boolean_attribute(element, attribute, val) {
        if (val) {
            element.setAttribute(attribute, '');
        }
        else {
            element.removeAttribute(attribute);
        }
    }
    function _get_id(element) {
        return element.id;
    }
    function get_id_set(selector) {
        // Given a selector, get ids of all elements matching the selector
        return new Set([].map.call(document.querySelectorAll(selector), _get_id));
    }
    function get_reload_property(name) {
        return history.state.qnc_reload_data[name];
    }
    function set_reload_property(name, value) {
        // Note - by the time this is called, we expect history.state to be an object with qnc_reload_data set
        // If not, some other script is manipulating history.state in an uncooperative way
        s = history.state;
        s.qnc_reload_data[name] = value;
        history.replaceState(s, '', '');
    }

    // restore state when reloading page
    if (history.state && 'qnc_reload_data' in history.state) {
        var reload_data = history.state.qnc_reload_data;

        [].map.call(document.querySelectorAll('details[id]'), function(e) {
            set_boolean_attribute(e, 'open', reload_data.open_details_ids.has(e.id));
        });
    }

    // Save page state (once document is fully loaded)
    window.addEventListener('load', function() {
        var reload_data = {};

        reload_data.open_details_ids = get_id_set('details[id][open]');

        var s = history.state || {};
        s.qnc_reload_data = reload_data;
        history.replaceState(s, '', '');
    });

    // Incremental updates -> save state as mutations occur
    // (Reminder - many of these functions would be easier to achieve in a single unload listener, but that would break bfcache)
    document.addEventListener('toggle', function(e) {
        set_reload_property('open_details_ids', get_id_set('details[id][open]'));
    }, true);
})();