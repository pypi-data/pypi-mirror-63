/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[232],{1946:function(e,n,t){"use strict";(function(a,o){var s,i,l=t(18),r=t(813);s=[t(219),t(717),t(1947),t(1948)],void 0===(i=function(e,n,t,s){return a.View.extend({el:o("#main"),nodeDic:{},fullPath:"",render:function(e){var n=this,a=t();this.$el.append(a),o("#importModuleModal").on("hidden.bs.modal",function(){n.nodeDic=null,o("#importModuleModal").off("hidden.bs.modal"),o("#importModuleModal").remove()}).modal("show"),o("#importModuleModal").css("z-index","4000"),(0,l.postRender)(o("#importModuleModal")),setTimeout(function(){n.addHandlers(e,o("#importModuleModal")),n.onLoad(o("#importModuleModal"))},200)},onLoad:function(t){var a=this,s=new n;new e;setTimeout(function(){o("#main-modal button.btn-primary").focus()},500),o(".form-wizard").length>0&&o(".form-wizard").formwizard({formPluginEnabled:!1,validationEnabled:!1,focusFirstInput:!1,disableUIStyles:!0,textSubmit:"Finish",submitStepClass:"submit_step",validationOptions:{errorElement:"span",errorClass:"help-block has-error",errorPlacement:function(e,n){n.parents("label").length>0?n.parents("label").after(e):n.after(e)},highlight:function(e){o(e).closest(".form-group").removeClass("has-error has-success").addClass("has-error"),console.log("aaa")},success:function(e){e.addClass("valid").closest(".form-group").removeClass("has-error has-success").addClass("has-success")}},formOptions:{success:function(e){alert("Response: \n\n"+e.say)},dataType:"json",resetForm:!0}});var i=new plupload.Uploader({runtimes:"html5",browse_button:"fromWorkstation",url:"".concat(__apiURL,"/modelManager/uploadFileToTemp/"),headers:{Authorization:"Token ".concat(__currentToken),"session-key":__currentSession.session_key},file_data_name:"files",multi_selection:!1,max_file_size:"0",chunk_size:"10mb",unique_names:!1,filters:{title:"Model files",extensions:"ppl"},flash_swf_url:"js/plupload/plupload.flash.swf",silverlight_xap_url:"js/plupload/plupload.silverlight.xap",multipart_params:{action:"uploadFileToTemp"},init:{PostInit:function(){},FilesAdded:function(e,n){plupload.each(n,function(e){a.getBase().find(".sr-only").html("Uploading file..."),a.getBase().find(".import-progressbar").toggle(),a.getBase().find(".btn-upload").toggle(),i.start()})},UploadProgress:function(e,n){a.getBase().find(".progress-bar").css("width",n.percent+"%")},UploadComplete:function(e,n){setTimeout(function(){a.getBase().find(".importTypeLoading").css("display","none"),a.getBase().find(".importTypeLoading .sr-only").html("File uploaded, going next..."),a.getBase().find("#next").enable(!0),a.getBase().find("#next").click()},2e3)},FileUploaded:function(e,n,t){t&&""!=t.response&&"ok"!=t.response&&(a.fullPath=t.response.slice(1,-1))},Error:function(e,n){(0,l.showMessage)(n.code+": "+n.message,null,"error")}}});i.init(),o("#treeMoveTo").jstree({plugins:["wholerow","types","contextmenu","dnd"],types:{default:{icon:"fa fa-folder"},folder:{icon:"fa fa-folder"},shared:{icon:"fa fa-users"},recent:{icon:"fa fa-clock"},favs:{icon:"fa fa-star"},trash:{icon:"fa fa-trash"},file:{icon:"fa fa-file"},myfolder:{icon:"fa fa-user"},public:{icon:"fa fa-globe"},zip:{icon:"fa-file-archive-o"},modelsPath:{icon:"fa fa-cubes"},model:{icon:"fa fa-cube"}},core:{check_callback:!0,themes:{name:"proton",responsive:!0},data:function(e,n){if("#"===e.id)s.getMainFolders(function(e){null!==e&&(e=a.optimizeStructureForTree(e,"tree"),n.call(this,e)),a.openRootNodes(e)});else{var t=""===e.data.fullPath?"/":e.data.fullPath;s.getFiles(t,function(e){null!==e&&(e=a.optimizeStructureForTree(e,"tree"),n.call(this,e))})}}}}).on("changed.jstree",function(e,n){var i;o("#treeMoveTo").jstree();n.node&&(i=""===n.node.data.fullPath?"/":n.node.data.fullPath,a.moveToPath=i,"model"!==n.node.type?(a.getBase().find("#next").enable(!1),s.getFiles(i,function(e){null!==e&&(e=a.optimizeStructureForTree(e,"tree"))})):("2"===t.find('input[name="radio"]:checked').val()&&a.getBase().find("#next").enable(!0),a.fullPath=i))}).on("create_node.jstree",function(e,n){console.log("saved")})},addHandlers:function(n,t){var a=this;t.find('input[type="radio"]').change(function(){t.find(".fromWorkstationCont").toggle(),t.find(".fromServerCont").toggle()}),t.find("button.resolve").on("click",function(e){e.preventDefault(),a.importModule(t)}),t.find("#next").on("click",function(){o(".form-wizard").formwizard("next")}),o(".form-wizard").bind("before_step_shown",function(e,n){"thirdStep"===n.currentStep&&a.importModule(t)}),t.find("button.finish").on("click",function(e){e.preventDefault(),o("#importModuleModal").modal("hide")}),o(".form-wizard").bind("step_shown",function(e,n){if(n.isLastStep)return!1}),t.find(".btnGenerate").on("click",function(){o(this).prop("disabled","disabled"),t.find(".entry-data select, .entry-data input").prop("disabled","disabled"),t.find(".wait").show(),t.find(".progress").show(),t.find(".error").hide();var a=new e,s=t.find('input[name="radio"]:checked').val();a.exportModuleToFile(n,s,function(e){var n="",a=e.getResponseHeader("Content-Disposition");if(a&&-1!==a.indexOf("attachment")){var o=/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(a);null!=o&&o[1]&&(n=o[1].replace(/['"]/g,""))}if("1"===s){t.find(".wait").hide(),t.find(".progress").hide();var i=new Blob([e.response],{type:"octet/stream"});(0,r.saveAs)(i,n),t.modal("hide")}else t.modal("hide"),(0,l.showMessage)("The module was exported with the name: "+n,(0,l.translate)("_successful_export"),"success",!0)},function(){"1"===s?t.find(".error").show():(t.modal("hide"),(0,l.showMessage)((0,l.translate)("loaderror_tryagain"),(0,l.translate)("_export_error"),"error",!0))})}),t.find(".btnClose").on("click",function(){o(".form-wizard").unbind("before_step_shown"),o("#importModuleModal").modal("hide")})},importModule:function(n){n.find(".loadingResults").show();var t="1"===n.find('input[name="radio"]:checked').val(),a=o(".model-breadcrumb span").attr("data-module-id"),i=[];n.find(".conflictsList table tbody tr").each(function(e){i.push({currentId:o(this).find(".currentId").val(),currentIdchanged:o(this).find(".currentIdChanged").val(),newId:o(this).find(".newId").val(),newIdChanged:o(this).find(".newIdChanged").val()})}),n.find(".conflictsList").empty();var l={moduleFile:this.fullPath,fromTemp:t,importType:n.find('input[name="importType"]:checked').val(),parentModelId:a};i.length>0&&(l.mapData=i),(new e).importModuleFromFile(l,function(e){if(n.find(".loadingResults").hide(),0===e.mapData.length)n.find(".resultInfo").show(),n.find(".resultInfo p").html("Import process was successful."),n.find("#next").hide(),n.find("button.resolve").hide(),n.find("button.btnClose").hide(),n.find("button.finish").show(),o(".mainTask.influence-diagram").trigger("refreshView");else{n.find(".conflictsList").empty();var t={conflicts:e.mapData},a=s(t);n.find(".conflictsList").append(a),n.find(".conflictsList").show(),n.find("#next").hide(),n.find("button.finish").hide(),n.find("button.resolve").show()}},function(e){n.find(".loadingResults").hide(),n.find(".resultInfo").show(),n.find(".resultInfo p").html(e)})},openRootNodes:function(e){var n=setInterval(function(){if(o("#treeMoveTo .jstree-container-ul li").length===e.length){clearInterval(n);var t=0;o("#treeMoveTo .jstree-container-ul li").each(function(){0===t&&o("#treeMoveTo").jstree("select_node",o(this),!1,!0),o("#treeMoveTo").jstree("open_node",o(this)),t++})}},5)},optimizeStructureForTree:function(e,n){for(var t=[],a=0;a<e.length;a++){if(1===e[a].type||0===e[a].type)e[a].children=!0,e[a].type="folder";else{"ppl"!==e[a].data.extension&&t.push(a)}if(0!==e[a].data.specialFolderType)switch(e[a].children=!0,e[a].data.specialFolderType){case 0:e[a].type="folder";break;case 1:e[a].type="myfolder";break;case 2:e[a].type="public";break;case 3:e[a].type="company";break;case 4:e[a].type="modelsPath";break;case 5:e[a].type="shared";break;default:e[a].type="folder"}if(0===e[a].type||2===e[a].type)switch(e[a].data.specialFileType){case 0:e[a].type="file";break;case 1:e[a].type="model";break;case 2:e[a].type="zip";break;default:e[a].type="file"}}if("tree"===n)for(a=0;a<t.length;a++)e.splice(t[t.length-(a+1)],1);return e},getBase:function(){return this.$el.find("#importModuleModal")},exportNode:function(e){}})}.apply(n,s))||(e.exports=i)}).call(this,t(218),t(1))},1947:function(e,n,t){var a=t(690);function o(e){return e&&(e.__esModule?e.default:e)}e.exports=(a.default||a).template({compiler:[8,">= 4.3.0"],main:function(e,n,a,s,i){var l=null!=n?n:e.nullContext||{},r=e.escapeExpression;return'<div id="importModuleModal" class="modal fade scenario-manager" tabindex="-1" role="dialog"\n  aria-labelledby="myModalLabel" aria-hidden="true">\n  <div class="modal-dialog" style="width: 50%;">\n\n    <div class="modal-content">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">x</button>\n        <h3>'+r(o(t(688)).call(l,"_import_module",{name:"L",hash:{},data:i,loc:{start:{line:8,column:12},end:{line:8,column:34}}}))+'</h3>\n      </div>\n\n      <div class="modal-body">\n\n        <div class="box-content">\n          <form action="return false;" class="form-horizontal form-wizard ui-formwizard" id="ss"\n            novalidate="novalidate">\n            <div class="step ui-formwizard-content" id="firstStep" style="display: block;">\n              <ul class="wizard-steps steps-3">\n                <li class="active">\n                  <div class="single-step">\n                    <span class="title">\n                      1</span>\n                    <span class="circle">\n                      <span class="active"></span>\n                    </span>\n                    <span class="description">\n                      Select file\n                    </span>\n                  </div>\n                </li>\n                <li>\n                  <div class="single-step">\n                    <span class="title">\n                      2</span>\n                    <span class="circle">\n                    </span>\n                    <span class="description">\n                      Import type\n                    </span>\n                  </div>\n                </li>\n                <li>\n                  <div class="single-step">\n                    <span class="title">\n                      3</span>\n                    <span class="circle">\n                    </span>\n                    <span class="description">\n                      Results\n                    </span>\n                  </div>\n                </li>\n              </ul>\n              <div class="step-forms">\n\n                <div class="col-sm-12 nopadding entry-data">\n                  <div class="form-group">\n                    <div class="col-sm-12">\n                      <div class="radio">\n                        <label>\n                          <input type="radio" name="radio" value="1" checked="checked"> From workstation\n                        </label>\n                      </div>\n                      <div class="radio">\n                        <label>\n                          <input type="radio" name="radio" value="2"> From server\n                        </label>\n                      </div>\n                    </div>\n                  </div>\n                </div>\n\n                <div class="row">\n                  <div class="col-sm-12 text-center fromWorkstationCont" style="height:280px; width:100%">\n                    <a href="#" id="fromWorkstation" class="btn btn-big btn-green btn-upload"\n                      style="margin-top:80px;">Select a file</a>\n\n                    <div class="progress progress-striped import-progressbar active nodisplay">\n                      <div class="progress-bar" role="progressbar" aria-valuenow="45" aria-valuemin="0"\n                        aria-valuemax="100" style="">\n                        <span class="sr-only"></span>\n                      </div>\n                    </div>\n                  </div>\n\n                  <div class="col-sm-12 fromServerCont nodisplay">\n                    \x3c!-- START: Left column --\x3e\n                    <div id="tree-container" class="col-sm-12 nopadding" style="overflow: scroll; height: 280px;">\n                      <div id="treeMoveTo"></div>\n                    </div>\n                    \x3c!-- END: Left column --\x3e\n                  </div>\n                </div>\n\n              </div>\n            </div>\n            <div class="step ui-formwizard-content" id="secondStep" style="display: none;">\n              <ul class="wizard-steps steps-3">\n                <li>\n                  <div class="single-step">\n                    <span class="title">\n                      1</span>\n                    <span class="circle">\n\n                    </span>\n                    <span class="description">\n                      Select file\n                    </span>\n                  </div>\n                </li>\n                <li class="active">\n                  <div class="single-step">\n                    <span class="title">\n                      2</span>\n                    <span class="circle">\n                      <span class="active"></span>\n                    </span>\n                    <span class="description">\n                      Import type\n                    </span>\n                  </div>\n                </li>\n                <li>\n                  <div class="single-step">\n                    <span class="title">\n                      3</span>\n                    <span class="circle">\n                    </span>\n                    <span class="description">\n                      Results\n                    </span>\n                  </div>\n                </li>\n              </ul>\n              <div class="row" style="height:120px; width:100%">\n                <div class="col-sm-12 nopadding entry-data">\n                  <div class="form-group ">\n                    <div class="col-sm-12">\n                      <div class="radio">\n                        <label>\n                          <input type="radio" name="importType" value="0" checked="checked"> Merge\n                        </label>\n                      </div>\n                      <div class="radio">\n                        <label>\n                          <input type="radio" name="importType" value="2"> Switch\n                        </label>\n                      </div>\n                    </div>\n                  </div>\n                </div>\n              </div>\n              <div class="row importTypeLoading nodisplay" style="height:280px; width:100%">\n                <div class="col-sm-12 text-center">\n                  <i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>\n                </div>\n              </div>\n            </div>\n            <div class="step ui-formwizard-content" id="thirdStep" style="display: none;">\n              <ul class="wizard-steps steps-3">\n                <li>\n                  <div class="single-step">\n                    <span class="title">\n                      1</span>\n                    <span class="circle">\n\n                    </span>\n                    <span class="description">\n                      Select file\n                    </span>\n                  </div>\n                </li>\n                <li>\n                  <div class="single-step">\n                    <span class="title">\n                      2</span>\n                    <span class="circle">\n\n                    </span>\n                    <span class="description">\n                      Import type\n                    </span>\n                  </div>\n                </li>\n                <li class="active">\n                  <div class="single-step">\n                    <span class="title">\n                      3</span>\n                    <span class="circle">\n                      <span class="active"></span>\n                    </span>\n                    <span class="description">\n                      Results\n                    </span>\n                  </div>\n                </li>\n              </ul>\n\n              <div class="row loadingResults">\n                <div class="col-sm-12 text-center">\n                  <i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>\n                </div>\n              </div>\n              <div class="row resultInfo nodisplay">\n                <div class="col-sm-12">\n                  <p></p>\n                </div>\n              </div>\n              <div class="row conflictsList nodisplay">\n\n              </div>\n\n            </div>\n\n            <div class="form-actions nopadding">\n              <button class="btn btn-red btnClose">'+r(o(t(688)).call(l,"cancel",{name:"L",hash:{},data:i,loc:{start:{line:215,column:51},end:{line:215,column:65}}}))+'</button>\n              <input type="button" class="btn btn-primary ui-wizard-content ui-formwizard-button" value="Next"\n                id="next">\n              <button class="btn btn-primary ui-wizard-content ui-formwizard-button finish nodisplay">Finish</button>\n              <button class="btn btn-primary ui-wizard-content ui-formwizard-button resolve nodisplay">Resolve</button>\n            </div>\n          </form>\n        </div>\n\n      </div>\n    </div>\n  </div>\n</div>'},useData:!0})},1948:function(e,n,t){var a=t(690);e.exports=(a.default||a).template({1:function(e,n,t,a,o){var s=e.lambda,i=e.escapeExpression;return'      <tr>\n        <td>\n          <input type="hidden" class="currentId" value="'+i(s(null!=n?n.currentId:n,n))+'" />\n          <input type="text" class="currentIdChanged" value="'+i(s(null!=n?n.currentId:n,n))+'" /></td>\n        <td class="currentName">'+i(s(null!=n?n.currentName:n,n))+'</td>\n        <td>\n          <input type="hidden" class="newId" value="'+i(s(null!=n?n.currentId:n,n))+'" />\n          <input type="text" class="newIdChanged" value="'+i(s(null!=n?n.currentId:n,n))+'" /></td>\n        <td class="newName">'+i(s(null!=n?n.newName:n,n))+"</td>\n      </tr>\n"},compiler:[8,">= 4.3.0"],main:function(e,n,t,a,o){var s;return'<div class="col-sm-12">\n  <p><span><i class="fa fa-exclamation-triangle"></i></span> The following nodes are in conflict with existing nodes. Please resolve these conflicts by changing the ID.</p>\n  <table class="table table-hover table-nomargin table-bordered">\n    <thead>\n      <tr>\n        <th colspan="2" style="background-color: #dff0d8;">Base model</th>\n        <th colspan="2" style="background-color: #f2dede;">New module</th>\n      </tr>\n      <tr>\n        <th width="25%">Current Id</th>\n        <th width="25%">Current Name</th>\n        <th width="25%">New Id</th>\n        <th width="25%">New Name</th>\n      </tr>\n    </thead>\n    <tbody>\n\n'+(null!=(s=t.each.call(null!=n?n:e.nullContext||{},null!=n?n.conflicts:n,{name:"each",hash:{},fn:e.program(1,o,0),inverse:e.noop,data:o,loc:{start:{line:18,column:6},end:{line:29,column:15}}}))?s:"")+"\n    </tbody>\n  </table>\n</div>\n"},useData:!0})},717:function(e,n,t){"use strict";(function(a){var o,s=t(693);void 0===(o=function(){return a.Model.extend({url:"myFileManager",getMainFolders:function(e){(0,s.send)("fileManager/getMainFolders/",null,{type:"GET"},e)},getFiles:function(e,n){(0,s.send)("fileManager/getFiles/?folder=".concat(encodeURIComponent(e)),null,{type:"GET"},n)},createFolder:function(e,n,t){(0,s.send)("fileManager/createFolder/",{folder_path:e,folder_name:n},{type:"POST"},t)},deleteFiles:function(e,n){(0,s.send)("fileManager/deleteFiles/",JSON.stringify({sources:e}),{type:"DELETE",contentType:"application/json",dataType:"text"},n)},renameFiles:function(e,n,t){(0,s.send)("fileManager/renameFile/?source=".concat(encodeURIComponent(e),"&newName=").concat(n),null,{type:"GET"},t)},unzipFile:function(e,n,t){(0,s.send)("fileManager/unzipFile/?source=".concat(e,"&targetFolder=").concat(encodeURIComponent(n)),null,{type:"GET",dataType:"text"},t)},moveFiles:function(e,n,t){var a=e.map(function(e){return"sources=".concat(e)}).join("&");(0,s.send)("fileManager/moveFiles/?".concat(a,"&target=").concat(encodeURIComponent(n)),null,{type:"GET",dataType:"text"},t)},copyToMyWorkspace:function(e,n){(0,s.send)("fileManager/copyToMyWorkspace/?source="+encodeURIComponent(e),null,{type:"GET",dataType:"text"},n)},copyFiles:function(e,n,t){var a=e.map(function(e){return"sources=".concat(e)}).join("&");(0,s.send)("fileManager/copyFiles/?".concat(a,"&target=").concat(encodeURIComponent(n)),null,{type:"GET",dataType:"text"},t)},duplicateFiles:function(e,n){var t=e.map(function(e){return"sources=".concat(e)}).join("&");(0,s.send)("fileManager/duplicateFiles/?".concat(t),null,{type:"GET"},n)},zipFiles:function(e,n){var t=e.map(function(e){return"sources=".concat(e)}).join("&");(0,s.send)("fileManager/zipFiles/?".concat(t),null,{type:"GET",dataType:"text"},n)},downloadFiles:function(e,n){var a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:function(){},o=arguments.length>3&&void 0!==arguments[3]?arguments[3]:function(){},s=arguments.length>4&&void 0!==arguments[4]?arguments[4]:function(){},i=arguments.length>5&&void 0!==arguments[5]?arguments[5]:function(){},l=e.map(function(e){return"sources=".concat(e)}).join("&"),r=new XMLHttpRequest;r.responseType="arraybuffer",r.open("GET","".concat(__apiURL,"/fileManager/download/?").concat(l),!0),r.setRequestHeader("Authorization","Token ".concat(__currentToken)),r.setRequestHeader("session-key",__currentSession?__currentSession.session_key:""),r.onloadstart=a,r.onreadystatechange=function(e){var a=e.currentTarget;a.onprogress=o,a.onerror=i,a.onloadend=s,a.readyState==a.DONE&&(200==a.status?n(a):t.e(18).then(function(){var e=[t(685)];(function(e){(new e).show({title:"ERROR!",text:a.response,notifyType:"error"})}).apply(null,e)}).catch(t.oe))},r.send()},getDepartments:function(e){(0,s.send)("departments/by_current_company/",null,{type:"GET"},e)},getDeniedDepartments:function(e,n){(0,s.send)("departments/denied/?folder=".concat(encodeURIComponent(e)),null,{type:"GET"},n)},setDeniedPath:function(e,n){(0,s.send)("departments/deny_items/",JSON.stringify(e),{type:"POST",contentType:"application/json;charset=utf-8"},n)},optimzeTemplates:function(e,n,t){var a=e.map(function(e){return"sources=".concat(e)}).join("&");(0,s.send)("fileManager/optimizeTemplates/?".concat(a),null,{type:"GET",dataType:"text"},n,t)}})}.apply(n,[]))||(e.exports=o)}).call(this,t(218))},813:function(e,n,t){(function(t){var a,o,s;o=[],void 0===(s="function"==typeof(a=function(){"use strict";function n(e,n,t){var a=new XMLHttpRequest;a.open("GET",e),a.responseType="blob",a.onload=function(){i(a.response,n,t)},a.onerror=function(){console.error("could not download file")},a.send()}function a(e){var n=new XMLHttpRequest;return n.open("HEAD",e,!1),n.send(),200<=n.status&&299>=n.status}function o(e){try{e.dispatchEvent(new MouseEvent("click"))}catch(t){var n=document.createEvent("MouseEvents");n.initMouseEvent("click",!0,!0,window,0,0,0,80,20,!1,!1,!1,!1,0,null),e.dispatchEvent(n)}}var s="object"==typeof window&&window.window===window?window:"object"==typeof self&&self.self===self?self:"object"==typeof t&&t.global===t?t:void 0,i=s.saveAs||("object"!=typeof window||window!==s?function(){}:"download"in HTMLAnchorElement.prototype?function(e,t,i){var l=s.URL||s.webkitURL,r=document.createElement("a");t=t||e.name||"download",r.download=t,r.rel="noopener","string"==typeof e?(r.href=e,r.origin===location.origin?o(r):a(r.href)?n(e,t,i):o(r,r.target="_blank")):(r.href=l.createObjectURL(e),setTimeout(function(){l.revokeObjectURL(r.href)},4e4),setTimeout(function(){o(r)},0))}:"msSaveOrOpenBlob"in navigator?function(e,t,s){if(t=t||e.name||"download","string"!=typeof e)navigator.msSaveOrOpenBlob(function(e,n){return void 0===n?n={autoBom:!1}:"object"!=typeof n&&(console.warn("Deprecated: Expected third argument to be a object"),n={autoBom:!n}),n.autoBom&&/^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(e.type)?new Blob(["\ufeff",e],{type:e.type}):e}(e,s),t);else if(a(e))n(e,t,s);else{var i=document.createElement("a");i.href=e,i.target="_blank",setTimeout(function(){o(i)})}}:function(e,t,a,o){if((o=o||open("","_blank"))&&(o.document.title=o.document.body.innerText="downloading..."),"string"==typeof e)return n(e,t,a);var i="application/octet-stream"===e.type,l=/constructor/i.test(s.HTMLElement)||s.safari,r=/CriOS\/[\d]+/.test(navigator.userAgent);if((r||i&&l)&&"object"==typeof FileReader){var d=new FileReader;d.onloadend=function(){var e=d.result;e=r?e:e.replace(/^data:[^;]*;/,"data:attachment/file;"),o?o.location.href=e:location=e,o=null},d.readAsDataURL(e)}else{var c=s.URL||s.webkitURL,p=c.createObjectURL(e);o?o.location=p:location.href=p,o=null,setTimeout(function(){c.revokeObjectURL(p)},4e4)}});s.saveAs=i.saveAs=i,void 0!==e&&(e.exports=i)})?a.apply(n,o):a)||(e.exports=s)}).call(this,t(14))}}]);