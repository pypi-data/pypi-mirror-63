/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[309],{724:function(e,t,n){"use strict";(function(o,a){var i,r=n(693);void 0===(i=function(){return o.Model.extend({defaults:{dashId:null,dashboardViewList:[],modifiedDash:!1,noQuery:[],styleLibraries:[],nodeOwner:"",extraOptions:void 0},resizeTimeOut:0,getDashboard:function(e,t){(0,r.send)("dashboardManager/by_id/".concat(e,"/"),null,null,function(e){e&&(t(e),a("#summary").trigger("refresh"))})},getNavigator:function(e,t){var n=e.reportId,o=void 0===n?null:n,a=e.dashboardId,i=void 0===a?null:a,s="";o?(s="?report_id=".concat(o),i&&(s+="&dashboard_id=".concat(i))):i&&(s="?dashboard_id=".concat(i)),(0,r.send)("reportManager/getNavigator/".concat(s),null,null,t)},calculateScaleFactor:function(e,t){if(this.getItemsModel().length>0)for(var n=this.getItemsModel(),o=0;o<n.length;o++)n[o].calculateScaleFactor(e,t)},updateSizes:function(e,t){if(this.getItemsModel().length>0){var n=300;t&&(n=1),clearTimeout(this.resizeTimeOut);var o=this.getItemsModel();this.resizeTimeOut=setTimeout(function(){var e;for(e=0;e<o.length;e++)o[e].baseUpdateSize(),o[e].updateSize()},n)}},setStateModified:function(e){this.set({modifiedDash:e})},getStateModified:function(){return this.get("modifiedDash")},addItemToModel:function(e){this.get("dashboardViewList").push(e)},getItemsModel:function(){return this.get("dashboardViewList")},getItemModel:function(e){var t,n=this.getItemsModel();for(t=0;t<n.length;t++)if(n[t].tagId==e)return n[t]},countItemsModelByNodeId:function(e){for(var t=0,n=this.getItemsModel(),o=0;o<n.length;o++)n[o].currentNodeId&&e&&n[o].currentNodeId.toLowerCase()==e.toLowerCase()&&t++;return t},removeItemModel:function(e){var t,n=this.getItemsModel();for(t=0;t<n.length;t++)if(n[t].tagId==e.tagId){n.splice(t,1);break}this.set({dashboardViewList:n})},removeAllItemsModel:function(){this.set("dashboardViewList",[])},changeItemModel:function(e,t){this.removeItemModel(e),this.addItemToModel(t)},setNodeOwner:function(e){this.set("node",e)},getNodeOwner:function(){return this.get("node")},onFilterChange:function(e,t,n,o,a,i){if(a){var r=this.getItemModel(a);if(r&&r.isUnlinkedIndex(e))return void r.onFilterChange(e,t,n,o,!0)}var s=this.getItemsModel();if(s)for(var d=0;d<s.length;d++)s[d].onFilterChange(e,t,n,o,!1,i)},onFiltersChange:function(e){var t=this.getItemsModel();if(t)for(var n=0;n<t.length;n++)t[n].onFiltersChange(e)},synchronizeDrop:function(e,t,n,o,a,i,r){if(r){var s=this.getItemsModel();if(s)for(var d=0;d<s.length;d++)s[d].tagId&&s[d].tagId!=r&&s[d].onSynchronizeDrop(e,t,n,o,a,i)}},synchronizeLevel:function(e,t,n){if(n){var o=this.getItemsModel();if(o)for(var a=0;a<o.length;a++)o[a].tagId&&o[a].tagId!=n&&o[a].onSynchronizeLevel(e,t)}},getNodeFullData:function(e,t,n,o){var a={node:e};t&&(a.fromRow=1,a.toRow=t),(0,r.send)("dashboardManager/getNodeFullData/",a,{type:"GET"},n,o)},getNodeIndexes:function(e,t){(0,r.send)("dashboardManager/getNodeIndexes/",{node:e},null,function(e){e&&t(e)})},getIndexValues:function(e,t){(0,r.send)("dashboardManager/getIndexValues/",e,null,function(e){e&&t(e)})},getGeoDef:function(e,t){(0,r.send)("Dashboard/GetGeoDef/"+e,null,null,function(e){e&&t(e)})},evaluateNode:function(e,t,n,o,a,i,s,d,l,u,c,f,h,g,m){d||(d="sum");var v={node:e,dims:t,rows:n,columns:o,summaryBy:d,bottomTotal:c,rightTotal:f,timeFormat:h,timeFormatType:g,calendarType:m},p="evaluateNode";i&&(p="evaluateNodeDef"),l&&l>0&&u&&u>0&&(v.fromRow=l*(u-1)+1,v.toRow=l*u),(0,r.send)("dashboardManager/".concat(p,"/"),JSON.stringify(v),{type:"POST",contentType:"application/json;charset=utf-8"},a,s)},evaluateNodeForPivot:function(e,t,n,o){(0,r.send)("Dashboard/EvaluateNodeForPivot/",{node:e},{type:"GET"},function(e){var i=e.value,r={success:function(e,n,o){t(e)},complete:function(){a("#mainLoading").hide(),a("#secondLoading").hide(),n()},dataType:"json",progress:function(e){if(e.lengthComputable){var t=e.loaded/e.total*100;o(t)}else try{var n=this.getResponseHeader("X-Content-Length");t=e.loaded/n*100;o(t)}catch(e){}}};a("#secondLoading").show(),a.ajax("".concat(__apiURL,"/scripts/download.aspx?name=").concat(i),r)},n)},updateDefinition:function(e,t,n,o){var i=[];n&&a.each(n,function(e,t){i.push({id:t})});var s={dashboardId:e,definition:t,styles:n};(0,r.send)("dashboardManager/".concat(e,"/"),JSON.stringify(s),{type:"PATCH",contentType:"application/json;charset=utf-8",dataType:"text"},function(e){void 0!=o&&o(e)})},updateDashboardImage:function(e,t,n){var o={id:e,fileData:t};(0,r.send)("Dashboard/UpdateImage/",o,{type:"PUT"},function(t){a("#summary").trigger("refresh"),a("#model-summary").trigger("refresh",{id:e}),t&&n&&n(t)})},validateIndexes:function(e,t){var n=function(t){var n;for(n=0;n<e.length;n++)if(e[n].field==t)return e[n]},o=function(e){var t,o;for(t=0;t<e.length;t++)void 0!=(o=n(e[t].field))&&(e[t].name=o.name)};o(t.dims),o(t.rows),o(t.columns)},initializeDashboardQuery:function(e){this.set("noQuery",e),this._initNoQuery()},_initNoQuery:function(){var e=this.get("noQuery");e&&e.length>0&&a.each(e,function(e,t){t.started=!1})},isReadyForEvaluate:function(e,t){var n=!0,o=this.get("noQuery");return o&&o.length>0&&a.each(o,function(o,a){a.node==e?a.started=!0:0==a.started&&a.rel&&a.rel.indexOf(t)>=0&&(n=!1)}),n},setNodeValueChanges:function(e,t){(0,r.send)("dashboardManager/pivotGrid/setCubeChanges/",JSON.stringify(e),{type:"POST",contentType:"application/json;charset=utf-8"},function(e){t(e),a("body").trigger("pendingChanges",[!0])})},isResultComputed:function(e,t){(0,r.send)("dashboardManager/isResultComputed/",JSON.stringify({nodes:e}),{type:"POST",contentType:"application/json;charset=utf-8"},function(e){t(e)})},reevaluateNodesNeeded:function(e){a(".dashboardTask").trigger("reevaluateNodesNeeded",[e])},reevaluateNodesNeededInThisDashboard:function(e){for(var t=[],n=this.getItemsModel(),o=0;o<n.length;o++){var i=n[o].getNodesOfView();i&&(t=t.concat(i))}t.length>0&&this.isResultComputed(t,function(t){if(t&&t.length>0)for(var o=0;o<n.length;o++)e&&n[o].tagId==e||(t.indexOf(n[o].currentNodeId)>=0&&a(n[o].tagId).trigger("evaluateNodeFromCurrentResult"),n[o].needRefresh(t)&&n[o].refreshItemDash())})},applyNumberFormat:function(e){for(var t=this.getItemsModel(),n=0;n<t.length;n++)t[n].currentNodeId==e&&t[n].applyNumberFormat()},getStyleLibrary:function(e){var t=this.get("styleLibraries");if(t)for(var n=0;n<t.length;n++)if(t[n].id==e)return t[n].definition;return[]},getStyleLibraries:function(){return this.get("styleLibraries")},setStyleLibraries:function(e){return this.set("styleLibraries",e)},refreshStyleLibraries:function(e){var t=this;n.e(62).then(function(){var o=[n(743)];(function(n){(new n).list(null,function(n){t.set("styleLibraries",n),e(n)})}).apply(null,o)}).catch(n.oe)},syncDrilldown:function(e,t,n){var o=this.getItemsModel();if(o)for(var a=0;a<o.length;a++)o[a].tagId!=n&&o[a].syncDrilldown(e,t,n)},syncDrillUp:function(e,t){var n=this.getItemsModel();if(n)for(var o=0;o<n.length;o++)n[o].tagId!=t&&n[o].syncDrillup(e,t)},syncShowHideLegend:function(e,t,n){},viewAsChart:function(e,t){(0,r.send)("Dashboard/viewAsChart/",e,{type:"POST"},t)}})}.apply(t,[]))||(e.exports=i)}).call(this,n(218),n(1))}}]);