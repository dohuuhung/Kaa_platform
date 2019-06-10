angular
	.module('app.dashboard')
	.controller('DeviceTypeDetailController', DeviceTypeDetailController);

DeviceTypeDetailController.$inject = [
	'$scope',
	'app.dashboard.route',
	'localStorage.service',
	'$location',
	'dashboard.service',
	'$routeParams',
	'modal.service',
	'$timeout',
	'utils.service'
];

function DeviceTypeDetailController(
	$scope,
	route,
	localStorage,
	$location,
	dashboardService,
	$routeParams,
	modalService,
	$timeout,
	utils
) {

  $scope.deviceTypeToken = $routeParams.token;
	$scope.parametersMap = {};

	const getOverview = async function() {
		try {
			$scope.failed = false;
			
			let { data, headers, status } = await dashboardService.getDeviceTypeOverviews(
				$scope.user.token, $scope.deviceTypeToken);
			
			$scope.overview = data;

			$scope.$apply();
		} catch (err) {
      console.error(err);
			let { data, status } = err;
			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
      $scope.$apply();
		}
	};

	$scope.$on('$routeChangeSuccess',function(){
		getOverview();
	});

	$scope.currentTab = 'overviews';
	
	$scope.changeTab = function(tab) {
		$scope.currentTab = tab;

		if (tab == 'parameters') {
			$scope.getParameters();
		}
	};

	$scope.tabActive = function(tab) {
		return tab == $scope.currentTab ? 'active' : '';
	}

	$scope.getParameters = async function() {
		try {
			$scope.failed = false;
			
			let { data, headers, status } = await dashboardService.getDeviceTypeParameters(
				$scope.user.token, $scope.deviceTypeToken);
			
			$scope.parameters = data;
			$scope.$apply();
		} catch (err) {
      console.error(err);
			let { data, status } = err;
			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
      $scope.$apply();
		}
	}
}
