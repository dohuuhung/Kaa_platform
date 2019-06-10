angular
	.module('app.dashboard')
	.controller('DevicesController', DevicesController);

DevicesController.$inject = [
	'$scope',
	'app.dashboard.route',
	'localStorage.service',
	'$location',
	'dashboard.service',
	'$route',
	'$timeout',
	'modal.service'
];

function DevicesController(
	$scope,
	route,
	localStorage,
	$location,
	dashboardService,
	$route,
	$timeout,
	modalService
) {

	const getDevices = async function() {
		try {
			$scope.failed = false;
			let { data, headers, status } = await dashboardService.getDevices($scope.user.token);
			$scope.devices = data;
			$scope.$apply();
		} catch (err) {
			let { data, status } = err;

			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
			$scope.$apply();
		}
	};

	$scope.deleteDevice = async function(device) {
		try {
			$scope.failed = false;
			let { data, headers, status } = await dashboardService.deleteDevice($scope.user.token, device.device_key_hash);
			$scope.success = 'Device has been deleted.';
			$scope.$apply();
			$timeout(() => {
				getDevices();
			}, 2000);
		} catch (err) {
			let { data, status } = err;

			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
			$scope.$apply();
		}
	}

	$scope.$on('$routeChangeSuccess',function(){
		getDevices();
	});

	$scope.openModalConfirmDelete = function(device) {
		modalService.open({
			target: device,
			action: 'Delete',
			doAction: $scope.deleteDevice,
			modalClass: 'danger',
			title: 'Confirm Delete Device',
			content: `Are you sure to delete device <b>${device.device_name}</b>?`
		});
	}

	$scope.showDevice = function(device) {
		$location.path('/devices/' + device.device_key_hash);
	}

}
