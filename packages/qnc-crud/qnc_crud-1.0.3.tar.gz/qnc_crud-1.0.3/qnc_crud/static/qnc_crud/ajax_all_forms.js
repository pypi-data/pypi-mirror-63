/*
	ajax_all_forms.js

	Submit all forms via xhr (you can opt-out by adding "data-no-ajax-form" attribute to a given form).
	Action and method are specified, as usual, on the form element.

	The goal is to make the querystring/body of the request behave exactly as for a normal submission (with entype="multipart/form-data"). File uploads are supported. If you click a named submit button, it's name/value will be included in the data sent.

	Your server's xhr response should be the body of a js function, which will be executed.
	The "response function" is passed the form element as its sole argument.

	Additional form submissions while an xhr request is outstanding will always be ignored.
	Once the "response function" has completed, submissions will again be allowed.
	If the response function returns true, then no further submissions will handled (this is primarily useful if the response function causes a page navigation, and leaves the form in the DOM).

	Custom events are fired before submission and upon receipt of response.
	One use case for this is to restore focus state, if your "response function" destroys/recreates the focused element.

	A custom event is also fired for any non-200 response. Unless you handle this event (preventDefault()) we'll alert a basic error message to user.

	If the form has "data-ajax-form-replace-query" attribute, then every time the form is submitted we will use the history api to replace the query string with the data from the form. This is useful if you want to be able to restore the full page state after reload/back-forward/bookmark navigation. 
*/

// Polyfill CustomEvent constructor, courtesy of MDN
// https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent/CustomEvent#Polyfill
(function () {
  if ( typeof window.CustomEvent === "function" ) return false;
  function CustomEvent ( event, params ) {
    params = params || { bubbles: false, cancelable: false, detail: null };
    var evt = document.createEvent( 'CustomEvent' );
    evt.initCustomEvent( event, params.bubbles, params.cancelable, params.detail );
    return evt;
   }
  window.CustomEvent = CustomEvent;
})();

/*
	Normalize browser behaviour - when clicking a (named) submit button, focus it
	We rely on this to determine which button submitted the form (so we can serialize it's name/value)
	Most browsers already do this, some don't (Safari and Firefox on Mac).
	I'm not sure we should really be altering this behaviour, but it's easier than trying to track the "active button" separately.
	Note - listen on capturing phase, to run as early as possible.
*/
document.addEventListener('click', function(event) {
	function is_valid_submit_button(element) {
		return element.type == 'submit' && element.form && element.tabIndex >= 0
	}
	var c = event.target;
	while (!is_valid_submit_button(c) && c.parentElement) {
		c = c.parentElement;
	}
	if (!is_valid_submit_button(c)) return

	/* 
		Some browsers (ie. chrome) generate fake click events on the "default" submit button when pressing enter while an input is focused. 
		In this case, we do not want to move focus (focus should stay in input, so user can keep typing).
		These fake events have screenX and screenY of 0 (in Chrome, at least).
	*/
	if (!event.screenX && !event.screenY) return

	c.focus();
}, true);

