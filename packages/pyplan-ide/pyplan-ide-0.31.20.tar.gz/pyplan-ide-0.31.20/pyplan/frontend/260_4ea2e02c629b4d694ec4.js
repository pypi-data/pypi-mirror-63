/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[260],{2022:function(n,l,a){"use strict";(function(e,o){var t,i;t=[a(987),a(2023)],void 0===(i=function(n,l){return e.View.extend({el:o("#main"),render:function(a,e){this.$el.find("#main-modal").remove();var t=n(a);this.$el.append(t);var i=l();o("#main-modal .modal-body").html(i),o("#main-modal .modal-footer button").click(function(){var n=!0;return a.callback&&a.callback()&&(n=!1),n&&(o("#main-modal").off("shown"),o("#main-modal").modal("hide")),!1}),o("#main-modal").on("shown",function(){o("#main-modal button.btn-primary").focus()}),o("#main-modal").on("hidden.bs.modal",function(){o("#main-modal").off("hidden"),a.hasOwnProperty("onClose")&&a.onClose(o("#main-modal")),o("#main-modal").remove()});var d=null;a.backdrop&&(d={backdrop:"static",keyboard:!1}),o("#main-modal").modal(d),a.hasOwnProperty("onLoad")&&a.onLoad(o("#main-modal")),this.initUploader(e,a)},initUploader:function(n,l){n=n;var a=new plupload.Uploader({runtimes:"html5,flash,silverlight,html4",browse_button:"pickfiles",container:document.getElementById("container"),url:"".concat(__apiURL,"/scripts/uploader.ashx"),filters:{max_file_size:"10mb",mime_types:[{title:"Image files",extensions:"jpg,gif,png"},{title:"Zip files",extensions:"zip"}]},flash_swf_url:"/plupload/js/Moxie.swf",silverlight_xap_url:"/plupload/js/Moxie.xap",init:{PostInit:function(){var n=this;o("#main-modal .modal-footer button.btn-primary").on("click",function(){n.setOption({multipart_params:{targetPath:"",action:"knowledgeDocument",token:__currentToken,knowledgeBaseId:l.postId}}),a.start()})},FilesAdded:function(n,l){plupload.each(l,function(n){o(".note-image-url").html('<div id="'+n.id+'">'+n.name+" ("+plupload.formatSize(n.size)+") <b></b></div>")})},FileUploaded:function(l,a,e){var t="".concat(__apiURL,"/").concat(e.response).concat(a.name);o(".summernoteFullDesc").summernote("insertImage",t,a.name),n()}}});a.init()}})}.apply(l,t))||(n.exports=i)}).call(this,a(218),a(1))},2023:function(n,l,a){var e=a(690);n.exports=(e.default||e).template({compiler:[8,">= 4.3.0"],main:function(n,l,a,e,o){var t;return'<div id="insert-image" data-id="'+n.escapeExpression("function"==typeof(t=null!=(t=a.id||(null!=l?l.id:l))?t:n.hooks.helperMissing)?t.call(null!=l?l:n.nullContext||{},{name:"id",hash:{},data:o,loc:{start:{line:1,column:32},end:{line:1,column:38}}}):t)+'" class="box-content nopadding abm-content">\n  <div id="container">\n\n    <button class="btn btn-primary" id="pickfiles">Select file</button>\n    <br /><br />\n\n    <label>Image selected: </label><br />\n    <span class="note-image-url col-md-12"></span><br>\n\n  </div>\n</div>\n'},useData:!0})},987:function(n,l,a){var e=a(690);n.exports=(e.default||e).template({1:function(n,l,a,e,o){var t,i=null!=l?l:n.nullContext||{},d=n.hooks.helperMissing,s=n.escapeExpression;return'                <button class="btn btn-'+s("function"==typeof(t=null!=(t=a.css||(null!=l?l.css:l))?t:d)?t.call(i,{name:"css",hash:{},data:o,loc:{start:{line:14,column:39},end:{line:14,column:46}}}):t)+'" data-code="'+s("function"==typeof(t=null!=(t=a.code||(null!=l?l.code:l))?t:d)?t.call(i,{name:"code",hash:{},data:o,loc:{start:{line:14,column:59},end:{line:14,column:67}}}):t)+'" data-dismiss="modal" aria-hidden="true">'+s("function"==typeof(t=null!=(t=a.title||(null!=l?l.title:l))?t:d)?t.call(i,{name:"title",hash:{},data:o,loc:{start:{line:14,column:109},end:{line:14,column:118}}}):t)+"</button>\n"},compiler:[8,">= 4.3.0"],main:function(n,l,a,e,o){var t,i,d=null!=l?l:n.nullContext||{},s=n.hooks.helperMissing,c=n.escapeExpression;return'<div id="main-modal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="display: none;">\n  <div class="modal-dialog '+c("function"==typeof(i=null!=(i=a.modalClass||(null!=l?l.modalClass:l))?i:s)?i.call(d,{name:"modalClass",hash:{},data:o,loc:{start:{line:2,column:27},end:{line:2,column:41}}}):i)+'">\n      <div class="modal-content">\n        <div class="modal-header">\n                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">x</button>\n                <h4 class="modal-title" id="myModalLabel">'+c("function"==typeof(i=null!=(i=a.title||(null!=l?l.title:l))?i:s)?i.call(d,{name:"title",hash:{},data:o,loc:{start:{line:6,column:58},end:{line:6,column:67}}}):i)+'</h4>\n        </div>\n\n            <div class="modal-body" style="overflow-y:auto; overflow-x: hidden;">\n                <p>'+c("function"==typeof(i=null!=(i=a.text||(null!=l?l.text:l))?i:s)?i.call(d,{name:"text",hash:{},data:o,loc:{start:{line:10,column:19},end:{line:10,column:27}}}):i)+'</p>\n            </div>\n            <div class="modal-footer">\n'+(null!=(t=a.each.call(d,null!=l?l.buttons:l,{name:"each",hash:{},fn:n.program(1,o,0),inverse:n.noop,data:o,loc:{start:{line:13,column:16},end:{line:15,column:25}}}))?t:"")+"            </div>\n    </div>\n  </div>\n</div>\n"},useData:!0})}}]);