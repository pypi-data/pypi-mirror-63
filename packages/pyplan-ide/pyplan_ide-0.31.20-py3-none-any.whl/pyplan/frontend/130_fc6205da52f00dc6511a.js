/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[130],{1436:function(e,t,i){"use strict";(function(r,n){var l,s;l=[i(727)],void 0===(s=function(e){return e.extend({drawChart:function(e){var t=this,i=this.currentResult;this.applyDefaultProperties(i.itemProperties),i.nodeResult&&this.applyStyleSeries(i.nodeResult);var l=i.itemProperties.axes.xAxis,s=i.itemProperties.axes.yAxis,o=r.extend({},l),a=r.extend({},s);o=this.setAxesRange(o),a=this.setAxesRange(a),o.type="category",o.categories=null,o.title=this.getXTitle(),o.labels.style=this.getLabelsStyle(),a.labels.style=this.getLabelsStyle(),a.labels.formatter=function(){return t.createFormatter(),t.numberFormatter.format(this.value)},o.labels.formatter=function(){return t.columnFormatter?t.columnFormatter.format(this.value):this.value};var u=n.extend(i.itemProperties.tooltip,{formatter:function(){return t.formatTooltip(this)}}),p={chart:{type:"line",zoomType:this.ensureProp(i.itemProperties,"zoom",!1)?"x":"none",reflow:!1,spacingBottom:2,events:{drillup:function(e){t.drillup(e)},drilldown:function(e){t.drilldown(e)}}},plotOptions:{series:{turboThreshold:0},line:{dataLabels:{enabled:this.ensureProp(i.itemProperties.labels,"enabled",!1),style:this.getLabelStyle(),formatter:function(){return t.formatLabel(this)}},marker:{enabled:this.ensureProp(i.itemProperties.markers,"enabled",!0)},events:{legendItemClick:function(e){t.legendClick(e)}}}},title:{floating:!0,text:""},subtitle:{text:""},credits:{enabled:!1},navigation:{buttonOptions:{enabled:!1}},xAxis:o,yAxis:a,tooltip:u,legend:this.getChartLegend(i.itemProperties.legend),series:i.nodeResult?i.nodeResult.series:null,drilldown:{activeAxisLabelStyle:{textDecoration:"none",fontWeight:"normal"},activeDataLabelStyle:{textDecoration:"none",fontWeight:"normal"}}};i.itemProperties.timeChart.active?n(e).highcharts("StockChart",p):n(e).highcharts(p)},applyDefaultProperties:function(e){e.labels||(e.labels={enabled:!1,inside:!1})}})}.apply(t,l))||(e.exports=s)}).call(this,i(1),i(1))}}]);