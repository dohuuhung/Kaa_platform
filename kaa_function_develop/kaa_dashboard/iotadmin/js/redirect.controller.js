angular
	.module('app')
	.controller('RedirectController', RedirectController);

RedirectController.$inject = [
	'$window',
    '$location',
];

function RedirectController($window, $location) {
	$window.location.href = $location.absUrl();
}
