/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[272],{1296:function(e,t,n){"use strict";(function(o,a){var r,s,i=n(18),d=n(813);function c(e){return function(e){if(Array.isArray(e)){for(var t=0,n=new Array(e.length);t<e.length;t++)n[t]=e[t];return n}}(e)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance")}()}r=[n(812),n(2061)],void 0===(s=function(e,t){return o.View.extend({el:a("#main"),selectedIds:[],report_ids:[],dashboard_ids:[],render:function(e){var n=e.dashboard_ids,o=e.report_ids,r=this;this.selectedIds=[].concat(c(n),c(o)),this.report_ids=o,this.dashboard_ids=n;var s={countItems:this.selectedIds.length},d=t(s);this.$el.append(d),a("#exportDashboardModal").on("hidden.bs.modal",function(){a("#exportDashboardModal").off("hidden.bs.modal"),a("#exportDashboardModal").remove()}).modal("show"),a("#exportDashboardModal").css("z-index","4000"),(0,i.postRender)(a("#exportDashboardModal")),setTimeout(function(){r.addHandlers(a("#exportDashboardModal"))},200)},addHandlers:function(e){var t=this;e.find(".btnGenerate").on("click",function(){t.exportDashboard(e)}),e.find(".btnClose").on("click",function(){a("#exportDashboardModal").modal("hide")})},exportDashboard:function(t){this.selectedIds&&this.selectedIds.length>0&&(t.find(".btnGenerate").prop("disabled","disabled"),t.find(".entry-data select, .entry-data input").prop("disabled","disabled"),t.find(".wait").show(),t.find(".progress").show(),(new e).exportDashboards({report_ids:this.report_ids,dashboard_ids:this.dashboard_ids},function(e){var n="dashboards";try{var o=e.getResponseHeader("Content-Disposition");n=o.trim().slice(o.indexOf("filename=")+9)}catch(e){}t.find(".wait").hide(),t.find(".progress").hide();var a=new Blob([e.response],{type:"octet/stream"});(0,d.saveAs)(a,"".concat(n,".json")),t.modal("hide")}))}})}.apply(t,r))||(e.exports=s)}).call(this,n(218),n(1))},2061:function(e,t,n){var o=n(690);function a(e){return e&&(e.__esModule?e.default:e)}e.exports=(o.default||o).template({compiler:[8,">= 4.3.0"],main:function(e,t,o,r,s){var i=null!=t?t:e.nullContext||{},d=e.escapeExpression;return'<div id="exportDashboardModal" class="modal fade scenario-manager generalExportView" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\n    <div class="modal-dialog">\n\n        <div class="modal-content">\n            <div class="modal-header">\n                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">x</button>\n                <h3>'+d(a(n(688)).call(i,"export_dashboards",{name:"L",hash:{},data:s,loc:{start:{line:7,column:20},end:{line:7,column:45}}}))+'</h3>\n            </div>\n\n            <div class="modal-body">\n                '+d(e.lambda(null!=t?t.countItems:t,t))+' item(s) to be exported.\n                <div class="clearfix"></div>\n\n                  <div class="generator">\n\n                    <button class="btn btn-primary btn-small btnGenerate">'+d(a(n(688)).call(i,"generate_file",{name:"L",hash:{},data:s,loc:{start:{line:16,column:74},end:{line:16,column:95}}}))+'</button>\n\n                      <span class="wait export-message nodisplay">'+d(a(n(688)).call(i,"please_wait",{name:"L",hash:{},data:s,loc:{start:{line:18,column:66},end:{line:18,column:85}}}))+'</span>\n\n                      <a class="link export-message nodisplay" href="#" target="_blank" >'+d(a(n(688)).call(i,"click_to_download",{name:"L",hash:{},data:s,loc:{start:{line:20,column:89},end:{line:20,column:114}}}))+'</a>\n\n                    <div class="progress progress-striped active nodisplay">\n                        <div class="progress-bar" style="width: 100%;">\n                        </div>\n                    </div>\n                  </div>\n\n                <div class="controls">\n                    <button class="btn btn-small btnClose ">'+d(a(n(688)).call(i,"close",{name:"L",hash:{},data:s,loc:{start:{line:29,column:60},end:{line:29,column:73}}}))+"</button>\n                </div>\n            </div>\n\n\n        </div>\n    </div>\n</div>\n"},useData:!0})},812:function(e,t,n){"use strict";(function(o){var a,r=n(693);void 0===(a=function(){return o.Model.extend({url:"inputModule",defaults:{formsViewList:[]},search:function(e,t){(0,r.send)("reportManager/search/?text=".concat(e),null,{type:"GET"},t)},getMyReports:function(e,t){(0,r.send)("reportManager/myReports/?parent=".concat(e),null,{type:"GET"},t)},getFavsReports:function(e,t){(0,r.send)("reportManager/myReports/?favs=true",null,{type:"GET"},t)},getReportsSharedWithMe:function(e,t){(0,r.send)("reportManager/sharedWithMe/?parent=".concat(e),null,{type:"GET"},t)},getMySharedReports:function(e,t){(0,r.send)("reportManager/mySharedReports/",null,{type:"GET"},t)},getRecentsReports:function(e,t){(0,r.send)("reportManager/recents/?parent=".concat(e),null,{type:"GET"},t)},exportDashboards:function(e,t){var o=new XMLHttpRequest;o.responseType="arraybuffer",o.open("PUT","".concat(__apiURL,"/reportManager/exportItems/"),!0),o.setRequestHeader("Authorization","Token ".concat(__currentToken)),o.setRequestHeader("session-key",__currentSession?__currentSession.session_key:""),o.setRequestHeader("Content-type","application/json"),o.onreadystatechange=function(e){var o=e.currentTarget;o.readyState==o.DONE&&(200==o.status?t(o):n.e(18).then(function(){var e=[n(685)];(function(e){(new e).show({title:"ERROR!",text:o.response,notifyType:"error"})}).apply(null,e)}).catch(n.oe))},o.send(JSON.stringify(e))},exportItemsAndPublish:function(e,t,n,o,a,s,i){(0,r.send)("reportManager/exportItemsAndPublish/",JSON.stringify({username:e,uuid:t,model_folder:n,model_id:o,dashboard_ids:a,report_ids:s}),{type:"PUT",contentType:"application/json;charset=utf-8"},i)},importDashboards:function(e,t){(0,r.send)("reportManager/importItems/",JSON.stringify(e),{type:"PUT",contentType:"application/json;charset=utf-8"},t)},create:function(e,t){(0,r.send)("reportManager/",e,{type:"POST"},function(e){void 0!=t&&t(e)})},createReport:function(e,t){(0,r.send)("reportManager/",e,{type:"POST"},function(e){void 0!=t&&t(e)})},dropOnReport:function(e,t){(0,r.send)("reportManager/dropOnReport/",JSON.stringify(e),{type:"PUT",contentType:"application/json;charset=utf-8"},t)},updateOrder:function(e){(0,r.send)("reportManager/changeOrder/",JSON.stringify({values:e}),{type:"PUT",contentType:"application/json;charset=utf-8"},function(e){})},setAsFav:function(e,t,n){(0,r.send)("reportManager/setAsFav/",JSON.stringify({report_ids:e.report_ids,dashboard_ids:e.dashboard_ids,is_fav:t}),{type:"PUT",contentType:"application/json;charset=utf-8",dataType:"text"},n)},updateName:function(e,t,n){(0,r.send)("reportManager/".concat(e,"/"),{name:t},{type:"PUT",dataType:"text"},function(e){void 0!=n&&n(e)})},deleteItems:function(e,t){(0,r.send)("reportManager/bulkDelete/",JSON.stringify({values:e}),{type:"DELETE",contentType:"application/json;charset=utf-8"},function(e){void 0!=t&&t(e)})},createTempId:function(){return"tmp-".concat(parseInt(5e5*Math.random()))},copyToMyReports:function(e,t){(0,r.send)("reportManager/copyToMyReports/",JSON.stringify(e),{type:"PUT",contentType:"application/json;charset=utf-8",dataType:"text"},function(e){void 0!=t&&t(e)})},duplicateItems:function(e,t){(0,r.send)("reportManager/duplicateItems/",JSON.stringify(e),{type:"PUT",contentType:"application/json;charset=utf-8",dataType:"text"},function(e){t&&t(e)})}})}.apply(t,[]))||(e.exports=a)}).call(this,n(218))},813:function(e,t,n){(function(n){var o,a,r;a=[],void 0===(r="function"==typeof(o=function(){"use strict";function t(e,t,n){var o=new XMLHttpRequest;o.open("GET",e),o.responseType="blob",o.onload=function(){s(o.response,t,n)},o.onerror=function(){console.error("could not download file")},o.send()}function o(e){var t=new XMLHttpRequest;return t.open("HEAD",e,!1),t.send(),200<=t.status&&299>=t.status}function a(e){try{e.dispatchEvent(new MouseEvent("click"))}catch(n){var t=document.createEvent("MouseEvents");t.initMouseEvent("click",!0,!0,window,0,0,0,80,20,!1,!1,!1,!1,0,null),e.dispatchEvent(t)}}var r="object"==typeof window&&window.window===window?window:"object"==typeof self&&self.self===self?self:"object"==typeof n&&n.global===n?n:void 0,s=r.saveAs||("object"!=typeof window||window!==r?function(){}:"download"in HTMLAnchorElement.prototype?function(e,n,s){var i=r.URL||r.webkitURL,d=document.createElement("a");n=n||e.name||"download",d.download=n,d.rel="noopener","string"==typeof e?(d.href=e,d.origin===location.origin?a(d):o(d.href)?t(e,n,s):a(d,d.target="_blank")):(d.href=i.createObjectURL(e),setTimeout(function(){i.revokeObjectURL(d.href)},4e4),setTimeout(function(){a(d)},0))}:"msSaveOrOpenBlob"in navigator?function(e,n,r){if(n=n||e.name||"download","string"!=typeof e)navigator.msSaveOrOpenBlob(function(e,t){return void 0===t?t={autoBom:!1}:"object"!=typeof t&&(console.warn("Deprecated: Expected third argument to be a object"),t={autoBom:!t}),t.autoBom&&/^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(e.type)?new Blob(["\ufeff",e],{type:e.type}):e}(e,r),n);else if(o(e))t(e,n,r);else{var s=document.createElement("a");s.href=e,s.target="_blank",setTimeout(function(){a(s)})}}:function(e,n,o,a){if((a=a||open("","_blank"))&&(a.document.title=a.document.body.innerText="downloading..."),"string"==typeof e)return t(e,n,o);var s="application/octet-stream"===e.type,i=/constructor/i.test(r.HTMLElement)||r.safari,d=/CriOS\/[\d]+/.test(navigator.userAgent);if((d||s&&i)&&"object"==typeof FileReader){var c=new FileReader;c.onloadend=function(){var e=c.result;e=d?e:e.replace(/^data:[^;]*;/,"data:attachment/file;"),a?a.location.href=e:location=e,a=null},c.readAsDataURL(e)}else{var l=r.URL||r.webkitURL,p=l.createObjectURL(e);a?a.location=p:location.href=p,a=null,setTimeout(function(){l.revokeObjectURL(p)},4e4)}});r.saveAs=s.saveAs=s,void 0!==e&&(e.exports=s)})?o.apply(t,a):o)||(e.exports=r)}).call(this,n(14))}}]);