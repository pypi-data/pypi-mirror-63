/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[142],{1446:function(e,t,r){"use strict";(function(i,o){var s,l;s=[r(727)],void 0===(l=function(e){return e.extend({drawChart:function(e){var t=this.currentResult;this.applyDefaultProperties(t.itemProperties);var r=t.itemProperties.axes.xAxis,s=t.itemProperties.axes.yAxis;t.nodeResult&&(r.categories=t.nodeResult.columns.categories);var l=i.extend({},r),n=i.extend({},s);l=this.setAxesRange(l),n=this.setAxesRange(n),l.type="category",l.categories=null;var a=this;l.title=this.getXTitle(),l.labels.style=this.getLabelsStyle(),n.labels.style=this.getLabelsStyle(),n.labels.formatter=function(){return a.createFormatter(),a.numberFormatter.format(this.value)},l.labels.formatter=function(){return a.columnFormatter?a.columnFormatter.format(this.value):this.value};var u=o.extend(t.itemProperties.tooltip,{formatter:function(){return a.formatTooltip(this)}}),c={chart:{type:"scatter",zoomType:this.ensureProp(t.itemProperties,"zoom",!1)?"xy":"none",spacingBottom:2,reflow:!1,events:{drillup:function(e){a.drillup(e)},drilldown:function(e){a.drilldown(e)}}},plotOptions:{series:{turboThreshold:5e3},scatter:{dataLabels:{enabled:this.ensureProp(t.itemProperties.labels,"enabled",!1),style:this.getLabelStyle(),formatter:function(){return a.formatLabel(this)}},tooltip:{},marker:{radius:5,states:{hover:{enabled:!0,lineColor:"rgb(100,100,100)"}}},states:{hover:{marker:{enabled:!1}}},events:{legendItemClick:function(e){a.legendClick(e)}}}},title:{floating:!0,text:""},subtitle:{text:t.itemProperties.subtitle.text},credits:{enabled:!1},navigation:{buttonOptions:{enabled:!1}},xAxis:l,yAxis:n,tooltip:u,legend:this.getChartLegend(t.itemProperties.legend),series:t.nodeResult?t.nodeResult.series:null,drilldown:{activeAxisLabelStyle:{textDecoration:"none",fontWeight:"normal"},activeDataLabelStyle:{textDecoration:"none",fontWeight:"normal"}}};t.itemProperties.timeChart.active?o(e).highcharts("StockChart",c):o(e).highcharts(c)},applyDefaultProperties:function(e){e.labels||(e.labels={enabled:!1,inside:!1})}})}.apply(t,s))||(e.exports=l)}).call(this,r(1),r(1))}}]);