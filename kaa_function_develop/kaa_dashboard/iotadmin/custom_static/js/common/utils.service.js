angular
	.module('app')
	.factory('utils.service', utils);

utils.$inject = [
];

function utils() {
	return {
		toUnicode
	};

	function toUnicode(s) {
		var result = "";
	    for(var i = 0; i < s.length; i++){
	        result += "\\u" + ("000" + s[i].charCodeAt(0).toString(16)).substr(-4);
	    }
	    return result;
	}
}