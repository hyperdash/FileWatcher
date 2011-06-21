chrome.tabs.onCreated.addListener(function(newTab) {
	var lsutils = new LocalStorageUtil('urls');
	var matched = false;
	lsutils.each(function(key, value) {
		if (matched == true) return;
		var searchStr = value.pattern;
		if (value.regex == 'true') searchStr = new RegExp(value.pattern, 'ig');
		if (newTab.url.search(searchStr) >= 0) {
			matched = true;
		}
	});
	if (!matched) return;

	chrome.windows.getAll({ 'populate': true }, function(windows) {
		for (var m in windows) {
			if (windows[m].type != 'normal') continue;

			var tabs = windows[m].tabs;
			for (var n in tabs) {
				var tab = tabs[n];
				if (tab.url.length != newTab.url.length || tab.id == newTab.id) continue;
				if (tab.url == newTab.url) {
					chrome.tabs.remove(newTab.id);
					chrome.tabs.update(tab.id, {url: tab.url, selected: true });
					break;
				}
			}
		}
	});
});