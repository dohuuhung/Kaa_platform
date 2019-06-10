angular
	.module('app', [
		'ngRoute',
		'app.dashboard',
		'app.auth',
		'ui.bootstrap',
		'ngSanitize'
	])
	.config(config)
	.constant('apiBase', 'http://52.15.81.21:2004/api/')
	.run(run);

config.$inject = [
	'$routeProvider',
	'$locationProvider'
];

function config($routeProvider, $locationProvider) {
	$locationProvider.html5Mode(true);
	$routeProvider
	.when('/', {
		templateUrl: 'templates/dashboard.html',
		controller: 'DashboardController',
	})
	.when('/login', {
		templateUrl: 'templates/login.html',
		controller: 'LoginController',
		css: 'custom_static/css/auth.css'
	})
	.when('/register', {
		templateUrl: 'templates/register.html',
		controller: 'RegisterController',
		css: 'custom_static/css/auth.css'
	})
	.when('/change_temporary_password', {
		templateUrl: 'templates/changeTempPassword.html',
		controller: 'LoginController',
		css: 'custom_static/css/auth.css'
	})
	.when('/users', {
		templateUrl: 'templates/users.html',
	})
	.when('/users/:userId', {
		templateUrl: 'templates/userProfile.html',
	})
	.when('/devices', {
		templateUrl: 'templates/devices.html',
	})
	.when('/devices/:device_key_hash', {
		templateUrl: 'templates/deviceDetail.html'
	})	
	.when('/device_types', {
		templateUrl: 'templates/deviceTypes.html',
	})
	.when('/device_types/:token', {
		templateUrl: 'templates/deviceTypeDetail.html'
	});
}

run.$inject = [];

function run() {
}

angular.module('app')
.directive('head', ['$rootScope','$compile',
    function($rootScope, $compile){
        return {
            restrict: 'E',
            link: function(scope, elem){
                var html = '<link rel="stylesheet" ng-repeat="(routeCtrl, cssUrl) in routeStyles" ng-href="{{cssUrl}}" />';
                elem.append($compile(html)(scope));
                scope.routeStyles = {};
                $rootScope.$on('$routeChangeStart', function (e, next, current) {
                    if(current && current.$$route && current.$$route.css){
                        if(!angular.isArray(current.$$route.css)){
                            current.$$route.css = [current.$$route.css];
                        }
                        angular.forEach(current.$$route.css, function(sheet){
                            delete scope.routeStyles[sheet];
                        });
                    }
                    if(next && next.$$route && next.$$route.css){
                        if(!angular.isArray(next.$$route.css)){
                            next.$$route.css = [next.$$route.css];
                        }
                        angular.forEach(next.$$route.css, function(sheet){
                            scope.routeStyles[sheet] = sheet;
                        });
                    }
                });
            }
        };
    }
]);