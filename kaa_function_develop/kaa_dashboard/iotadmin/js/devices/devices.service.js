angular
	.module('app.devices')
	.factory('app.devices.service', deviceService);

deviceService.$inject = [
	'app.core.api.service'
];

const devicesList = [
	{
		device_id: 'c3a1d284-5b2c-46a2-b187-fc40792439e3',
		device_profile_body: {
			id: 'c3a1d284-5b2c-46a2-b187-fc40792439e3',
			os: 'Linux',
			os_version: '3.17',
			build: '0.0.1-SNAPSHOT',
			name: 'Device 1'
		},
		device_key_hash: '/XfhG73Ok5/v3hWlHAnB2gBkOhs=',
		state: 1,
	},
	{
		device_id: '13e24605-ea97-4f42-8ca8-69f4078ffc41',
		device_profile_body: {
			id: '13e24605-ea97-4f42-8ca8-69f4078ffc41',
			os: 'Linux',
			os_version: '3.17',
			build: '0.0.1-SNAPSHOT',
			name: 'Device 2'
		},
		device_key_hash: '+w6LqjbyNeYNxGFZwuhmgUPSOGs=',
		state: 0,
	},
	{
		device_id: '01b46434-b594-4a4d-8437-936fef4f0c6a',
		device_profile_body: {
			id: '13e24605-ea97-4f42-8ca8-69f4078ffc41',
			os: 'Linux',
			os_version: '3.17',
			build: '0.0.1-SNAPSHOT',
			name: 'Device 3'
		},
		device_key_hash: '+w6LqjbyNeYNxGFZwuhmgUSHOGs=',
		state: 1,
	},
	{
		device_id: '01b46434-c594-4a4d-8437-936fef4f0c6a',
		device_profile_body: {
			id: '01b46434-c594-4a4d-8437-936fef4f0c6a',
			os: 'Linux',
			os_version: '3.17',
			build: '0.0.1-SNAPSHOT',
			name: 'Device 4'
		},
		device_key_hash: '+w6LqjbyNeYNxGFZwuhdfUSHOGs=',
		state: 1,
	},
];

const devicesMap = {
	'c3a1d284-5b2c-46a2-b187-fc40792439e3': {
		name: 'Device 1',
		state: 1,
		specification: {
			humidity_accurrent: '1.8%',
			temperature_accurrent: '0.2%',
			temperature_range: '-40 to 125oC',
			humidity_range: '0-100%'
		}
	},
	'13e24605-ea97-4f42-8ca8-69f4078ffc41': {
		name: 'Device 2',
		state: 0,
		specification: {
			humidity_accurrent: '1.8%',
			temperature_accurrent: '0.2%',
			temperature_range: '-40 to 125oC',
			humidity_range: '0-100%',
			sample: '120'
		}
	},
	'01b46434-b594-4a4d-8437-936fef4f0c6a': {
		name: 'Device 3',
		state: 1,
		specification: {
			humidity_accurrent: '2.8%',
			temperature_accurrent: '4.2%',
			temperature_range: '-30 to 125oC',
			humidity_range: '0-80%',
			sample: '120'
		}
	},
	'01b46434-c594-4a4d-8437-936fef4f0c6a': {
		name: 'Device 4',
		state: 1,
		specification: {
			humidity_accurrent: '2.8%',
			temperature_accurrent: '4.2%',
			temperature_range: '-30 to 125oC',
			humidity_range: '0-80%',
			sample: '120'
		}
	},
};

const deviceTypesList = [
	{
		device_type_id: 'c3a1d284-5b2c-46a2-b187-fc40792439e3',
		name: 'Temperature',
		description: 'Temperature',
	},
	{
		device_type_id: '13e24605-ea97-4f42-8ca8-69f4078ffc41',
		name: 'Humidity',
		description: 'Humidity',
	},
	{
		device_type_id: '01b46434-b594-4a4d-8437-936fef4f0c6a',
		name: 'IP Camera',
		description: 'IP Camera',
	}
];

function deviceService(
	apiService
) {
	return {
		listDeviceTypes,
		listDevices,
		showDevice,
		getMonitoringData
	};

	/**
	 * List device types
	 */
	function listDeviceTypes() {
		return apiService.get('/device_types', { external: true });
		// return new Promise((resolve, reject) => {
		// 	resolve(deviceTypesList);
		// });
	}

	/**
	 * List devices
	 */
	function listDevices(type, limit=50, offset=0) {
		return apiService.get('/devices?type='
			+ type + '&limit=' + limit + '&offset=' + offset);

		// return new Promise((resolve, reject) => {
		// 	resolve({
		// 		last_device: true,
		// 		devices: devicesList,
		// 	})
		// });
	}

	/**
	 * Device detail
	 */
	function showDevice(id) {
		return apiService.get('/devices/' + id);
		// return new Promise((resolve, reject) => {
		// 	resolve(devicesMap[id]);
		// });
	}

	/**
	 * Get history monitoring data
	 */
	function getMonitoringData(deviceTypeId, deviceKeyHash, parameter, limit=100) {
		return apiService.get('/monitor/' + deviceTypeId + '/' + deviceKeyHash
				+ '?parameter=' + parameter + '&limit=' + limit);
	}

}
