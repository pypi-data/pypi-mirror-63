/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[245,246,283],{1084:function(t,e,n){"use strict";(function(a,i){var l,o,s=n(18),r=function(t){return t&&t.__esModule?t:{default:t}}(n(1266));l=[n(746),n(756),n(821),n(1992),n(1993),n(1994),n(1995)],void 0===(o=function(t,e,l,o,u,d,c){return a.View.extend({el:i("#main"),diagram:void 0,nodeFinder:void 0,diagramClipboard:void 0,editor:null,render:function(){var e=this;this._uId=i.uuid();var n={id:this._uId};this.inputModuleModel=new t,this.inputModuleController=new l;var a=o(n);this.$el.append(a),this.listEntities(),this.addHandlers(),this.addTableHandlers(),this.getBase().on("beforeRemoveView",function(t,n){e.onBeforeRemoveView(t,n)}),i(window).resize(function(){e.updateSizes()})},onBeforeRemoveView:function(){i("#entityDefinition").length},updateSizes:function(){var t=this.getBase().find(".groupsInput").height(),e=i("#left .navigation").height();i("#entityDefinition").css("height",e-(325+t))},getBase:function(){return i("div[data-id='"+this._uId+"']")},listEntities:function(){var t=this,e=i(".entityList");e.empty(),this.inputModuleModel.list(function(a){var l=u({data:a});e.append(l);t.getBase().find("table").cubeTable(null,{iDisplayLength:50},"inputForms"),t.getBase().find(".dataTables_scrollBody").css("height",t.h+"px"),n.e(292).then(function(){var e=[n(963)];(function(e){var n={items:[]};i.each(e,function(t,e){n.items.push(e)});var a=c(n);t.getBase().find("div.data-table-options").append(a)}).apply(null,e)}).catch(n.oe)})},addHandlers:function(){var t=this;this.getBase().on("click","div.data-table-options a.btn-addEntity",function(){return t.addEntity(null),!1}),this.getBase().on("click","div.data-table-options a.btn-addInputTemplate",function(){var e=i(this).attr("tmpl");return t.addEntity(e),!1}),this.getBase().on("click",".form-actions button.btn-cancel",function(){return t.close(),!1}),this.getBase().on("click",".form-actions button.btn-save",function(){return t.save(),!1})},addTableHandlers:function(){var t=this;this.getBase().on("click","table button.btn-edit",function(){var e=i(this).attr("data-id");return t.editEntity(e),!1}),this.getBase().on("click","table button.btn-delete",function(){var e=i(this).attr("data-id");n.e(5).then(function(){var a=[n(683)];(function(n){(new n).show({title:(0,s.translate)("remove_entity"),text:(0,s.translate)("confirm_remove_entity"),buttons:[{title:(0,s.translate)("yes"),css:"primary",code:"yes"},{title:(0,s.translate)("no"),code:"no"}],callback:function(n){"yes"==n&&t.deleteEntity(e)}})}).apply(null,a)}).catch(n.oe)}),this.getBase().on("click","table button.btn-generate",function(){var e=i(this).attr("data-id");return t.generateEntity(i(this),e),!1}),this.getBase().on("click","table button.btn-input-data",function(){var e=i(this).attr("data-id"),n=i(this).attr("data-name"),a=i(this).attr("data-code");return t.openForm({templateId:e,templateName:n,templateCode:a}),!1})},close:function(){this.listEntities()},addEntity:function(t){var a=this,l=i(".entityList");l.empty();var o=d();l.append(o),this.updateSizes();var s=new e;t&&Promise.all([n.e(16),n.e(35),n.e(293)]).then(function(){var e=[n(2098)("./"+t)];(function(t){a.editor.set(t)}).apply(null,e)}).catch(n.oe),s.List(__currentSession.companyId,function(t){if(t.length>0){for(var e=[{value:"",text:""}],n=0;n<t.length;n++)e[n]={value:t[n].groupId,text:t[n].name};var l=a.getBase().find("div.form-groups a");l.editable({pk:1,value:null,source:e,placement:"right",success:function(t,e){i(this).attr("data-value",e)}}),l.on("shown",function(){var t=i(this).data("editable").input.$input.closest("form"),e=t.parents("form").eq(0);t.data("validator",e.data("validator"))})}}),n.e(32).then(function(){var t=[n(706)];(function(t){var e=new t,n=""===a.editor.get()?{}:a.editor.get(),l=null===n.workflowGroups||void 0===n.workflowGroups?[]:n.workflowGroups;e.listTaskGroups(function(t){if(t.length>0){for(var e=[{value:"",text:""}],o=0;o<t.length;o++)e[o]={value:t[o].taskGroupId,text:t[o].name};var s=[];for(o=0;o<l.length;o++)s[o]=l[o];var r=a.getBase().find("div.workflow-groups a");r.attr("data-value",s.toString()),r.editable({pk:1,value:s,source:e,placement:"right",success:function(t,e){i(this).attr("data-value",e),(n=""!==a.editor.getText()?JSON.parse(a.editor.getText()):{}).workflowGroups=e,a.editor.set(JSON.parse(JSON.stringify(n,null,"\t")))}}),r.on("shown",function(){var t=i(this).data("editable").input.$input.closest("form"),e=t.parents("form").eq(0);t.data("validator",e.data("validator"))})}})}).apply(null,t)}).catch(n.oe),this.createEditor()},deleteEntity:function(t){var e=this;this.inputModuleModel.delete(t,function(t){e.listEntities()})},generateEntity:function(t,e){var n=this,a=t;i(".entityList").empty(),this.inputModuleModel.generate(e,function(t){(0,s.showMessage)((0,s.translate)("entity_created"),(0,s.translate)("success"),"success",!0),n.listEntities(),a.enable(!1)})},editEntity:function(t){var a=this,l=i(".entityList");l.empty();var o=new e;this.inputModuleModel.get(t,function(t){var e=t.groups;o.List(__currentSession.companyId,function(t){if(t.length>0){for(var n=[{value:"",text:""}],l=0;l<t.length;l++)n[l]={value:t[l].groupId,text:t[l].name};var o=[];for(l=0;l<e.length;l++)o[l]=e[l].groupId;var s=a.getBase().find("div.form-groups a");s.attr("data-value",o.toString()),s.editable({pk:1,value:o,source:n,placement:"right",success:function(t,e){i(this).attr("data-value",e)}}),s.on("shown",function(){var t=i(this).data("editable").input.$input.closest("form"),e=t.parents("form").eq(0);t.data("validator",e.data("validator"))})}}),n.e(32).then(function(){var e=[n(706)];(function(e){var n=new e,l=t.definition,o=void 0===JSON.parse(l).workflowGroups?[]:JSON.parse(l).workflowGroups;n.listTaskGroups(function(t){if(t.length>0){for(var e=[{value:"",text:""}],n=0;n<t.length;n++)e[n]={value:t[n].taskGroupId,text:t[n].name};var s=[];if(o.length>0)for(n=0;n<o.length;n++)s[n]=o[n];var r=a.getBase().find("div.workflow-groups a");r.attr("data-value",s.toString()),r.editable({pk:1,value:s,source:e,placement:"right",success:function(t,e){i(this).attr("data-value",e);var n=JSON.parse(l);n.workflowGroups=e,a.editor.set(n)}}),r.on("shown",function(){var t=i(this).data("editable").input.$input.closest("form"),e=t.parents("form").eq(0);t.data("validator",e.data("validator"))})}})}).apply(null,e)}).catch(n.oe);var s={templateId:t.InputTemplateId,code:t.code,name:t.name,definition:t.definition},r=d(s);l.append(r),setTimeout(function(){a.createEditor(t.definition),a.updateSizes()},100)})},save:function(){var t=this,e=this.getBase().find(".txtId").val(),n=this.getBase().find(".txtCode").val(),a=this.getBase().find(".txtName").val(),i=this.getBase().find(".form-groups a.editable").attr("data-value"),l=t.editor.get(),o=[];if(void 0!==i)for(var s=0;s<i.length;s++)o.push({groupId:i[s]});var r={code:n,name:a,groups:o,definition:JSON.stringify(l,null,"\t")};""!==e&&void 0!==e?(r.InputTemplateId=e,this.inputModuleModel.update(r,function(e){t.listEntities()})):this.inputModuleModel.create(r,function(e){t.listEntities()})},openForm:function(t){this.inputModuleController.openViewer(t)},createEditor:function(t){var e=document.getElementById("entityDefinition");this.editor=new r.default(e,{mode:"tree",modes:["code","form","text","tree","view"]});var n=void 0===t?"":t;""!==(n=(n=n.replace(/\\n/g,"\\n").replace(/\\'/g,"\\'").replace(/\\"/g,'\\"').replace(/\\&/g,"\\&").replace(/\\r/g,"\\r").replace(/\\t/g,"\\t").replace(/\\b/g,"\\b").replace(/\\f/g,"\\f")).replace(/[\u0000-\u0019]+/g,""))&&this.editor.set(JSON.parse(n))}})}.apply(e,l))||(t.exports=o)}).call(this,n(218),n(1))},1992:function(t,e,n){var a=n(690);t.exports=(a.default||a).template({compiler:[8,">= 4.3.0"],main:function(t,e,n,a,i){var l;return'<div data-id="'+t.escapeExpression("function"==typeof(l=null!=(l=n.id||(null!=e?e.id:e))?l:t.hooks.helperMissing)?l.call(null!=e?e:t.nullContext||{},{name:"id",hash:{},data:i,loc:{start:{line:1,column:14},end:{line:1,column:20}}}):l)+'" class="container-fluid mainTask full-horizontal inputModuleTask" data-rel="input-module" data-type="tab-content" >\n\n    <div class="box">\n      <div class="box-content entityList">\n\n      </div>\n    </div>\n\n</div>'},useData:!0})},1993:function(t,e,n){var a=n(690);t.exports=(a.default||a).template({1:function(t,e,a,i,l){var o,s=t.lambda,r=t.escapeExpression;return'      <tr>\n        <td class="templateId">'+r(s(null!=e?e.InputTemplateId:e,e))+"</td>\n        <td >"+r(s(null!=e?e.code:e,e))+"</td>\n        <td >"+r(s(null!=e?e.name:e,e))+'</td>\n        <td>\n            <button class="btn btn-small btn-green btn-edit" data-original-title="Edit" data-id="'+r(s(null!=e?e.InputTemplateId:e,e))+'">\n            <i class="fa fa-pencil-square-o"></i></button>\n            <button class="btn btn-small btn-red btn-delete" data-original-title="Delete" data-id="'+r(s(null!=e?e.InputTemplateId:e,e))+'">\n            <i class="fa fa-trash"></i></button>\n'+(null!=(o=function(t){return t&&(t.__esModule?t.default:t)}(n(689)).call(null!=e?e:t.nullContext||{},null!=e?e.generated:e,"==",!1,{name:"ifCond",hash:{},fn:t.program(2,l,0),inverse:t.program(4,l,0),data:l,loc:{start:{line:21,column:12},end:{line:27,column:23}}}))?o:"")+"        </td>\n      </tr>\n"},2:function(t,e,n,a,i){return'            <button class="btn btn-small btn btn-orange btn-generate" data-original-title="Generate table" data-id="'+t.escapeExpression(t.lambda(null!=e?e.InputTemplateId:e,e))+'">\n            <i class="fa fa-asterisk"></i></button>\n'},4:function(t,e,n,a,i){var l=t.lambda,o=t.escapeExpression;return'            <button class="btn btn-small btn btn-primary btn-input-data" data-original-title="Input data" data-id="'+o(l(null!=e?e.InputTemplateId:e,e))+'" data-name="'+o(l(null!=e?e.name:e,e))+'" data-code="'+o(l(null!=e?e.code:e,e))+'">\n            <i class="fa fa-table"></i></button>\n'},compiler:[8,">= 4.3.0"],main:function(t,e,n,a,i){var l;return'<table id="'+t.escapeExpression(t.lambda(null!=e?e.id:e,e))+'" class="table table-hover table-nomargin table-bordered dataTable dataTable-nosort">\n  <thead>\n    <tr>\n      <th>Id</th>\n      <th>Code</th>\n      <th>Name</th>\n      <th>Actions</th>\n    </tr>\n  </thead>\n  <tbody>\n'+(null!=(l=n.each.call(null!=e?e:t.nullContext||{},null!=e?e.data:e,{name:"each",hash:{},fn:t.program(1,i,0),inverse:t.noop,data:i,loc:{start:{line:11,column:4},end:{line:30,column:13}}}))?l:"")+"  </tbody>\n</table>\n"},useData:!0})},1994:function(t,e,n){var a=n(690);function i(t){return t&&(t.__esModule?t.default:t)}t.exports=(a.default||a).template({1:function(t,e,n,a,i){return'\n    <div class="form-group">\n      <label for="textfield" class="control-label col-sm-2">Id</label>\n      <div class="col-sm-10">\n        <input type="text" class="form-control txtId" value="'+t.escapeExpression(t.lambda(null!=e?e.templateId:e,e))+'">\n      </div>\n    </div>\n\n'},3:function(t,e,n,a,i){var l=t.lambda,o=t.escapeExpression;return'                <div data-value="'+o(l(null!=e?e.groupId:e,e))+'">'+o(l(null!=e?e.name:e,e))+"</div>\n"},compiler:[8,">= 4.3.0"],main:function(t,e,a,l,o){var s,r=null!=e?e:t.nullContext||{},u=t.lambda,d=t.escapeExpression;return"<div class='form-horizontal form-bordered form-validate'>\n\n"+(null!=(s=a.if.call(r,null!=e?e.templateId:e,{name:"if",hash:{},fn:t.program(1,o,0),inverse:t.noop,data:o,loc:{start:{line:3,column:2},end:{line:12,column:9}}}))?s:"")+'\n    <div class="form-group">\n      <label for="textfield" class="control-label col-sm-2">Code</label>\n      <div class="col-sm-10">\n        <input type="text" class="form-control txtCode" value="'+d(u(null!=e?e.code:e,e))+'">\n      </div>\n    </div>\n\n    <div class="form-group">\n      <label for="textfield" class="control-label col-sm-2">Name</label>\n      <div class="col-sm-10">\n        <input type="text" class="form-control txtName" value="'+d(u(null!=e?e.name:e,e))+'">\n      </div>\n    </div>\n\n    <div class="form-group groupsInput">\n      <label for="textfield" class="control-label col-sm-2">User groups</label>\n      <div class="col-sm-10 form-groups">\n        <a href="#" class="editable editable-click" data-type="checklist" data-original-title=\''+d(i(n(688)).call(r,"_groups",{name:"L",hash:{},data:o,loc:{start:{line:31,column:95},end:{line:31,column:110}}}))+"'>\n"+(null!=(s=a.each.call(r,null!=e?e.groups:e,{name:"each",hash:{},fn:t.program(3,o,0),inverse:t.noop,data:o,loc:{start:{line:32,column:12},end:{line:34,column:21}}}))?s:"")+'        </a>\n      </div>\n    </div>\n\n    <div class="form-group groupsInput">\n      <label for="textfield" class="control-label col-sm-2">Workflow groups</label>\n      <div class="col-sm-10 workflow-groups">\n        <a href="#" class="editable editable-click" data-type="checklist" data-original-title=\''+d(i(n(688)).call(r,"_groups",{name:"L",hash:{},data:o,loc:{start:{line:42,column:95},end:{line:42,column:110}}}))+"'>\n"+(null!=(s=a.each.call(r,null!=e?e.groups:e,{name:"each",hash:{},fn:t.program(3,o,0),inverse:t.noop,data:o,loc:{start:{line:43,column:12},end:{line:45,column:21}}}))?s:"")+'        </a>\n      </div>\n    </div>\n\n    \x3c!--div class="form-group">\n      <label for="textfield" class="control-label col-sm-2">Template Type</label>\n      <div class="col-sm-10">\n        <input type="text" class="form-control txtTemplateType">\n      </div>\n    </div--\x3e\n\n    <div class="form-group">\n      <label for="textfield" class="control-label col-sm-2">Definition</label>\n      <div class="col-sm-10">\n        <div id="entityDefinition" style="width: 100%;"></div>\n      </div>\n    </div>\n\n    <div class="form-actions col-sm-offset-2 col-sm-10">\n      <button type="submit" class="btn btn-primary btn-save">Save</button>\n      <button type="button" class="btn btn-cancel">Cancel</button>\n    </div>\n\n</div>'},useData:!0})},1995:function(t,e,n){var a=n(690);t.exports=(a.default||a).template({1:function(t,e,n,a,i){var l,o=null!=e?e:t.nullContext||{},s=t.hooks.helperMissing,r=t.escapeExpression;return'            <li>\n                <a href="#" class="btn-addInputTemplate" tmpl="'+r("function"==typeof(l=null!=(l=n.file||(null!=e?e.file:e))?l:s)?l.call(o,{name:"file",hash:{},data:i,loc:{start:{line:9,column:63},end:{line:9,column:71}}}):l)+'">'+r("function"==typeof(l=null!=(l=n.name||(null!=e?e.name:e))?l:s)?l.call(o,{name:"name",hash:{},data:i,loc:{start:{line:9,column:73},end:{line:9,column:81}}}):l)+"</a>\n            </li>\n"},compiler:[8,">= 4.3.0"],main:function(t,e,n,a,i){var l;return'<div class="btn-group newEntityOpts">\n    <a href="#" class="btn btn-addEntity" style="margin-right: 0px;">Add entity</a>\n    <a href="#" data-toggle="dropdown" class="btn dropdown-toggle">\n        <span class="caret"></span>\n    </a>\n    <ul class="dropdown-menu">\n'+(null!=(l=n.each.call(null!=e?e:t.nullContext||{},null!=e?e.items:e,{name:"each",hash:{},fn:t.program(1,i,0),inverse:t.noop,data:i,loc:{start:{line:7,column:8},end:{line:11,column:17}}}))?l:"")+"    </ul>\n</div>"},useData:!0})},746:function(t,e,n){"use strict";(function(a){var i,l=n(693);void 0===(i=function(){return a.Model.extend({url:"inputModule",defaults:{formsViewList:[]},get:function(t,e){(0,l.send)("inputModule/get/"+t,null,{type:"GET"},e)},list:function(t,e){(0,l.send)("inputTemplates/list/",null,{type:"GET"},t,e)},create:function(t,e){(0,l.send)("inputModule/create",t,{type:"POST"},e)},update:function(t,e){(0,l.send)("inputModule/update",t,{type:"PUT"},e)},delete:function(t,e){(0,l.send)("inputModule/delete/"+t,null,{type:"DELETE"},e)},getMetadata:function(t,e){(0,l.send)("inputTemplates/getMetadata/",{id:t},{type:"GET"},e)},generate:function(t,e){(0,l.send)("inputModule/generate/"+t,null,{type:"GET"},e)},getData:function(t,e){(0,l.send)("inputTemplates/getData/",JSON.stringify(t),{type:"POST",contentType:"application/json;charset=utf-8"},e)},setData:function(t,e,n){(0,l.send)("inputTemplates/setData/",JSON.stringify(t),{type:"POST",contentType:"application/json;charset=utf-8"},e,n)},getHistoryChanges:function(t,e){(0,l.send)("inputModule/getHistoryChanges",t,{type:"POST"},e)},addItemToModel:function(t){this.get("formsViewList").push(t)},getItemsModel:function(){return this.get("formsViewList")},getItemModel:function(t){var e,n=this.getItemsModel();for(e=0;e<n.length;e++)if(n[e].tagId==t)return n[e]},removeItemModel:function(t){var e,n=this.getItemsModel();for(e=0;e<n.length;e++)if(n[e].tagId==t.tagId){n.splice(e,1);break}this.set({formsViewList:n})},removeAllItemsModel:function(){this.set("formsViewList",[])},changeItemModel:function(t,e){this.removeItemModel(t),this.addItemToModel(e)},onClick:function(t,e,n,a){(0,l.send)("inputModule/onClick",{param1:t,param2:e},{type:"POST"},n,a)}})}.apply(e,[]))||(t.exports=i)}).call(this,n(218))},756:function(t,e,n){"use strict";(function(a){var i,l=n(693);void 0===(i=function(){return a.Model.extend({list:function(t,e){var n=null!=t?"?company_id=".concat(t):"";(0,l.send)("groups/".concat(n),null,{type:"GET",contentType:"application/json;charset=utf-8",dataType:"text"},e)},get:function(t,e){(0,l.send)("groups/".concat(t,"/"),null,{type:"GET",contentType:"application/json;charset=utf-8",dataType:"text"},e)},update:function(t,e,n){(0,l.send)("groups/".concat(t,"/"),JSON.stringify(e),{type:"PUT",contentType:"application/json;charset=utf-8",dataType:"text"},n)},create:function(t,e){(0,l.send)("groups/",JSON.stringify(t),{type:"POST",contentType:"application/json;charset=utf-8",dataType:"text"},e)},delete:function(t,e){(0,l.send)("groups/".concat(t,"/"),null,{type:"DELETE"},e)},listPermissions:function(t){(0,l.send)("permissions/",null,{type:"GET",contentType:"application/json;charset=utf-8",dataType:"text"},t)},updateGroupPermissions:function(t,e){(0,l.send)("groups/update_groups_permissions/",JSON.stringify(t),{type:"PATCH",contentType:"application/json;charset=utf-8",dataType:"text"},e)}})}.apply(e,[]))||(t.exports=i)}).call(this,n(218))}}]);