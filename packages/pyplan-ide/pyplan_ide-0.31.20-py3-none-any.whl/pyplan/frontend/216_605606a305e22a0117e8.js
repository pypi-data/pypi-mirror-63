/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[216,309],{1842:function(e,n,t){var a=t(690);function o(e){return e&&(e.__esModule?e.default:e)}e.exports=(a.default||a).template({1:function(e,n,t,a,o){var i;return"("+e.escapeExpression(e.lambda(null!=(i=null!=n?n.nodeData:n)?i.originalId:i,n))+")"},3:function(e,n,t,a,o){var i;return"("+e.escapeExpression(e.lambda(null!=(i=null!=n?n.nodeData:n)?i.id:i,n))+")"},compiler:[8,">= 4.3.0"],main:function(e,n,a,i,l){var d,s=e.escapeExpression,r=null!=n?n:e.nullContext||{};return'<div id="quickEvaluateModal" class="modal fade quickEvaluateView" tabindex="-1" role="dialog"\n  aria-labelledby="myModalLabel" aria-hidden="true">\n  <div class="modal-dialog">\n\n    <div class="modal-content">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">x</button>\n        <h4>'+s(e.lambda(null!=(d=null!=n?n.nodeData:n)?d.title:d,n))+" "+(null!=(d=a.if.call(r,null!=(d=null!=n?n.nodeData:n)?d.originalId:d,{name:"if",hash:{},fn:e.program(1,l,0),inverse:e.program(3,l,0),data:l,loc:{start:{line:8,column:31},end:{line:8,column:115}}}))?d:"")+'</h4>\n      </div>\n\n      <div class="modal-body">\n\n        <div class="col-sm-12 evaluating">\n          <label>'+s(o(t(688)).call(r,"please_wait",{name:"L",hash:{},data:l,loc:{start:{line:14,column:17},end:{line:14,column:36}}}))+'...</label>\n          <br /><br />\n        </div>\n\n        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 btnNodeProfileContainer nodisplay">\n          <a href="#" class="btnNodeProfile">'+s(o(t(688)).call(r,"show_node_profile",{name:"L",hash:{},data:l,loc:{start:{line:19,column:45},end:{line:19,column:70}}}))+'</a>\n        </div>\n\n        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 nodeProfileContainer nodisplay">\n\n        </div>\n        <div class="col-sm-12 resultType nodisplay">\n          <label>'+s(o(t(688)).call(r,"result_type",{name:"L",hash:{},data:l,loc:{start:{line:26,column:17},end:{line:26,column:36}}}))+'</label>\n          <div class="dimensionListPreview"></div>\n\n        </div>\n\n        <div class="col-sm-12 dimList nodisplay">\n          <label>'+s(o(t(688)).call(r,"dimension_list",{name:"L",hash:{},data:l,loc:{start:{line:32,column:17},end:{line:32,column:39}}}))+'</label>\n          <div class="dimensionListPreview"></div>\n        </div>\n\n        <div class="col-sm-12 columnList nodisplay">\n          <label>'+s(o(t(688)).call(r,"column_list",{name:"L",hash:{},data:l,loc:{start:{line:37,column:17},end:{line:37,column:36}}}))+'</label>\n          <div class="dimensionListPreview"></div>\n        </div>\n\n        <div class="col-sm-12 console nodisplay">\n          <label>'+s(o(t(688)).call(r,"console",{name:"L",hash:{},data:l,loc:{start:{line:42,column:17},end:{line:42,column:32}}}))+'</label>\n          <pre class="resultPreview"></pre>\n        </div>\n\n\n        <div class="col-sm-12 atomic nodisplay">\n          <label>'+s(o(t(688)).call(r,"result",{name:"L",hash:{},data:l,loc:{start:{line:48,column:17},end:{line:48,column:31}}}))+'</label>\n          <pre class="resultPreview"></pre>\n        </div>\n\n        <div class="col-sm-12 error nodisplay">\n          <label>'+s(o(t(688)).call(r,"error",{name:"L",hash:{},data:l,loc:{start:{line:53,column:17},end:{line:53,column:30}}}))+'</label>\n          <div class="dimensionListPreview" style="color:red"></div>\n\n        </div>\n\n\n      </div>\n\n      <div class="clearfix"></div>\n    </div>\n  </div>\n</div>'},useData:!0})},1843:function(e,n,t){var a=t(690);function o(e){return e&&(e.__esModule?e.default:e)}e.exports=(a.default||a).template({1:function(e,n,t,a,o){var i=e.lambda,l=e.escapeExpression;return"    <tr>\n      <td>"+l(i(null!=n?n.nodeId:n,n))+"</td>\n      <td>"+l(i(null!=n?n.title:n,n))+"</td>\n      <td>"+l(i(null!=n?n.evaluationTime:n,n))+"</td>\n      <td>"+l(i(null!=n?n.calcTime:n,n))+"</td>\n      <td>"+l(i(null!=n?n.calcPercentage:n,n))+" %</td>\n      <td>"+l(i(null!=n?n.usedMemory:n,n))+" MB</td>\n      <td>"+l(i(null!=n?n.rowIndex:n,n))+"</td>\n    </tr>\n"},compiler:[8,">= 4.3.0"],main:function(e,n,a,i,l){var d,s=null!=n?n:e.nullContext||{},r=e.escapeExpression;return"<table class='table table-nomargin nodeProfileTable'>\n  <thead>\n    <tr>\n      <th>"+r(o(t(688)).call(s,"nodeId",{name:"L",hash:{},data:l,loc:{start:{line:4,column:10},end:{line:4,column:24}}}))+"</th>\n      <th>"+r(o(t(688)).call(s,"nodeTitle",{name:"L",hash:{},data:l,loc:{start:{line:5,column:10},end:{line:5,column:27}}}))+"</th>\n      <th>"+r(o(t(688)).call(s,"evaluationTime",{name:"L",hash:{},data:l,loc:{start:{line:6,column:10},end:{line:6,column:32}}}))+"</th>\n      <th>"+r(o(t(688)).call(s,"calcTime",{name:"L",hash:{},data:l,loc:{start:{line:7,column:10},end:{line:7,column:26}}}))+"</th>\n      <th>"+r(o(t(688)).call(s,"calcPercentage",{name:"L",hash:{},data:l,loc:{start:{line:8,column:10},end:{line:8,column:32}}}))+"</th>\n      <th>"+r(o(t(688)).call(s,"usedMemory",{name:"L",hash:{},data:l,loc:{start:{line:9,column:10},end:{line:9,column:28}}}))+"</th>\n      <th>"+r(o(t(688)).call(s,"rowIndex",{name:"L",hash:{},data:l,loc:{start:{line:10,column:10},end:{line:10,column:26}}}))+"</th>\n    </tr>\n  </thead>\n  <tbody>\n"+(null!=(d=a.each.call(s,null!=n?n.nodes:n,{name:"each",hash:{},fn:e.program(1,l,0),inverse:e.noop,data:l,loc:{start:{line:14,column:4},end:{line:24,column:13}}}))?d:"")+"  </tbody>\n</table>"},useData:!0})},724:function(e,n,t){"use strict";(function(a,o){var i,l=t(693);void 0===(i=function(){return a.Model.extend({defaults:{dashId:null,dashboardViewList:[],modifiedDash:!1,noQuery:[],styleLibraries:[],nodeOwner:"",extraOptions:void 0},resizeTimeOut:0,getDashboard:function(e,n){(0,l.send)("dashboardManager/by_id/".concat(e,"/"),null,null,function(e){e&&(n(e),o("#summary").trigger("refresh"))})},getNavigator:function(e,n){var t=e.reportId,a=void 0===t?null:t,o=e.dashboardId,i=void 0===o?null:o,d="";a?(d="?report_id=".concat(a),i&&(d+="&dashboard_id=".concat(i))):i&&(d="?dashboard_id=".concat(i)),(0,l.send)("reportManager/getNavigator/".concat(d),null,null,n)},calculateScaleFactor:function(e,n){if(this.getItemsModel().length>0)for(var t=this.getItemsModel(),a=0;a<t.length;a++)t[a].calculateScaleFactor(e,n)},updateSizes:function(e,n){if(this.getItemsModel().length>0){var t=300;n&&(t=1),clearTimeout(this.resizeTimeOut);var a=this.getItemsModel();this.resizeTimeOut=setTimeout(function(){var e;for(e=0;e<a.length;e++)a[e].baseUpdateSize(),a[e].updateSize()},t)}},setStateModified:function(e){this.set({modifiedDash:e})},getStateModified:function(){return this.get("modifiedDash")},addItemToModel:function(e){this.get("dashboardViewList").push(e)},getItemsModel:function(){return this.get("dashboardViewList")},getItemModel:function(e){var n,t=this.getItemsModel();for(n=0;n<t.length;n++)if(t[n].tagId==e)return t[n]},countItemsModelByNodeId:function(e){for(var n=0,t=this.getItemsModel(),a=0;a<t.length;a++)t[a].currentNodeId&&e&&t[a].currentNodeId.toLowerCase()==e.toLowerCase()&&n++;return n},removeItemModel:function(e){var n,t=this.getItemsModel();for(n=0;n<t.length;n++)if(t[n].tagId==e.tagId){t.splice(n,1);break}this.set({dashboardViewList:t})},removeAllItemsModel:function(){this.set("dashboardViewList",[])},changeItemModel:function(e,n){this.removeItemModel(e),this.addItemToModel(n)},setNodeOwner:function(e){this.set("node",e)},getNodeOwner:function(){return this.get("node")},onFilterChange:function(e,n,t,a,o,i){if(o){var l=this.getItemModel(o);if(l&&l.isUnlinkedIndex(e))return void l.onFilterChange(e,n,t,a,!0)}var d=this.getItemsModel();if(d)for(var s=0;s<d.length;s++)d[s].onFilterChange(e,n,t,a,!1,i)},onFiltersChange:function(e){var n=this.getItemsModel();if(n)for(var t=0;t<n.length;t++)n[t].onFiltersChange(e)},synchronizeDrop:function(e,n,t,a,o,i,l){if(l){var d=this.getItemsModel();if(d)for(var s=0;s<d.length;s++)d[s].tagId&&d[s].tagId!=l&&d[s].onSynchronizeDrop(e,n,t,a,o,i)}},synchronizeLevel:function(e,n,t){if(t){var a=this.getItemsModel();if(a)for(var o=0;o<a.length;o++)a[o].tagId&&a[o].tagId!=t&&a[o].onSynchronizeLevel(e,n)}},getNodeFullData:function(e,n,t,a){var o={node:e};n&&(o.fromRow=1,o.toRow=n),(0,l.send)("dashboardManager/getNodeFullData/",o,{type:"GET"},t,a)},getNodeIndexes:function(e,n){(0,l.send)("dashboardManager/getNodeIndexes/",{node:e},null,function(e){e&&n(e)})},getIndexValues:function(e,n){(0,l.send)("dashboardManager/getIndexValues/",e,null,function(e){e&&n(e)})},getGeoDef:function(e,n){(0,l.send)("Dashboard/GetGeoDef/"+e,null,null,function(e){e&&n(e)})},evaluateNode:function(e,n,t,a,o,i,d,s,r,c,u,h,f,m,g){s||(s="sum");var v={node:e,dims:n,rows:t,columns:a,summaryBy:s,bottomTotal:u,rightTotal:h,timeFormat:f,timeFormatType:m,calendarType:g},p="evaluateNode";i&&(p="evaluateNodeDef"),r&&r>0&&c&&c>0&&(v.fromRow=r*(c-1)+1,v.toRow=r*c),(0,l.send)("dashboardManager/".concat(p,"/"),JSON.stringify(v),{type:"POST",contentType:"application/json;charset=utf-8"},o,d)},evaluateNodeForPivot:function(e,n,t,a){(0,l.send)("Dashboard/EvaluateNodeForPivot/",{node:e},{type:"GET"},function(e){var i=e.value,l={success:function(e,t,a){n(e)},complete:function(){o("#mainLoading").hide(),o("#secondLoading").hide(),t()},dataType:"json",progress:function(e){if(e.lengthComputable){var n=e.loaded/e.total*100;a(n)}else try{var t=this.getResponseHeader("X-Content-Length");n=e.loaded/t*100;a(n)}catch(e){}}};o("#secondLoading").show(),o.ajax("".concat(__apiURL,"/scripts/download.aspx?name=").concat(i),l)},t)},updateDefinition:function(e,n,t,a){var i=[];t&&o.each(t,function(e,n){i.push({id:n})});var d={dashboardId:e,definition:n,styles:t};(0,l.send)("dashboardManager/".concat(e,"/"),JSON.stringify(d),{type:"PATCH",contentType:"application/json;charset=utf-8",dataType:"text"},function(e){void 0!=a&&a(e)})},updateDashboardImage:function(e,n,t){var a={id:e,fileData:n};(0,l.send)("Dashboard/UpdateImage/",a,{type:"PUT"},function(n){o("#summary").trigger("refresh"),o("#model-summary").trigger("refresh",{id:e}),n&&t&&t(n)})},validateIndexes:function(e,n){var t=function(n){var t;for(t=0;t<e.length;t++)if(e[t].field==n)return e[t]},a=function(e){var n,a;for(n=0;n<e.length;n++)void 0!=(a=t(e[n].field))&&(e[n].name=a.name)};a(n.dims),a(n.rows),a(n.columns)},initializeDashboardQuery:function(e){this.set("noQuery",e),this._initNoQuery()},_initNoQuery:function(){var e=this.get("noQuery");e&&e.length>0&&o.each(e,function(e,n){n.started=!1})},isReadyForEvaluate:function(e,n){var t=!0,a=this.get("noQuery");return a&&a.length>0&&o.each(a,function(a,o){o.node==e?o.started=!0:0==o.started&&o.rel&&o.rel.indexOf(n)>=0&&(t=!1)}),t},setNodeValueChanges:function(e,n){(0,l.send)("dashboardManager/pivotGrid/setCubeChanges/",JSON.stringify(e),{type:"POST",contentType:"application/json;charset=utf-8"},function(e){n(e),o("body").trigger("pendingChanges",[!0])})},isResultComputed:function(e,n){(0,l.send)("dashboardManager/isResultComputed/",JSON.stringify({nodes:e}),{type:"POST",contentType:"application/json;charset=utf-8"},function(e){n(e)})},reevaluateNodesNeeded:function(e){o(".dashboardTask").trigger("reevaluateNodesNeeded",[e])},reevaluateNodesNeededInThisDashboard:function(e){for(var n=[],t=this.getItemsModel(),a=0;a<t.length;a++){var i=t[a].getNodesOfView();i&&(n=n.concat(i))}n.length>0&&this.isResultComputed(n,function(n){if(n&&n.length>0)for(var a=0;a<t.length;a++)e&&t[a].tagId==e||(n.indexOf(t[a].currentNodeId)>=0&&o(t[a].tagId).trigger("evaluateNodeFromCurrentResult"),t[a].needRefresh(n)&&t[a].refreshItemDash())})},applyNumberFormat:function(e){for(var n=this.getItemsModel(),t=0;t<n.length;t++)n[t].currentNodeId==e&&n[t].applyNumberFormat()},getStyleLibrary:function(e){var n=this.get("styleLibraries");if(n)for(var t=0;t<n.length;t++)if(n[t].id==e)return n[t].definition;return[]},getStyleLibraries:function(){return this.get("styleLibraries")},setStyleLibraries:function(e){return this.set("styleLibraries",e)},refreshStyleLibraries:function(e){var n=this;t.e(62).then(function(){var a=[t(743)];(function(t){(new t).list(null,function(t){n.set("styleLibraries",t),e(t)})}).apply(null,a)}).catch(t.oe)},syncDrilldown:function(e,n,t){var a=this.getItemsModel();if(a)for(var o=0;o<a.length;o++)a[o].tagId!=t&&a[o].syncDrilldown(e,n,t)},syncDrillUp:function(e,n){var t=this.getItemsModel();if(t)for(var a=0;a<t.length;a++)t[a].tagId!=n&&t[a].syncDrillup(e,n)},syncShowHideLegend:function(e,n,t){},viewAsChart:function(e,n){(0,l.send)("Dashboard/viewAsChart/",e,{type:"POST"},n)}})}.apply(n,[]))||(e.exports=i)}).call(this,t(218),t(1))},956:function(e,n,t){"use strict";(function(a,o){var i,l,d=t(18);i=[t(724),t(219),t(1842),t(1843)],void 0===(l=function(e,n,t,i){return a.View.extend({el:o("#main"),render:function(){var e=this,n=t(this.options);this.$el.append(n);var a=parseInt(.9*o(window).height()).toString();o("#quickEvaluateModal .modal-content").css("max-height",a+"px"),o("#quickEvaluateModal").on("hidden.bs.modal",function(){o("#quickEvaluateModal").find(".nodeProfileTable").DataTable().destroy(),o("#quickEvaluateModal").off("hidden.bs.modal"),o("#quickEvaluateModal").remove()}).modal("show"),o("#quickEvaluateModal").css("z-index","10009"),o(".modal-backdrop").css("z-index","10008"),setTimeout(function(){e.evaluateNode(o("#quickEvaluateModal"))},200)},evaluateNode:function(e){var t=this.options.nodeData.id,a=this;(new n).previewNode(t,function(n){e.find(".evaluating").hide(),n&&(n.resultType&&(e.find(".resultType div").text(n.resultType),e.find(".resultType").show()),n.dims&&n.dims.length>0&&(e.find(".dimList .dimensionListPreview").text(n.dims.join(", ")),e.find(".dimList").show()),n.columns&&n.columns.length>0&&(e.find(".columnList .dimensionListPreview").text(n.columns.join(", ")),e.find(".columnList").show()),n.console&&(e.find(".console").show(),e.find(".console pre").text(n.console)),e.find(".atomic").show(),e.find(".atomic pre").text(n.preview),a.showNodeProfile(t,e),o('.btn[data-action="run"]').click())},function(n){e.find(".evaluating").hide(),e.find(".error div").text(n),e.find(".error").show()})},showNodeProfile:function(e,t){t.find(".btnNodeProfileContainer").show(),t.isShowingProfile=!1,t.find(".btnNodeProfileContainer").on("click",function(a){(a.preventDefault(),t.isShowingProfile)?(t.find(".nodeProfileContainer").fadeOut("slow").html(""),t.find(".nodeProfileTable").DataTable().destroy(),t.find(".btnNodeProfileContainer a").text((0,d.translate)("show_node_profile")),t.isShowingProfile=!1):(new n).getProfile(e,function(e){var n=0;o.each(e,function(e,t){n+=t.calcTime}),o.each(e,function(t,a){e[t].calcPercentage=(a.calcTime/n*100).toFixed(2),e[t].evaluationTime=e[t].evaluationTime.toFixed(3),e[t].calcTime=e[t].calcTime.toFixed(3),e[t].usedMemory=e[t].usedMemory.toFixed(2),e[t].rowIndex=t});var a=i({nodes:e});t.find(".nodeProfileContainer").append(a),t.find(".nodeProfileContainer").fadeIn("slow"),t.find(".btnNodeProfileContainer a").text((0,d.translate)("hide_node_profile")),o.fn.DataTable.isDataTable(t.find(".nodeProfileTable"))&&t.find(".nodeProfileTable").DataTable().destroy(),t.find(".nodeProfileTable").DataTable({bAutoWidth:!1,iDisplayLength:-1,bLengthChange:!1,paging:!1,info:!1,scrollY:"300px",scrollX:!1,scrollCollapse:!0,columnDefs:[{targets:0,data:"nodeId",width:"30%"},{targets:1,data:"lastTitle",width:"30%"},{targets:2,data:"evaluationTime",width:"10%"},{targets:3,data:"calcTime",width:"10%"},{targets:4,data:"calcPercentage",width:"10%"},{targets:5,data:"usedMemory",width:"10%"},{targets:6,data:"rowIndex",visible:!1,searchable:!1}],aaSorting:[[6,"asc"]],fnRowCallback:function(e,n){0==n.rowIndex?o(e).addClass("highlightTableRow"):o(e).addClass("nothighlightTableRow")}}),t.isShowingProfile=!0})})}})}.apply(n,i))||(e.exports=l)}).call(this,t(218),t(1))}}]);