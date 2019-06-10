angular
	.module('app.auth')
	.controller('LoginController', LoginController);

LoginController.$inject = [
	'$scope',
	'localStorage.service',
	'$location',
	'auth.service',
	'$timeout'
];

function LoginController($scope, localStorage, $location, authService, $timeout) {
	
	$scope.doLogin = async function() {
		$scope.failed = false;
		try {
			let response = await authService.login($scope.username, $scope.password);
			console.log(response);
			let user = response.data;
			localStorage.setObject('user', user);
			$scope.success = 'Login success';
			$scope.showSpin = true;
			$scope.spinText = 'Go to Home page in 3s.';
			$scope.$apply();
			$timeout(() => { $location.path('/'); }, 3000);

		} catch (err) {
			$scope.failed = true;
			$scope.error = err.status + ' - ' + err.data.result;
			if (err.status == 402) {
				$scope.showSpin = true;
				$scope.spinText = 'Go to Change temporary password page in 3s.';
				$timeout(() => { $location.path('/change_temporary_password'); }, 3000);
			}
			$scope.$apply();
		}
	}

	$scope.doChangeTempPassword = async function() {
		$scope.failed = false;
		try {
			if ($scope.new_password !== $scope.confirm_new_password) {
				$scope.failed = true;
				$scope.error = 'Please confirm your password again.';
				return;
			}
			let user = localStorage.getObject('user');
			let response = await authService.changeTempPassword($scope.username,
				$scope.old_password, $scope.new_password);
			
			$scope.success = 'Successfully change password.';
			$scope.showSpin = true;
			$scope.spinText = 'Go to Login page in 3s.';
			$scope.$apply();
			$timeout(() => { $location.path('/login'); }, 3000);
		} catch (err) {
			console.error(err);
			$scope.failed = true;
			$scope.error = err.status + ' - ' + err.data.result;
			$scope.$apply();
		}
	}
}