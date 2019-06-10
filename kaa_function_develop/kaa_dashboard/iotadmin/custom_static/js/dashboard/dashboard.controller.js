angular
	.module('app.dashboard')
	.controller('DashboardController', DashboardController);

DashboardController.$inject = [
	'$scope',
	'app.dashboard.route',
	'localStorage.service',
	'$location',
];

function DashboardController(
	$scope,
	route,
	localStorage,
	$location
) {

	$scope.route = route;

	init();

	function init() {
		getUser();
	}

	function getUser() {
		let user = localStorage.getObject('user');
		if (!user) {
			$location.url('/login');
		}
		$scope.user = user;
	}

	$scope.logout = function() {
		localStorage.setObject('user', undefined);
		$location.path('/login');
	}

	$scope.active = function(route) {
		return $location.path().split('/')[1] == route ? 'active' : '';
	}
}
