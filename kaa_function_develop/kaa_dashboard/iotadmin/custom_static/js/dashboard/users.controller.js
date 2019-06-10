angular
	.module('app.dashboard')
	.controller('UsersController', UsersController);

UsersController.$inject = [
	'$scope',
	'app.dashboard.route',
	'localStorage.service',
	'$location',
	'dashboard.service',
	'$route',
	'$timeout',
	'modal.service'
];

function UsersController(
	$scope,
	route,
	localStorage,
	$location,
	dashboardService,
	$route,
	$timeout,
	modalService
) {

	const getUsers = async function() {
		try {
			$scope.failed = false;
			let { data, headers, status } = await dashboardService.getTenantUsers($scope.user.token);
			$scope.users = data;
			$scope.$apply();
		} catch (err) {
			let { data, status } = err;

			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
			$scope.$apply();
		}
	};

	$scope.deleteUser = async function(user) {
		try {
			$scope.failed = false;
			let { data, headers, status } = await dashboardService.deleteUser($scope.user.token, user.user_id);
			$scope.success = 'User has been deleted.';
			$scope.$apply();
			$timeout(() => {
				getUsers();
			}, 2000);
		} catch (err) {
			let { data, status } = err;

			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
			$scope.$apply();
		}
	}

	$scope.$on('$routeChangeSuccess',function(){
		getUsers();
	});

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

}
