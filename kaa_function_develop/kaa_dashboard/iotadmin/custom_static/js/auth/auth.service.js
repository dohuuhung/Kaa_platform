angular
	.module('app.auth')
	.factory('auth.service', authService);

authService.$inject = [
	'$http',
	'apiBase'
];

function authService($http, apiBase) {
	return {
		login,
		register,
		changeTempPassword
	};

	function login(username, password) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'POST',
				url: apiBase + 'login',
				headers: {},
				data: { username, password }
			}).then(resolve, reject);

			// resolve({
			// 	data: {
			// 		user_id: '1',
			// 	  auth_result: "OK",
			// 	  authority: "Tenant administrator",
			// 	  display_name: "Do Hung",
			// 	  tenant_name: "BK tenant",
			// 	  username: "hungdh9"
			// 	},
			// 	status: 200,
			// 	headers: {
			// 		token: 'eyJhbGciOiJIUzUxMiIsImV4cCI6MTU1OTQ2NTUyMiwiaWF0IjoxNTU5NDY0OTIyfQ.eyJpZCI6ImRvaHV1aHVuZyJ9.RMXF7YWtoLb70rr6fkUVx0KGbNqmuhfYabCD9KbuAx60RvDVEzZJtG9HNibUpZyIV5CHKYEBxwPHZU2tfDWn3Q'
			// 	}
			// });

			// // Need to change password
			// reject({
			// 	data: 'Need to change temporary password',
			// 	status: 402,
			// });

			// // Invalid credential
			// reject({
			// 	data: 'Invalid credential',
			// 	status: 403,
			// });
		});
	}

	function register(body) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'POST',
				url: apiBase + 'registry',
				headers: {},
				data: body
			}).then(resolve, reject);

			// resolve({
			// 	status: 200,
			// 	headers: {},
			// 	data: {}
			// })

			// reject({
			// 	status: 401,
			// 	data: 'Unknown error'
			// })
		});

			
	}

	function changeTempPassword(username, old_password, new_password) {
		return new Promise((resolve, reject) => {
			$http({
				method: 'POST',
				url: apiBase + 'change_temporary_password',
				headers: { 'Content-Type': 'application/json' },
				data: { username, old_password, new_password }
			}).then(resolve, reject);

			// resolve({
			// 	status: 200,
			// 	headers: {},
			// 	data: {}
			// })

			// reject({
			// 	status: 401,
			// 	data: 'Unknown error'
			// })
		});

			
	}
		
}
