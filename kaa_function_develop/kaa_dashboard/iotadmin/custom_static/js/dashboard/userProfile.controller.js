angular
	.module('app.dashboard')
	.controller('UserProfileController', UserProfileController);

UserProfileController.$inject = [
	'$scope',
	'app.dashboard.route',
	'localStorage.service',
	'$location',
	'dashboard.service',
	'$routeParams',
	'modal.service',
	'$timeout'
];

function UserProfileController(
	$scope,
	route,
	localStorage,
	$location,
	dashboardService,
	$routeParams,
	modalService,
	$timeout
) {

	const getUserProfile = async function() {
		try {
			$scope.failed = false;
			let userId = $routeParams.userId;
			let response;

			if (userId !== $scope.user.user_id)
				response = await dashboardService.getUserProfile($scope.user.token, userId);
			else
				response = await dashboardService.getCurrentUserProfile($scope.user.token);
			$scope.current_user = response.data;
			$scope.$apply();
		} catch (err) {
			let { data, status } = err;
			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
			$scope.$apply();
		}
	};

	$scope.$on('$routeChangeSuccess',function(){
		getUserProfile();
	});

	// TODO: deduplicate
	$scope.deleteUser = async function(user) {
		try {
			$scope.failed = false;
			let { data, headers, status } = await dashboardService.deleteUser($scope.user.token, user.user_id);
			$scope.success = 'User has been deleted.';
			$scope.$apply();
			$timeout(() => {
				$location.path('/users');
			}, 1000);
		} catch (err) {
			console.error(err);
			let { data, status } = err;

			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
			$scope.$apply();
		}
	}

	$scope.openModalConfirmDelete = function(user) {
		modalService.open({
			target: user,
			action: 'Delete',
			doAction: $scope.deleteUser,
			modalClass: 'danger',
			title: 'Confirm Delete User',
			content: `Are you sure to delete user <b>${user.username}</b>?`
		});
	}

	$scope.updatePassword = async function() {
		try {
			if ($scope.new_password !== $scope.confirm_new_password) {
				$scope.formFailed = true;
				$scope.formError = 'Please confirm your password again.';
				return;
			}
			let response = await dashboardService.changePassword($scope.user.token, $scope.old_password, $scope.new_password);
			
			$scope.formSuccess = 'Successfully change password.';
			$scope.showSpin = true;
			$scope.spinText = 'Go to Login page in 3s.';
			$scope.$apply();
			$timeout(() => { $scope.logout(); }, 3000);
		} catch (err) {
			console.error(err);
			$scope.formFailed = true;
			$scope.formError = err.status + ' - ' + err.data;
			$scope.$apply();
		}
	}

	$scope.openModalChangePassword = function(user) {
		modalService.open({
			target: user,
			action: 'Change Password',
			doAction: $scope.updatePassword,
			templateUrl: 'templates/updatePasswordModal.html',
			modalClass: 'warning',
			title: 'Change Password',
			content: `Are you sure to delete user <b>${user.username}</b>?`
		});
	}
}
