{% load static %}
'use strict';

var AppConfig = new function() {

    {% for key, value in AppConfig.items %}
    this.{{key}} = "{{value}}";
    {% endfor %}
    //this.welcome = "{{welcome}}";
    //this.welcome_description = "{{welcome_description}}";
    //this.welcome_button_test = ""

    this.base_path = "{% static '' %}";
    this.app_dependencies = ['ui.router',  'ui.bootstrap', 'ngAnimate'];

    this.register_module = function(module_name, dependencies) {
        angular.module(module_name, dependencies || []);
        angular.module(this.app_name).requires.push(module_name);
    };

}
