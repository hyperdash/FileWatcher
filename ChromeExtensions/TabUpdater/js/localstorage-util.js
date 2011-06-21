LocalStorageUtil = function(namespace, separator) {
	switch (arguments.length) {
		case 1: separator = '.';
		case 0: namespace = null;
	}
	this._separator = separator;
	this._namespace = namespace;
};

LocalStorageUtil.prototype = {
	set: function(key, obj) {
		if (this._namespace != null) key = this._namespace + this._separator + key;
		localStorage.setItem(key, JSON.stringify(obj));
	},
	get: function(key) {
		if (this._namespace != null) key = this._namespace + this._separator + key;
		return JSON.parse(localStorage.getItem(key));
	},
	remove: function(key) {
		if (this._namespace != null) key = this._namespace + this._separator + key;
		localStorage.removeItem(key);
	},
	key: function (key) {
		if (this._namespace == null) return key;
		return key.replace(this._namespace + this._separator, '');
	},
	each: function(func) {
		var u = new LocalStorageUtil();
		for (var i = 0; i < localStorage.length; i++) {
			var k = localStorage.key(i);
			if (this._namespace != null && k.indexOf(this._namespace) != 0) continue;
			func(this.key(k), u.get(k));
		}
	}
};