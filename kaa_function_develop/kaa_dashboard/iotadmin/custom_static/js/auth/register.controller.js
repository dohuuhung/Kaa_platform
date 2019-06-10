angular
	.module('app.auth')
	.controller('RegisterController', RegisterController);

RegisterController.$inject = [
	'$scope',
	'localStorage.service',
	'$location',
	'auth.service',
	'$timeout'
];

function RegisterController($scope, localStorage, $location, authService, $timeout) {
	
	$scope.doRegister = async function() {
		$scope.failed = false;
		try {
			await authService.register({
				username: $scope.username,
				firstname: $scope.firstname,
				lastname: $scope.lastname,
				email: $scope.email,
				tenant_name: $scope.tenant_name,
			});
			$scope.success = 'Success registration, we will send a temporary password to your email address.';
			$scope.showSpin = true;
			$scope.spinText = 'Go to Login page in 5s.';
			$scope.$apply();
			$timeout(() => { $location.path('/login'); }, 5000);
		} catch (err) {
			$scope.failed = true;
			$scope.error = err.status + ' - ' + err.data;
			$scope.$apply();
		}
	}
}