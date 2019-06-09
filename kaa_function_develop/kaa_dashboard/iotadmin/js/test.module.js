angular.module('app.module1', [])
	.controller('Controller1', function($scope) {
		console.log('Controller1 OK');
	});

angular.module('app', ['app.module1']);