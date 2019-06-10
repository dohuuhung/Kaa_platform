angular
	.module('app.dashboard')
	.factory('dashboard.service', dashboardService);

dashboardService.$inject = [
	'$http',
	'apiBase'
];

function dashboardService($http, apiBase) {
	return {
		// User
		getTenantUsers,
		getUserProfile,
		deleteUser,
		getCurrentUserProfile,
		changePassword,


		// Devices
		getDevices,
		deleteDevice,
		getDeviceOverviews,
		getDeviceSpecifications,
		getDeviceMonitorData,

		// Device Type
		getDeviceTypes,
		getDeviceTypeOverviews,
		getDeviceTypeParameters
	};


	function changePassword(token, old_password, new_password) {
		console.log({token, old_password, new_password})
		return new Promise((resolve, reject) => {
			// $http({
			// 	method: 'POST',
			// 	url: apiBase + 'change_password',
			// 	headers: { 'Content-Type': 'application/json', token },
			// 	data: { old_password, new_password }
			// }).success(function(data, status, headers) {
			// 	resolve({ data, status, headers });
			// }).error(function(data, status) {
			// 	reject({ data, status });
			// });

			// resolve({
			// 	status: 200,
			// 	headers: {},
			// 	data: {}
			// })

			reject({
				status: 401,
				data: 'Unknown error'
			})
		});
	}

	function getTenantUsers(token) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'GET',
				url: apiBase + 'tenant_admin/users',
				headers: { 'Content-Type': 'application/json', token },
				params: {}
			}).then(resolve, reject);

			// let data = [];
			// for (let i = 0; i < 30; i++) {
			// 	data.push({ user_id: '2014266' + i, username: 'user' + i })
			// }

			// resolve({
			// 	data,
			// 	status: 200,
			// });

			// // // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// // Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });
		});
	}

	function getUserProfile(token, userId) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'GET',
				url: apiBase + 'tenant_admin/users/profile/' + userId,
				headers: { 'Content-Type': 'application/json', token },
				params: {}
			}).then(resolve, reject);

			// resolve({
			// 	data: {
			// 	  authority: "Tenant user",
			// 	  firstname: "Nguyen",
			// 	  lastname: "Toan",
			// 	  email: "toannt@gmail.com",
			// 	  username: "hungdh9"
			// 	},
			// 	status: 200,
			// });

			// // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });			

		});
	}

	function deleteUser(token, userId) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'DELETE',
				url: apiBase + 'tenant_admin/users/delete/' + userId,
				headers: { 'Content-Type': 'application/json', token },
			}).then(resolve, reject);

			// resolve({
			// 	data: {},
			// 	status: 200,
			// });

			// // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// // Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });			

		});		
	}

	function getCurrentUserProfile(token, userId) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'GET',
				url: apiBase + 'current_user_profile',
				headers: { 'Content-Type': 'application/json', token },
			}).then(resolve, reject);

			// resolve({
			// 	data: {
			// 	  authority: "Tenant administrator",
			// 	  firstname: "Do",
			// 	  lastname: "Hung",
			// 	  email: "mrjohan3004@gmail.com",
			// 	  username: "datn_user_1"
			// 	},
			// 	status: 200,
			// });

			// // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// // Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });			

		});		
	}

	function getDevices(token) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'GET',
				url: apiBase + 'devices',
				headers: { 'Content-Type': 'application/json', token },
				params: {}
			}).then(resolve, reject);

			// let data = [];

			// for (let i = 0; i < 20; i++) {
			// 	data.push({
			//     device_name: "device_" + i,
			//     device_key_hash: " P8v3sebtc/Ied/iaE3vnhEf/Ma0" + i,
			//     uuid: '5cf4d6f6a90e2e0c3864b59' + i,
			//     status: i % 2
			// 	});
			// }

			// resolve({
			// 	data,
			// 	status: 200,
			// });

			// // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// // Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });			

		});		
	}

	function deleteDevice(token, device_key_hash) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'DELETE',
				url: apiBase + 'devices/delete',
				headers: { 'Content-Type': 'application/json', token },
				data: { device_key_hash }
			}).then(resolve, reject);

			// resolve({
			// 	data: {},
			// 	status: 200,
			// });

			// // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// // Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });			

		});		
	}

	function formatDeviceKeyHash(deviceKeyHash) {
		return deviceKeyHash.replace(/\//gi, 'F2FZAC')
	}

	function getDeviceOverviews(token, device_key_hash) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'GET',
				url: apiBase + 'devices/overviews/' + formatDeviceKeyHash(device_key_hash),
				headers: { 'Content-Type': 'application/json', token },
				// data: { device_key_hash }
				// params: { device_key_hash: formatDeviceKeyHash(device_key_hash) }
			}).then(resolve, reject);

			// resolve({
			// 	data: {
			// 	  device_name: "device_1",
			// 	  credentials: "P8v3sebtc/Ied/iaE3vnhEf/Ma0=",
			// 	  device_type: {
			// 			device_type_id: "32768",
			// 			device_type_token: '77632917579169294658',
			// 			device_type_name: "device_type_a",
			// 			parameters:
   //          [
   //            {
   //              display_name: "Nhiet do khong khi",
   //              name: "air_temperature",
   //              unit: "oC"
   //            },
   //            {
   //              display_name: "Do am khong khi",
   //              name: "air_humidity",
   //              unit: "%"
   //            },
   //            {
   //              display_name: "Cuong do anh sang",
   //              name: "luminous_intensity",
   //              unit: "cd"
   //            }
   //          ]
			// 		}
			// 	},
			// 	status: 200,
			// });

			// // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// // Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });			

		});		
	}

	function getDeviceSpecifications(token, device_key_hash) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'GET',
				url: apiBase + 'devices/specifications/' + formatDeviceKeyHash(device_key_hash),
				headers: { 'Content-Type': 'application/json', token },
				// data: { device_key_hash }
			}).then(resolve, reject)

			// resolve({
			// 	data: {
			// 	  "Dai do nhiet do": "10-50oC",
			// 	  "Do dai que do": "80mm",
			// 	  "Do chia nho nhat": "0.1oC"
			// 	},
			// 	status: 200,
			// });

			// // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// // Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });			

		});		
	}

	function getDeviceMonitorData(token, device_type_token, device_key_hash, parameter, limit=1000) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'GET',
				url: apiBase + 'devices/monitor/' + device_type_token + '/' + formatDeviceKeyHash(device_key_hash),
				headers: { 'Content-Type': 'application/json', token },
				// data: { device_key_hash },
				params: { parameter, limit }
			}).then(resolve, reject);

			// let data = [];
			// let now = Date.now();

			// for (let i = 0; i < limit; i++) {
			// 	data.push({
			// 		timestamp: { long: now },
			// 		value: Math.floor(100 * Math.random())
			// 	});

			// 	now -= 60000;
			// }

			// resolve({
			// 	data,
			// 	status: 200,
			// });

			// // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// // Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });			

		});
	}

	function getDeviceTypes(token) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'GET',
				url: apiBase + 'device_types',
				headers: { 'Content-Type': 'application/json', token },
				params: {}
			}).then(resolve, reject);

			// let data = [];

			// for (let i = 0; i < 6; i++) {
			// 	data.push({
			//     device_type_id: "3276" + i,
			//     device_type_token: "7763291757916929465" + i,
			//     device_type_name: "device_type_a" + i
			//   });
			// }

			// resolve({
			// 	data,
			// 	status: 200,
			// });

			// // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// // Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });			

		});		
	}

	function getDeviceTypeOverviews(token, device_type_token) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'GET',
				url: apiBase + 'device_types/overviews/' + device_type_token,
				headers: { 'Content-Type': 'application/json', token },
				params: {}
			}).then(resolve, reject);

			// let data = {
			//     device_type_id: "32768",
			//     device_type_token: "77632917579169294658",
			//     device_type_name: "device_type_a",
			//     credential_service: "Internal"
			// };

			// resolve({
			// 	data,
			// 	status: 200,
			// });

			// // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// // Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });			

		});		
	}

	function getDeviceTypeParameters(token, device_type_token) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'GET',
				url: apiBase + 'device_types/parameters/' + device_type_token,
				headers: { 'Content-Type': 'application/json', token },
				params: {}
			}).then(resolve, reject);

			// let data = [
			//   {
			//     display_name: "Nhiet do khong khi",
			//     name: "air_temperature",
			//     unit: "oC"
			//   },
			//   {
			//     display_name: "Do am khong khi",
			//     name: "air_humidity",
			//     unit: "%"
			//   },
			//   {
			//     display_name: "Cuong do anh sang",
			//     name: "luminous_intensity",
			//     unit: "cd"
			//   }
			// ];

			// resolve({
			// 	data,
			// 	status: 200,
			// });

			// // Unknown error
			// reject({
			// 	data: 'Unknown error',
			// 	status: 401,
			// });

			// // Token expired
			// reject({
			// 	data: 'Token expired',
			// 	status: 403,
			// });

			// // Invalid/ missing token
			// reject({
			// 	data: 'Invalid token',
			// 	status: 405,
			// });			

		});		
	}
}
