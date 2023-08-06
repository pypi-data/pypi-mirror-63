# qnc_crud

WORK IN PROGRESS

A rather opinionated framework to help create multi-page CRUD/form-heavy web apps. Comes with a collection of django and js utilities which can also be used in a more flexible way, without opting-in to the entire framework. 

Intended to be installed as an "app" in a django project, but also useful in other web projects just for the js files.

## No Full-Page Form Submissions
You should never use standard form submission (which loads a new page). Meaningless entries end up in browser history, page state is lost, file inputs are cleared if there are form errors. The list of issues is long.

ajax_all_forms.js automatically makes all of your forms submit via ajax, and executes the code returned by your server.

set_form_errors.js provides useful helper utilities for generating form error messages.

## Automatic Page Invalidation
reload_if_necessary.js will cause pages to reload automatically, if any form has been POSTED by the user (same browsing session) at some time after the page was initially rendered

This means the user can navigate back in history (after logging in/out, manipulating data, etc.), and the page will reload.
Also, the user can make changes in one window, and those changes will be reflected in another window as soon as the user focuses that window.

## Form Pages Removed From History
### Edit Forms Go Back
### Add Forms Replace Location

## Automatic Back Button


