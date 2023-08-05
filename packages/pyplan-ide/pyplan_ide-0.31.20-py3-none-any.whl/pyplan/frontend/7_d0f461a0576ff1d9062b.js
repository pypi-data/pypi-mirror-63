/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[7,309],{702:function(e,a,t){"use strict";(function(n,o){var r,i;r=[t(684),t(724)],void 0===(i=function(e,a){return n.Controller.extend({name:"dashboardManager",showDashboard:function(a,n,r,i,c,l){var s="dashboard-"+a,u=new e;u.existsTask(s)?(u.selectTask(s),i&&o(".mainTask[data-rel='"+s+"']").length>0&&o(".mainTask[data-rel='"+s+"']").trigger("refreshView")):(u.addSimpleTask(s,r),t.e(19).then(function(){var e=[t(818)];(function(e){(new e).render(a,n,c,l),u.selectTask(s)}).apply(null,e)}).catch(t.oe))},showEmbeddableDashboard:function(a,n,r,i,c,l){var s="dashboard-"+a,u=new e;__currentSession.fromEmbedded&&u.removeAllTask(),u.existsTask(s)?(u.selectTask(s),i&&o(".mainTask[data-rel='"+s+"']").length>0&&o(".mainTask[data-rel='"+s+"']").trigger("refreshView")):(u.addSimpleTask(s,r),Promise.all([t.e(19),t.e(125)]).then(function(){var e=[t(1414)];(function(e){(new e).render(a,n,c,l),u.selectTask(s)}).apply(null,e)}).catch(t.oe))},removeDashboardTaskFromHome:function(a){var t="dashboard-"+a,n=new e;n.existsTask(t)&&n.removeTask(t)},drawDashboardBars:function(e,a){this.drawToolbar(e,function(){a()})},drawBottombar:function(e,a){t.e(126).then(function(){var n=[t(1416)];(function(t){var n=new t;n.setElement(e),n.render(),void 0!=a&&a()}).apply(null,n)}).catch(t.oe)},drawToolbar:function(e,a){t.e(41).then(function(){var n=[t(822)];(function(t){(new t).show({el:e,positions:["left","right"],onLoad:a,className:"dockDashboardProperty"})}).apply(null,n)}).catch(t.oe)},drawMoreDashboard:function(e,a){t.e(127).then(function(){var e=[t(1417)];(function(e){var t=new e;t.setElement("body"),t.render(a)}).apply(null,e)}).catch(t.oe)},getDefaultContent:function(e,a){Promise.all([t.e(1),t.e(9),t.e(60)]).then(function(){var n=[t(823)];(function(t){var n=new t({model:e});a(n)}).apply(null,n)}).catch(t.oe)},getEmptyContent:function(e,a){Promise.all([t.e(1),t.e(61)]).then(function(){var n=[t(1112)];(function(t){var n=new t({model:e});a(n)}).apply(null,n)}).catch(t.oe)},getChartToolbar:function(e,a,n,o){var r;switch(e){case"linechart":r="line/lineToolbar";break;case"columnchart":case"columnchartstacked":case"columnchartpercent":case"barchart":case"barchartstacked":case"barchartpercent":r="columnAndBar/columnAndBarToolbar";break;case"areachart":case"areachartstacked":case"areachartpercent":r="area/areaToolbar";break;case"piechart":r="pie/pieToolbar";break;case"funnelchart":r="funnelToolbar/funnelToolbar";break;case"pyramidchart":r="pyramidToolbar/pyramidToolbar";break;case"gaugechart":r="gauge/gaugeToolbar";break;case"waterfallchart":r="waterfall/waterfallToolbar";break;case"scatterchart":r="scatter/scatterToolbar";break;case"table":r="table/tableToolbar";break;case"indexlist":r="index/indexToolbar";break;case"map":r="map/mapToolbar";break;case"indicator":r="indicator/indicatorToolbar";break;case"selector":r="selector/selectorToolbar";break;case"formnode":r="formnode/formnodeToolbar";break;case"nodetable":r="nodeTable/nodetableToolbar";break;case"button":r="button/buttonToolbar";break;case"analyticachart":r="analyticaChart/analyticaChartToolbar";break;case"objectItem":switch(a){case"texteditor":r="texteditor/texteditorToolbar";break;case"cubeviewer":r="cubeviewer/cubeviewerToolbar";break;case"diagramviewer":r="diagramViewer/diagramViewerToolbar";break;case"mapviewer":r="mapViewer/mapViewerToolbar";break;case"menuwidget":r="menuWidget/menuWidgetToolbar";break;case"dashboardcontainer_QUITAR_ESTO_PARA_MOSTRAR":r="dashboardContainer/dashboardContainerToolbar"}break;case"complexchart":r="complexchart/complexChartToolbar";break;default:r=!1}r?Promise.all([t.e(24),t.e(53),t.e(128)]).then(function(){var e=[t(1423)("./"+r)];(function(e){var a=new e({model:n});o(a)}).apply(null,e)}).catch(t.oe):Promise.all([t.e(24),t.e(53),t.e(129)]).then(function(){var e=[t(1435)];(function(e){var a=new e({model:n});o(a)}).apply(null,e)}).catch(t.oe)},getChartItemViewFromType:function(e,a){switch(e){case"empty":Promise.all([t.e(1),t.e(61)]).then(function(){var e=[t(1112)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"linechart":Promise.all([t.e(1),t.e(9),t.e(130)]).then(function(){var e=[t(1436)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"columnchart":Promise.all([t.e(1),t.e(9),t.e(60)]).then(function(){var e=[t(823)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"columnchartstacked":Promise.all([t.e(1),t.e(9),t.e(131)]).then(function(){var e=[t(1437)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"columnchartpercent":Promise.all([t.e(1),t.e(9),t.e(132)]).then(function(){var e=[t(1438)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"barchart":Promise.all([t.e(1),t.e(9),t.e(133)]).then(function(){var e=[t(845)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"barchartstacked":Promise.all([t.e(1),t.e(9),t.e(134)]).then(function(){var e=[t(1439)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"barchartpercent":Promise.all([t.e(1),t.e(9),t.e(135)]).then(function(){var e=[t(1440)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"areachart":Promise.all([t.e(1),t.e(9),t.e(136)]).then(function(){var e=[t(846)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"areachartstacked":Promise.all([t.e(1),t.e(9),t.e(137)]).then(function(){var e=[t(1441)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"areachartpercent":Promise.all([t.e(1),t.e(9),t.e(138)]).then(function(){var e=[t(1442)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"piechart":Promise.all([t.e(1),t.e(9),t.e(139)]).then(function(){var e=[t(1443)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"gaugechart":Promise.all([t.e(1),t.e(9),t.e(140)]).then(function(){var e=[t(1444)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"waterfallchart":Promise.all([t.e(1),t.e(9),t.e(141)]).then(function(){var e=[t(1445)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"scatterchart":Promise.all([t.e(1),t.e(9),t.e(142)]).then(function(){var e=[t(1446)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"complexchart":Promise.all([t.e(1),t.e(9),t.e(143)]).then(function(){var e=[t(1447)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"table":Promise.all([t.e(1),t.e(12),t.e(144)]).then(function(){var e=[t(1448)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"indexlist":Promise.all([t.e(1),t.e(145)]).then(function(){var e=[t(1449)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"map":Promise.all([t.e(33),t.e(1),t.e(12),t.e(89),t.e(146)]).then(function(){var e=[t(1450)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"indicator":Promise.all([t.e(87),t.e(1),t.e(147)]).then(function(){var e=[t(1453)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"selector":Promise.all([t.e(1),t.e(148)]).then(function(){var e=[t(1455)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"formnode":Promise.all([t.e(1),t.e(149)]).then(function(){var e=[t(1458)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"nodetable":Promise.all([t.e(1),t.e(16),t.e(34),t.e(150)]).then(function(){var e=[t(1459)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"button":Promise.all([t.e(1),t.e(151)]).then(function(){var e=[t(1469)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"funnelchart":Promise.all([t.e(1),t.e(9),t.e(152)]).then(function(){var e=[t(1471)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"pyramidchart":Promise.all([t.e(1),t.e(9),t.e(153)]).then(function(){var e=[t(1472)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"analyticachart":Promise.all([t.e(1),t.e(154)]).then(function(){var e=[t(1473)];(function(e){a(e)}).apply(null,e)}).catch(t.oe)}},getObjectItemViewFromType:function(e,a){switch(e){case"texteditor":Promise.all([t.e(1),t.e(88),t.e(155)]).then(function(){var e=[t(1474)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"cubeviewer":Promise.all([t.e(1),t.e(16),t.e(34),t.e(156)]).then(function(){var e=[t(1475)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"diagramviewer":Promise.all([t.e(1),t.e(12),t.e(17),t.e(157)]).then(function(){var e=[t(1476)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"mapviewer":Promise.all([t.e(33),t.e(1),t.e(12),t.e(91),t.e(158)]).then(function(){var e=[t(1477)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"inputform":Promise.all([t.e(1),t.e(16),t.e(35),t.e(159)]).then(function(){var e=[t(1483)];(function(e){a(e)}).apply(null,e)}).catch(t.oe);break;case"dashboardcontainer":Promise.all([t.e(1),t.e(160)]).then(function(){var e=[t(1486)];(function(e){a(e)}).apply(null,e)}).catch(t.oe)}},getFilterView:function(e){t.e(161).then(function(){var a=[t(1487)];(function(a){e(a)}).apply(null,a)}).catch(t.oe)},showCopyDashboard:function(e,a,n){t.e(162).then(function(){var o=[t(1488)];(function(t){(new t).render(e,a,n)}).apply(null,o)}).catch(t.oe)},showDashboardComments:function(e){t.e(163).then(function(){var a=[t(1489)];(function(a){var t=new a;t.setElement(e.parent),t.render(e)}).apply(null,a)}).catch(t.oe)},refreshAllOpenDashboards:function(){o(".mainTask.dashboardTask .btnRefresh").trigger("click")},showTimeFrameSetting:function(e){t.e(164).then(function(){var a=[t(1490)];(function(a){var t=new a(e);t.setElement(e.el),t.render()}).apply(null,a)}).catch(t.oe)},updatePrintReportProgress:function(e){t.e(42).then(function(){var a=[t(1023)];(function(a){new a(e).updatePrintReportProgress()}).apply(null,a)}).catch(t.oe)},updatePrintReportMessage:function(e){t.e(42).then(function(){var a=[t(1023)];(function(a){new a(e).updatePrintReportMessage()}).apply(null,a)}).catch(t.oe)},updatePrintReportComplete:function(e){t.e(42).then(function(){var a=[t(1023)];(function(a){new a(e).updatePrintReportComplete()}).apply(null,a)}).catch(t.oe)}})}.apply(a,r))||(e.exports=i)}).call(this,t(694),t(1))},724:function(e,a,t){"use strict";(function(n,o){var r,i=t(693);void 0===(r=function(){return n.Model.extend({defaults:{dashId:null,dashboardViewList:[],modifiedDash:!1,noQuery:[],styleLibraries:[],nodeOwner:"",extraOptions:void 0},resizeTimeOut:0,getDashboard:function(e,a){(0,i.send)("dashboardManager/by_id/".concat(e,"/"),null,null,function(e){e&&(a(e),o("#summary").trigger("refresh"))})},getNavigator:function(e,a){var t=e.reportId,n=void 0===t?null:t,o=e.dashboardId,r=void 0===o?null:o,c="";n?(c="?report_id=".concat(n),r&&(c+="&dashboard_id=".concat(r))):r&&(c="?dashboard_id=".concat(r)),(0,i.send)("reportManager/getNavigator/".concat(c),null,null,a)},calculateScaleFactor:function(e,a){if(this.getItemsModel().length>0)for(var t=this.getItemsModel(),n=0;n<t.length;n++)t[n].calculateScaleFactor(e,a)},updateSizes:function(e,a){if(this.getItemsModel().length>0){var t=300;a&&(t=1),clearTimeout(this.resizeTimeOut);var n=this.getItemsModel();this.resizeTimeOut=setTimeout(function(){var e;for(e=0;e<n.length;e++)n[e].baseUpdateSize(),n[e].updateSize()},t)}},setStateModified:function(e){this.set({modifiedDash:e})},getStateModified:function(){return this.get("modifiedDash")},addItemToModel:function(e){this.get("dashboardViewList").push(e)},getItemsModel:function(){return this.get("dashboardViewList")},getItemModel:function(e){var a,t=this.getItemsModel();for(a=0;a<t.length;a++)if(t[a].tagId==e)return t[a]},countItemsModelByNodeId:function(e){for(var a=0,t=this.getItemsModel(),n=0;n<t.length;n++)t[n].currentNodeId&&e&&t[n].currentNodeId.toLowerCase()==e.toLowerCase()&&a++;return a},removeItemModel:function(e){var a,t=this.getItemsModel();for(a=0;a<t.length;a++)if(t[a].tagId==e.tagId){t.splice(a,1);break}this.set({dashboardViewList:t})},removeAllItemsModel:function(){this.set("dashboardViewList",[])},changeItemModel:function(e,a){this.removeItemModel(e),this.addItemToModel(a)},setNodeOwner:function(e){this.set("node",e)},getNodeOwner:function(){return this.get("node")},onFilterChange:function(e,a,t,n,o,r){if(o){var i=this.getItemModel(o);if(i&&i.isUnlinkedIndex(e))return void i.onFilterChange(e,a,t,n,!0)}var c=this.getItemsModel();if(c)for(var l=0;l<c.length;l++)c[l].onFilterChange(e,a,t,n,!1,r)},onFiltersChange:function(e){var a=this.getItemsModel();if(a)for(var t=0;t<a.length;t++)a[t].onFiltersChange(e)},synchronizeDrop:function(e,a,t,n,o,r,i){if(i){var c=this.getItemsModel();if(c)for(var l=0;l<c.length;l++)c[l].tagId&&c[l].tagId!=i&&c[l].onSynchronizeDrop(e,a,t,n,o,r)}},synchronizeLevel:function(e,a,t){if(t){var n=this.getItemsModel();if(n)for(var o=0;o<n.length;o++)n[o].tagId&&n[o].tagId!=t&&n[o].onSynchronizeLevel(e,a)}},getNodeFullData:function(e,a,t,n){var o={node:e};a&&(o.fromRow=1,o.toRow=a),(0,i.send)("dashboardManager/getNodeFullData/",o,{type:"GET"},t,n)},getNodeIndexes:function(e,a){(0,i.send)("dashboardManager/getNodeIndexes/",{node:e},null,function(e){e&&a(e)})},getIndexValues:function(e,a){(0,i.send)("dashboardManager/getIndexValues/",e,null,function(e){e&&a(e)})},getGeoDef:function(e,a){(0,i.send)("Dashboard/GetGeoDef/"+e,null,null,function(e){e&&a(e)})},evaluateNode:function(e,a,t,n,o,r,c,l,s,u,d,h,f,p,m){l||(l="sum");var b={node:e,dims:a,rows:t,columns:n,summaryBy:l,bottomTotal:d,rightTotal:h,timeFormat:f,timeFormatType:p,calendarType:m},g="evaluateNode";r&&(g="evaluateNodeDef"),s&&s>0&&u&&u>0&&(b.fromRow=s*(u-1)+1,b.toRow=s*u),(0,i.send)("dashboardManager/".concat(g,"/"),JSON.stringify(b),{type:"POST",contentType:"application/json;charset=utf-8"},o,c)},evaluateNodeForPivot:function(e,a,t,n){(0,i.send)("Dashboard/EvaluateNodeForPivot/",{node:e},{type:"GET"},function(e){var r=e.value,i={success:function(e,t,n){a(e)},complete:function(){o("#mainLoading").hide(),o("#secondLoading").hide(),t()},dataType:"json",progress:function(e){if(e.lengthComputable){var a=e.loaded/e.total*100;n(a)}else try{var t=this.getResponseHeader("X-Content-Length");a=e.loaded/t*100;n(a)}catch(e){}}};o("#secondLoading").show(),o.ajax("".concat(__apiURL,"/scripts/download.aspx?name=").concat(r),i)},t)},updateDefinition:function(e,a,t,n){var r=[];t&&o.each(t,function(e,a){r.push({id:a})});var c={dashboardId:e,definition:a,styles:t};(0,i.send)("dashboardManager/".concat(e,"/"),JSON.stringify(c),{type:"PATCH",contentType:"application/json;charset=utf-8",dataType:"text"},function(e){void 0!=n&&n(e)})},updateDashboardImage:function(e,a,t){var n={id:e,fileData:a};(0,i.send)("Dashboard/UpdateImage/",n,{type:"PUT"},function(a){o("#summary").trigger("refresh"),o("#model-summary").trigger("refresh",{id:e}),a&&t&&t(a)})},validateIndexes:function(e,a){var t=function(a){var t;for(t=0;t<e.length;t++)if(e[t].field==a)return e[t]},n=function(e){var a,n;for(a=0;a<e.length;a++)void 0!=(n=t(e[a].field))&&(e[a].name=n.name)};n(a.dims),n(a.rows),n(a.columns)},initializeDashboardQuery:function(e){this.set("noQuery",e),this._initNoQuery()},_initNoQuery:function(){var e=this.get("noQuery");e&&e.length>0&&o.each(e,function(e,a){a.started=!1})},isReadyForEvaluate:function(e,a){var t=!0,n=this.get("noQuery");return n&&n.length>0&&o.each(n,function(n,o){o.node==e?o.started=!0:0==o.started&&o.rel&&o.rel.indexOf(a)>=0&&(t=!1)}),t},setNodeValueChanges:function(e,a){(0,i.send)("dashboardManager/pivotGrid/setCubeChanges/",JSON.stringify(e),{type:"POST",contentType:"application/json;charset=utf-8"},function(e){a(e),o("body").trigger("pendingChanges",[!0])})},isResultComputed:function(e,a){(0,i.send)("dashboardManager/isResultComputed/",JSON.stringify({nodes:e}),{type:"POST",contentType:"application/json;charset=utf-8"},function(e){a(e)})},reevaluateNodesNeeded:function(e){o(".dashboardTask").trigger("reevaluateNodesNeeded",[e])},reevaluateNodesNeededInThisDashboard:function(e){for(var a=[],t=this.getItemsModel(),n=0;n<t.length;n++){var r=t[n].getNodesOfView();r&&(a=a.concat(r))}a.length>0&&this.isResultComputed(a,function(a){if(a&&a.length>0)for(var n=0;n<t.length;n++)e&&t[n].tagId==e||(a.indexOf(t[n].currentNodeId)>=0&&o(t[n].tagId).trigger("evaluateNodeFromCurrentResult"),t[n].needRefresh(a)&&t[n].refreshItemDash())})},applyNumberFormat:function(e){for(var a=this.getItemsModel(),t=0;t<a.length;t++)a[t].currentNodeId==e&&a[t].applyNumberFormat()},getStyleLibrary:function(e){var a=this.get("styleLibraries");if(a)for(var t=0;t<a.length;t++)if(a[t].id==e)return a[t].definition;return[]},getStyleLibraries:function(){return this.get("styleLibraries")},setStyleLibraries:function(e){return this.set("styleLibraries",e)},refreshStyleLibraries:function(e){var a=this;t.e(62).then(function(){var n=[t(743)];(function(t){(new t).list(null,function(t){a.set("styleLibraries",t),e(t)})}).apply(null,n)}).catch(t.oe)},syncDrilldown:function(e,a,t){var n=this.getItemsModel();if(n)for(var o=0;o<n.length;o++)n[o].tagId!=t&&n[o].syncDrilldown(e,a,t)},syncDrillUp:function(e,a){var t=this.getItemsModel();if(t)for(var n=0;n<t.length;n++)t[n].tagId!=a&&t[n].syncDrillup(e,a)},syncShowHideLegend:function(e,a,t){},viewAsChart:function(e,a){(0,i.send)("Dashboard/viewAsChart/",e,{type:"POST"},a)}})}.apply(a,[]))||(e.exports=r)}).call(this,t(218),t(1))}}]);