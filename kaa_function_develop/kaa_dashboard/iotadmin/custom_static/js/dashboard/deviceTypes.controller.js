angular
	.module('app.dashboard')
	.controller('DeviceTypesController', DeviceTypesController);

DeviceTypesController.$inject = [
	'$scope',
	'app.dashboard.route',
	'localStorage.service',
	'$location',
	'dashboard.service',
	'$route',
	'$timeout',
	'modal.service'
];

function DeviceTypesController(
	$scope,
	route,
	localStorage,
	$location,
	dashboardService,
	$route,
	$timeout,
	modalService
) {

	const getDeviceTypes = async function() {
		try {
			$scope.failed = false;
			let { data, headers, status } = await dashboardService.getDeviceTypes($scope.user.token);
			$scope.deviceTypes = data;
			$scope.$apply();
		} catch (err) {
			let { data, status } = err;

			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
			$scope.$apply();
		}
	};

	$scope.$on('$routeChangeSuccess',function(){
		getDeviceTypes();
	});

}
