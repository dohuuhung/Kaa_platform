angular
	.module('app')
	.factory('localStorage.service', localStorageService);

localStorageService.$inject = [
	'$window'
];

function localStorageService($window) {
	return {
		get: function(key) {
			return $window.localStorage[key];
		},
		set: function(key, value) {
			$window.localStorage[key] = value;
		},
		setObject: function(key, value) {
			$window.localStorage[key] = angular.toJson(value);
		},
		getObject: function(key, value) {
			return angular.fromJson($window.localStorage[key]);
		}
	}
}
