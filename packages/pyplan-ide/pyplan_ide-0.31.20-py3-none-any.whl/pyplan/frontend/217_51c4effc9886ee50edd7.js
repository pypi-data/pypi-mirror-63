/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[217],{1844:function(n,a,d){var o=d(690);n.exports=(o.default||o).template({compiler:[8,">= 4.3.0"],main:function(n,a,d,o,i){var t,e=n.lambda,l=n.escapeExpression;return'<div id="documentationModal" class="modal fade documentationModalView" tabindex="-1" role="dialog"\n  aria-labelledby="myModalLabel" aria-hidden="true">\n  <div class="modal-dialog">\n\n    <div class="modal-content">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">x</button>\n        <h4>'+l(e(null!=(t=null!=a?a.nodeData:a)?t.title:t,a))+" ("+l(e(null!=(t=null!=a?a.nodeData:a)?t.id:t,a))+') </h4>\n      </div>\n\n      <div class="modal-body">\n\n        <div class="col-sm-12 documentation">\n          '+(null!=(t=e(null!=(t=null!=a?a.nodeData:a)?t.description:t,a))?t:"")+'\n        </div>\n\n      </div>\n\n      <div class="clearfix"></div>\n    </div>\n  </div>\n</div>'},useData:!0})},957:function(n,a,d){"use strict";(function(o,i){var t,e;t=[d(1844)],void 0===(e=function(n,a){return o.View.extend({el:i("#main"),render:function(){var a=n(this.options);this.$el.append(a);var d=parseInt(.9*i(window).height()).toString();i("#documentationModal .modal-content").css("max-height",d+"px"),i("#documentationModal").on("hidden.bs.modal",function(){i("#documentationModal").off("hidden.bs.modal"),i("#documentationModal").remove()}).modal("show"),i("#documentationModal").css("z-index","10009"),i(".modal-backdrop").css("z-index","10008")}})}.apply(a,t))||(n.exports=e)}).call(this,d(218),d(1))}}]);