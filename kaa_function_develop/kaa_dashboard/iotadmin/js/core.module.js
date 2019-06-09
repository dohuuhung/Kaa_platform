angular
  .module('app.core', [])
  .factory('app.core.api.service', ApiService);
/* eslint-enable angular/no-service-method */

ApiService.$inject = ['$http', '$window'];

function ApiService($http, $window, uploadService) {
  $window.API_URI = 'http://3.14.83.43:2004/api';

  var httpCall = function (method, url, data, config) {
    var backend = $http;

    // An external call goes directly to some OpenStack service, say Glance
    // API, not to the Horizon API wrapper layer. Thus it doesn't need a
    // WEBROOT prefix
    
    // var external = pop(config, 'external');
    // if (!external) {
    //   /* eslint-disable angular/window-service */
    //   url = $window.WEBROOT + url;
    //   /* eslint-enable angular/window-service */

    //   url = url.replace(/\/+/g, '/');
    // }

    if (angular.isUndefined(config)) {
      config = {};
    }
    // url and method are always provided
    config.method = method;
    config.url = $window.API_URI + url;
    if (angular.isDefined(data)) {
      config.data = data;
    }

    return backend(config).then(function success(res) {
      return res.data;
    } , function error(res) {
      return res;
    });
  };

  this.get = function(url, config) {
    return httpCall('GET', url, null, config);
  };

  this.post = function(url, data, config) {
    return httpCall('POST', url, data, config);
  };

  this.patch = function(url, data, config) {
    return httpCall('PATCH', url, data, config);
  };

  this.put = function(url, data, config) {
    return httpCall('PUT', url, data, config);
  };

  // NOTE the deviation from $http.delete which does not have the data param
  this.delete = function (url, data, config) {
    return httpCall('DELETE', url, data, config);
  };

  return this;
}

function pop(obj, key) {
  if (!angular.isObject(obj)) {
    return undefined;
  }
  var value = obj[key];
  delete obj[key];
  return value;
}
