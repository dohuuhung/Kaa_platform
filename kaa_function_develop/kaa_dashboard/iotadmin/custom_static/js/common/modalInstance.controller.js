angular
  .module('app')
  .controller('ModalInstanceCtrl', ModalInstanceCtrl);

function ModalInstanceCtrl($uibModalInstance, params, $scope) {
  const ctrl = this;
  $scope.action = params.action;
  $scope.modalClass = params.modalClass;
  $scope.target = params.target;
  $scope.title = params.title;
  $scope.content = params.content;

  ctrl.ok = function () {
    params.doAction(params.target);  
    $uibModalInstance.close();
  };

  ctrl.doAction = function() {
    params.doAction(params.target);
  }

  ctrl.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
}