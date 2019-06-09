const childModules = [
	'ngRoute',
	'app.core',
	'app.devices',
];

angular
	.module('app', childModules)
	// .controller('AController', function($scope) {
	// 	$scope.init = function() {
	// 		console.log('OK AController');
	// 	};

	// 	$scope.init();
	// })
	.config(config)
	.run(run);

config.$inject = [
	'$locationProvider',
	'$routeProvider',
];

function config($locationProvider, $routeProvider, $window) {
	$locationProvider.html5Mode({
		enabled: true,
		requireBase: false,
	}).hashPrefix('!');
	
	$routeProvider
		.when('/', {
			templateUrl: '/devices_list.html'
		})
		.when('/devices/:id', {
	    	templateUrl: '/detail.html',
	    	controller: 'DeviceDetailController'
	    });

	// $routeProvider.otherwise({
	// 	template: '',
	// 	controller: 'RedirectController',
	// });
}

run.$inject = ['$route'];

function run($route) {
	console.log('Run app')
	$route.reload();
}

// test
// angular.module('test', [])
// 	.controller('TestController', function($scope) {
// 		$scope.init = function() {
// 			console.log('Hello')
// 		};
// 		$scope.init();
// 	})
// 	.run(function() {
// 		console.log('Run test');
// 	});
