angular
	.module('app.devices')
	.controller('DevicesController', DevicesController);

DevicesController.$inject = [
	'app.devices.service',
	'localStorage.service',
	'$scope',
	'$location'
];

function DevicesController(
	deviceService,
	localStorageService,
	$scope,
	$location
) {
		
	var ctrl = this;

	$scope.init = function() {
		$scope.devices = [];
		$scope.deviceTypes = [];
		$scope.currentDeviceType = null;
		initDevicesTypes();
	}

	$scope.init();

	async function initDevicesTypes() {
		try {
			// Get device types
			$scope.deviceTypes = await deviceService.listDeviceTypes();
			$scope.deviceTypes = _formatDeviceTypes($scope.deviceTypes);
			if (!$scope.deviceTypes.length) return;

			// Get current device type
			let currentDeviceTypeId = localStorageService.get('currentDeviceTypeId');
			let currentDeviceType = $scope.deviceTypes.find(
				device => device.device_type_id === currentDeviceTypeId);
			
			if (!currentDeviceType)
				$scope.currentDeviceType = $scope.deviceTypes[0];
			else {
				localStorageService.set('currentDeviceTypeId', currentDeviceType.device_type_id);
				$scope.currentDeviceType = currentDeviceType;
			}

			// Get devices
			let devicesResult = await deviceService.listDevices($scope.currentDeviceType.device_type_id);

			$scope.devices = _formatDevices(devicesResult.devices);
			$scope.$apply();
		} catch (err) {
			console.error(err);
		}
	}

	function _formatDeviceTypes(deviceTypes) {
		for (let type of deviceTypes) {
			type.name = type.name.split('-').map(item => {
				item = item.replace(/_/g, ' ');
				item = item[0].toUpperCase() + item.substr(1);

				return item;
			}).join(' - ');
		}

		return deviceTypes;
	}

	function _formatDevices(devices) {
		for (let device of devices) {
			if (typeof device.device_profile_body === 'string') {
				device.device_profile_body = JSON.parse(device.device_profile_body);
			}
			device.device_key_hash = device.device_key_hash.replace(/\//g, '%2F');
		}

		return devices;
	}

	$scope.onChooseDeviceType = async function(deviceType) {
		try {
			localStorageService.set('currentDeviceTypeId', deviceType.device_type_id);
			$scope.currentDeviceType = deviceType;
			
			if ($location.path() !== '/') {
				console.log('sss')
				$location.path('/');
			}

			// Get devices
			let devicesResult = await deviceService.listDevices($scope.currentDeviceType.device_type_id);
			console.log(devicesResult)
			$scope.devices = _formatDevices(devicesResult.devices);
			$scope.$apply();
		} catch (err) {
			console.error(err);
		}
	}
}
