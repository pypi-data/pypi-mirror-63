/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[133],{845:function(t,e,i){"use strict";(function(s,r){var a,n,l=i(18);a=[i(727)],void 0===(n=function(t){return t.extend({drawChart:function(t){var e=this,i=this.currentResult;this.applyDefaultProperties(i.itemProperties);var a=i.itemProperties.axes.xAxis,n=i.itemProperties.axes.yAxis;i.nodeResult&&this.applyStyleSeries(i.nodeResult);var l=s.extend({},a),o=s.extend({},n);l=this.setAxesRange(l),o=this.setAxesRange(o),l&&l.labels&&0==l.labels.rotation&&l.labels.align&&delete l.labels.align,l.type="category",l.categories=null,l.title=this.getXTitle(),l.labels.style=this.getLabelsStyle(),o.labels.style=this.getLabelsStyle(),o.labels.formatter=function(){return e.createFormatter(),e.numberFormatter.format(this.value)},l.labels.formatter=function(){return e.columnFormatter?e.columnFormatter.format(this.value):this.value};var h=r.extend(i.itemProperties.tooltip,{formatter:function(){return e.formatTooltip(this)}}),p={chart:{type:"bar",zoomType:i.itemProperties.hasOwnProperty("zoom")&&i.itemProperties.zoom?"x":"none",reflow:!1,spacingBottom:2,events:{drillup:function(t){e.drillup(t)},drilldown:function(t){e.drilldown(t)}}},plotOptions:{series:{grouping:!0!==i.itemProperties.grouping,dataLabels:{enabled:this.ensureProp(i.itemProperties.labels,"enabled",!1),inside:i.itemProperties.labels.inside,style:this.getLabelStyle(),formatter:function(){return e.formatLabel(this)}},events:{legendItemClick:function(t){e.legendClick(t)}}}},title:{floating:!0,text:""},subtitle:{text:i.itemProperties.subtitle.text},credits:{enabled:!1},navigation:{buttonOptions:{enabled:!1}},xAxis:l,yAxis:o,tooltip:h,legend:this.getChartLegend(i.itemProperties.legend),series:i.nodeResult?i.nodeResult.series:null,drilldown:{activeAxisLabelStyle:{textDecoration:"none",fontWeight:"normal"},activeDataLabelStyle:{textDecoration:"none",fontWeight:"normal"}}};p=r.extend({},p,this.getExtraChartOptions(p)),this.applyCustomFeatures(p),r(t).highcharts(p)},applyDefaultProperties:function(t){t.labels||(t.labels={enabled:!1,inside:!1})},setPositionForDropDetails:function(){var t=r(this.tagId).find(".drop-area"),e=t.find(".for-column"),i=t.find(".for-row");e.find("span").text((0,l.translate)("drop_axis_here")),i.find("span").text((0,l.translate)("drop_serie_here"));var s=87;r(this.tagId).find("g.highcharts-axis").first().length,this.chart&&this.chart.xAxis&&this.chart.xAxis.length>0&&this.chart.xAxis[0].axisTitle&&this.chart.xAxis[0].axisTitle.textStr&&(s+=25),i.css("left",s+"px").css("top","30px"),i.width(t.width()-10-s),i.height(t.height()-70),e.css("left","5px").css("top","30px"),e.width(s-5),e.height(t.height()-70)},applyCustomFeatures:function(t){}})}.apply(e,a))||(t.exports=n)}).call(this,i(1),i(1))}}]);