// Note - this method can be called any time to submit a form
// If you call it manually, bear in mind that we'll still "lookup" the "active button" and submit that
// calling form.submit() does NOT cause any event listeners to be called
function ajax_submit_form(form) {
	// Note - this prevents the form from submitting while previous request is outstanding, but if the request completes and the response doesn't remove the form/navigate away, then the user is free to submit the form again
	if (form._is_ajax_submitting) return
	form._is_ajax_submitting = true;

	var submitting_button = document.activeElement && document.activeElement.form && document.activeElement.form == form && document.activeElement.type == 'submit' && document.activeElement;

	var method = ((submitting_button && submitting_button.getAttribute('formmethod')) || form.method).toLowerCase();
	var action = (submitting_button && submitting_button.getAttribute('formaction')) || form.action;

	function get_params() {
		var items = [];
		for (var i = form.elements.length - 1; i >= 0; i--) {
			var e = form.elements[i];
			if ((e.type == 'radio' || e.type == 'checkbox') && !e.checked) continue
			if (e.disabled) continue
			// button[type=button] elements should not be submitted
			if (e.type == 'button') continue
			// submit buttons should only be submitted if clicked
			if (e.type == 'submit' && e != submitting_button) continue
			if (!e.name) continue
			items.push(encodeURIComponent(e.name)+'='+encodeURIComponent(e.value));
		}
		return items.join('&');
	}

	if (form.hasAttribute('data-ajax-form-replace-query')) {
		history.replaceState(history.state, '', '?'+get_params());
	}

	// if GET, data needs to go in query string
	// else, it goes in body
	function get_action() {
		if (method != 'get') return action
		// Now we need to serialize form
		// Ideally, we'd use FormData just like get_body, and pass to URLSearchParams to serialize, but that's not supported in IE, so we have to serialize ourselves

		var params = get_params();

		// If the user is using data-ajax-form-replace-query, then they are probably serving different responses depending on whether or not it's an ajax request. The user can check the X-Requested-With header, but http caches don't VARY based on this header, by default. This can cause the ajax response to get cached and used when navigating back to the page. Therefore, we add a query param to distinguish between these two cases.
		// TODO - explain this better? Look for better alternative? Drop this practice entirely?
		if (form.hasAttribute('data-ajax-form-replace-query')) {
			if (params) {
				params += '&';
			}
			params += '_ajax_all_forms_submitted=true';
		}

		return action.split('?')[0] + '?' + params;
	}
	function get_body() {
		if (method == 'get') return

		var d = new FormData(form);
		/*
			If user clicked a submit button to submit the form, attach name/value
			Note - unlike some browsers, if the user submits the form by pressing enter from an input field, we do NOT try to determine the "default" submit button. 
			If you want to treat a button as default, you should handle that on the backend.
		*/
		if (submitting_button && submitting_button.name) {
			d.append(submitting_button.name, submitting_button.value);
		}
		return d;
	}

	form.dispatchEvent(new CustomEvent('ajax_form_will_submit', {bubbles: true}));

	var r = new XMLHttpRequest();
	r.open(method, get_action());
	// Most js libraries set this header. Helps server respond to ajax requests differently.
	r.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	r.onload = function(event) {
		form._is_ajax_submitting = false;

		if (r.status == 200) {
			// basically, we're "eval"-ing the response
			// This is more efficient, though
			// The response code will only have access to global scope, and the submitted form via "form"
			var f = new Function('form', r.responseText);

			// Note - returned function can return true to prevent further form submissions
			// You SHOULD do this whenever your response triggers a navigation, since those are asynchronous
			var prevent_further_submissions = Boolean(f(form));

			// hijack this flag for a second purpose, to prevent any more submissions
			// TODO - UI update? Remove form from DOM? I _think_ we should leave that up to users
			form._is_ajax_submitting = prevent_further_submissions;
		}
		else {
			// Fire custom event
			var e = new CustomEvent('ajax_form_error', {
				detail: r,
				bubbles: true,
				cancelable: true,
			});
			form.dispatchEvent(e);
			// If no one handles it, alert the user
			// TODO - handle 403 slightly differently?
			if (!e.defaultPrevented) {
				function get_message() {
					if (r.status == 403) {
						return 'Forbidden: ' + r.responseText;
					}
					return 'Error: ' + r.statusText;
				}
				alert(get_message());
			}
		}

		form.dispatchEvent(new CustomEvent('ajax_form_submission_complete', {bubbles: true}));
	}
	r.send(get_body());
}

// Note - we're attaching directly to window, so we should be one of the last listeners to run
// Other form submit listeners can either stopPropagation() or preventDefault() to stop us from submitting
addEventListener('submit', function(e) {
	// escape hatch so pages can use regular full-page form submission even when including this script
	if (e.target.hasAttribute('data-no-ajax-form')) return

	if (e.defaultPrevented) return

	e.preventDefault();
	ajax_submit_form(e.target);
});