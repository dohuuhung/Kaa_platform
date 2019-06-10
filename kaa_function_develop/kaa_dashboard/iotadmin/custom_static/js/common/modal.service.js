angular
	.module('app')
	.factory('modal.service', modalService);

modalService.$inject = [
	'$uibModal'
];

function modalService($uibModal) {
	return {
		open,
	};

	function open(params) {
    return $uibModal.open({
      animation: true,
      ariaLabelledBy: 'modal-title',
      ariaDescribedBy: 'modal-body',
      templateUrl: params.templateUrl || 'templates/modal.html',
      controller: 'ModalInstanceCtrl',
      controllerAs: 'ctrl',
      resolve: {
        params: function() {
        	return params;
        }
      }
    });
	}
}
