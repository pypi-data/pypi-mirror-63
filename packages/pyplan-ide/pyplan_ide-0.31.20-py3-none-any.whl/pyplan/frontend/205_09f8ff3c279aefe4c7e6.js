/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[205,5],{1018:function(n,a,e){var t=e(690);function o(n){return n&&(n.__esModule?n.default:n)}n.exports=(t.default||t).template({compiler:[8,">= 4.3.0"],main:function(n,a,t,l,s){var i=null!=a?a:n.nullContext||{},c=n.escapeExpression;return'       <div class="box">\n            \n               <span>'+c(o(e(688)).call(i,"copy_dashboard_splain",{name:"L",hash:{},data:s,loc:{start:{line:3,column:21},end:{line:3,column:50}}}))+'</span>\n\n           <div class="box-content">\n\n                <div class="control-group">\n                                            \n                    <div class="controls">\n                        <input type="text" class=\'input-xlarge\' name="name" value="'+c(o(e(688)).call(i,"copy_of",{name:"L",hash:{},data:s,loc:{start:{line:10,column:83},end:{line:10,column:98}}}))+" "+c(n.lambda(null!=a?a.dashboardName:a,a))+'"  />\n                    </div>\n                                        \n                </div>\n            \n\n\n        </div>'},useData:!0})},683:function(n,a,e){"use strict";(function(t){var o;void 0===(o=function(){return t.Controller.extend({name:"showModal",show:function(n){Promise.all([e.e(2),e.e(119)]).then(function(){var a=[e(700)];(function(a){(new a).render(n)}).apply(null,a)}).catch(e.oe)}})}.apply(a,[]))||(n.exports=o)}).call(this,e(694))},946:function(n,a,e){"use strict";(function(t,o){var l,s,i=e(18);l=[e(683),e(749),e(1018)],void 0===(s=function(n,a,e){return t.View.extend({el:o("#main"),render:function(t,o,l){var s=e({dashboardId:t,dashboardName:o});(new n).show({title:(0,i.translate)("copy_dashboard"),html:s,modalClass:"shortModal",buttons:[{title:(0,i.translate)("yes"),css:"primary",code:"yes"},{title:(0,i.translate)("close"),code:"close"}],callback:function(n,e){if("yes"==n){var o=e.find("input[name='name']").val();if(o&&""!=o)(new a).copyDashboard(o,t,function(n){var a=n.id;void 0!=l&&l(a,o),e.modal("hide")});else e.find("input[name='name']").focus();return!1}},onLoad:function(n){setTimeout(function(){n.find("input[name='name']").focus()},500)}})}})}.apply(a,l))||(n.exports=s)}).call(this,e(218),e(1))}}]);