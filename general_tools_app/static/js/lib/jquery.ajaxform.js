(function($) {

function AjaxForm() {
	this.regional = []
	this.regional[''] = {
		msgSending: 'Sending...',
		msgSuccess: 'Success!',
		msgFail: 'Failed',
		msgRetry: 'Retrying'
	}
	this._defaults = {

	}

	$.extend(this._defaults, this.regional[''])
}

$.extend(AjaxForm.prototype, {
	markerClassName: 'hasAjaxForm',
	propertyName: 'ajaxForm',

	/* Override the default settings for all plugin instances.
	   @param  options  (object) the new settings to use as defaults
	   @return  (Plugin) this object */
	setDefaults: function(options) {
		$.extend(this._defaults, options || {})
		return this
	},

	/* Attach the plugin functionality.
	   @param  target   (element) the control to affect
	   @param  options  (object) the custom options for this instance */
	_attachPlugin: function(target, options) {
		target = $(target)

		if (target.hasClass(this.markerClassName)) {
			return
		}

		var inst = {options: $.extend({}, this._defaults)}

		target.addClass(this.markerClassName).
			data(this.propertyName, inst)
		
		// Add event handlers for the target element if applicable,
		// using namespace this.propertyName
		this._optionPlugin(target, options)
	},

	/* Retrieve or reconfigure the settings for a control.
	   @param  target   (element) the control to affect
	   @param  options  (object) the new options for this instance or
	                    (string) an individual property name
	   @param  value    (any) the individual property value (omit if options
	                    is an object or to retrieve the value of a setting)
	   @return  (any) if retrieving a value */
	_optionPlugin: function(target, options, value) {
		target = $(target)
		var inst = target.data(this.propertyName)

		if (!options || (typeof options == 'string' && value == null)) { // Get option
			var name = options
			options = (inst || {}).options
			return (options && name ? options[name] : options)
		}

		if (!target.hasClass(this.markerClassName)) {
			return
		}
		options = options || {}
		if (typeof options == 'string') {
			var name = options
			options = {}
			options[name] = value
		}

		$.extend(inst.options, options);
		// Update target element based on new options here
		// Run main functionality here, if applicable
	}
})

var plugin = $.ajaxform = new AjaxForm()
  ,	getters = []

/* Determine whether a method is a getter and doesn't permit chaining.
   @param  method     (string, optional) the method to run
   @param  otherArgs  ([], optional) any other arguments for the method
   @return  true if the method is a getter, false if not */
function isNotChained(method, otherArgs) {
	if (method == 'option' && (otherArgs.length == 0 ||
			(otherArgs.length == 1 && typeof otherArgs[0] == 'string'))) {
		return true
	}
	return $.inArray(method, getters) > -1
}

/* Attach the plugin functionality to a jQuery selection.
   @param  options  (object) the new settings to use for these instances (optional) or
                    (string) the method to run (optional)
   @return  (jQuery) for chaining further calls or
            (any) getter value */
$.fn.ajaxform = function (options) {
	var otherArgs = Array.prototype.slice.call(arguments, 1)

	if (isNotChained(options, otherArgs)) {
		return plugin['_' + options + 'Plugin'].apply(plugin, [this[0]].concat(otherArgs))
	}
	return this.each(function() {
		if (typeof options == 'string') {
			if (!plugin['_' + options + 'Plugin']) {
				throw 'Unknown method: ' + options
			}
			plugin['_' + options + 'Plugin'].apply(plugin, [this].concat(otherArgs))
		}
		else {
			plugin._attachPlugin(this, options || {})
		}
	});
}


})(jQuery);
