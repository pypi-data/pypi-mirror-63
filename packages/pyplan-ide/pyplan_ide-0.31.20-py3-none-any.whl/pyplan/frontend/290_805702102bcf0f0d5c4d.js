/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[290],{2094:function(e,n,o){"use strict";(function(t,i){var a,r,s=o(18);a=[o(752),o(2095)],void 0===(r=function(e,n){return t.View.extend({el:i("#main"),diagram:void 0,render:function(){var e=this,o=n();i("#nodeDocumentationTab").append(o),this.$el=i(".nodeDocumentationTab"),this.instanceSummernote(),this.$el.on("clickNode",function(n,o){var t=o.nodeFullData,a=o.nodeProperties;e.nodeFullData=t,e.nodeProperties=a,i(".overlapDisable").show(),e.loadData()}),i(".nodeDocumentationTab").on("updateSizes",function(n){e.updateSizes()}),i(".nodeDocumentationTab .doc-description").css("width","100%"),i(".nodeDocumentationTab .note-editor.panel.panel-default").css("width","100%"),e.updateSizes(),e.addHandlers()},updateSizes:function(){if(i(".nodeDocumentationTab")){var e=i(".mainTask.influence-diagram .dockInfluenceDiagramProperty").height(),n=i(".mainTask.influence-diagram .dockInfluenceDiagramProperty").width();i(".nodeDocumentationTab").height(e-110),i(".note-editor.panel.panel-default").width(n-50);var o=8;i("#nodeDocumentationTab .note-toolbar").is(":visible")&&(o=i(".note-toolbar.panel-heading").height()+8),i(".note-editable.panel-body").height(e-110-o),i(".note-editing-area").height(e-110-o),i(".note-editable").height(i(".note-editing-area").height()-20)}},loadData:function(){var e="";if(this.options.dic[this.nodeFullData.id]){i(".btnsConfirmChanges").show(),i(".moreChangesContainer").show(),i("body").trigger("pendingChanges",[!0]);var n=this.options.dic[this.nodeFullData.id].properties.find(function(e){return"description"===e.name});n&&(e=n.value)}else{var o=this.nodeProperties.properties.find(function(e){return"description"===e.name});o&&(e=o.value),i(".btnsConfirmChanges").hide(),i.isEmptyObject(this.options.dic)&&i(".moreChangesContainer").hide()}i(".doc-description").summernote("code",e),i(".overlapDisable").hide()},instanceSummernote:function(){var e=this;i(".doc-description").summernote({focus:!0,height:100,dialogsInBody:!0,disableResizeEditor:!0,placeholder:(0,s.translate)("_desc_here"),callbacks:{onInit:function(){i(i(".note-toolbar")[0]).find('button[aria-label="Picture"]').remove(),i(i(".note-toolbar")[0]).find('button[aria-label="Video"]').remove(),i(i(".note-toolbar")[0]).find('button[aria-label="Full Screen"]').remove()},change:function(){}}}),i(".doc-description").on("summernote.change",function(n,o,t){var a=e.nodeProperties.node;if(e.options.dic[a])for(var r in e.options.dic[a].properties)"description"===e.options.dic[a].properties[r].name&&(e.options.dic[a].properties[r].value=o);else if((void 0!=e.nodeFullData.description||null!=o)&&e.nodeFullData.description!==o){for(var s in e.options.dic[a]=e.nodeProperties,e.options.dic[a].properties)"description"===e.options.dic[a].properties[s].name&&(e.options.dic[a].properties[s].value=o);i(".btnsConfirmChanges").show(),i(".moreChangesContainer").show(),i("body").trigger("pendingChanges",[!0])}})},openDocumentation:function(e){o.e(15).then(function(){var n=[o(751)];(function(n){(new n).show(e.nodeFullData.id)}).apply(null,n)}).catch(o.oe)},addHandlers:function(){var e,n=this,o=this.$el.find("textarea");o.keyup(function(o){var t=i(o.currentTarget).val();if(e!==t&&void 0!==e){var a=i(o.currentTarget).attr("data-rel");n.updateNodeProperty(n.nodeProperties,a,t)}}),o.focusin(function(){e=i(this).val()}),o.mousedown(function(e){e.stopPropagation()})},updateNodeProperty:function(e,n,o){var t=this.nodeProperties.properties.find(function(e){return e.name===n});if(t&&t.value!==o){for(var a in this.options.dic[this.nodeProperties.node]||(this.options.dic[this.nodeProperties.node]=e),this.options.dic[this.nodeProperties.node].properties)this.options.dic[this.nodeProperties.node].properties[a].name===n&&(this.options.dic[this.nodeProperties.node].properties[a].value=o);i(".btnsConfirmChanges").show(),i(".moreChangesContainer").show(),i("body").trigger("pendingChanges",[!0])}},onRemoveView:function(){(0,s.removeResizeEvent)("updateSizes"),this.diagram&&(this.diagram.destroy(),this.diagram=null)}})}.apply(n,a))||(e.exports=r)}).call(this,o(218),o(1))},2095:function(e,n,o){var t=o(690);e.exports=(t.default||t).template({compiler:[8,">= 4.3.0"],main:function(e,n,o,t,i){return'<div class="row nodeDocumentationTab" style="padding: 10px 33px;">\n  <div class="col-sm-12 doc-description"></div>\n</div>'},useData:!0})},752:function(e,n,o){"use strict";(function(t){var i,a=o(693);void 0===(i=function(){return t.Model.extend({url:"knowledgeBase",getPost:function(e,n){(0,a.send)("KnowledgeBase/getPost?nodeId="+e,null,{type:"GET"},n)},search:function(e,n){(0,a.send)("KnowledgeBase/search",e,{type:"POST"},n)},generatePost:function(e,n){(0,a.send)("KnowledgeBase/generatePost?nodeId="+e,null,{type:"POST"},n)},updatePost:function(e,n){(0,a.send)("KnowledgeBase/updatePost",e,{type:"PUT"},n)},deleteAttachedFile:function(e,n){(0,a.send)("KnowledgeBase/deleteDocument?url="+e,null,{type:"DELETE"},n)}})}.apply(n,[]))||(e.exports=i)}).call(this,o(218))}}]);