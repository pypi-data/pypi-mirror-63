/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[72,283],{1282:function(n,t,e){"use strict";(function(a,l){var o,i,s=e(18);o=[e(756),e(709),e(723),e(1934)],void 0===(i=function(n,t,o,i){return a.View.extend({el:l("#main"),_uId:"",render:function(){l("#mainLoading").show(),l("div[data-rel='abm-group']").remove();var a,c,d=new n,u=this;this._uId=l.uuid(),a=this.options.groupId?new Promise(function(n,t){d.get(u.options.groupId,function(t){var e={id:u._uId,dataRel:"abm-group",tmpClass:"group-edit",title:(0,s.translate)("_editGroup")},a={group:t,isSuper:__currentSession.userIsSuperUser};n({dataBaseTemplate:e,dataUniqTemplate:a})})}):new Promise(function(n,t){n({dataBaseTemplate:{id:u._uId,dataRel:"abm-group",tmpClass:"group-create",title:(0,s.translate)("_newGroup")},dataUniqTemplate:{isSuper:__currentSession.userIsSuperUser}})}),c=new Promise(function(n,t){e.e(23).then(function(){var t=[e(725)];(function(t){(new t).list(function(t){n(t)})}).apply(null,t)}).catch(e.oe)}),Promise.all([a,c]).then(function(n){var e=n[1],a=n[0].dataBaseTemplate,c=n[0].dataUniqTemplate;c.companies=e.results;var d=t(a),r=o(),p=i(c);u.$el.append(d),l("div[data-id='"+u._uId+"']").find("div.abm-content").append(r),l("div[data-id='"+u._uId+"']").find("div.form-content").append(p),l("div[data-id='"+u._uId+"']").find("div.group-code input").removeAttr("disabled");l("div[data-id='"+u._uId+"'] div.company-id select");(0,s.postRender)(u.$el.find("div[data-id='"+u._uId+"']")),u.addHandlers(),l("#mainLoading").hide()})},save:function(){var t=this._uId,a=l("div[data-id='".concat(t,"']")).find("form");if(!l(a).validate().errorList.length>0){var o=l("div[data-id='".concat(t,"']")).find("div.group-name input").val(),i=l("div[data-id='".concat(t,"']")).find("div.company-id select").val(),s=l("div[data-id='".concat(this._uId,"']")).find("div.template-id select").val(),c=new n,d={name:o};"-"!==s&&(d.permission_template=s),__currentSession.userIsSuperUser&&(d.company_id=i),this.options.groupId?c.update(this.options.groupId,d,function(){Promise.resolve().then(function(){var n=[e(777)];(function(n){(new n).show()}).apply(null,n)}).catch(e.oe)}):c.create(d,function(){Promise.resolve().then(function(){var n=[e(777)];(function(n){(new n).show()}).apply(null,n)}).catch(e.oe)})}},cancel:function(){Promise.resolve().then(function(){var n=[e(777)];(function(n){(new n).show()}).apply(null,n)}).catch(e.oe)},addHandlers:function(){l(".warning").hide();var n=l("div[data-id='".concat(this._uId,"']")).find("div.template-id select");n.on("change",function(t){l(".warning").toggle("-"!==n.val())}),l("div[data-id='".concat(this._uId,"']")).find("form").on("submit",l.proxy(function(){return this.save(),!1},this)),l("div[data-id='".concat(this._uId,"']")).find("div.submit button.btn-cancel").on("click",l.proxy(function(){return this.cancel(),!1},this)),l("div[data-id='".concat(this._uId,"']")).find("div.abm-top-options a.btn-close").on("click",this.cancel)}})}.apply(t,o))||(n.exports=i)}).call(this,e(218),e(1))},1934:function(n,t,e){var a=e(690);function l(n){return n&&(n.__esModule?n.default:n)}n.exports=(a.default||a).template({1:function(n,t,a,o,i,s,c){var d,u=null!=t?t:n.nullContext||{};return'<div class="form-group">\n    <label for="textfield" class="col-sm-2 control-label">'+n.escapeExpression(l(e(688)).call(u,"_company",{name:"L",hash:{},data:i,loc:{start:{line:3,column:58},end:{line:3,column:74}}}))+'</label>\n    <div class="col-sm-10">\n        <div class="col-sm-4 company-id">\n            <select class="form-control" data-rule-required="true">\n'+(null!=(d=a.each.call(u,null!=t?t.companies:t,{name:"each",hash:{},fn:n.program(2,i,0,s,c),inverse:n.noop,data:i,loc:{start:{line:7,column:16},end:{line:9,column:25}}}))?d:"")+"            </select>\n        </div>\n    </div>\n</div>\n"},2:function(n,t,a,o,i,s,c){var d,u=n.lambda,r=n.escapeExpression;return'                <option value="'+r(u(null!=t?t.id:t,t))+'" '+(null!=(d=l(e(689)).call(null!=t?t:n.nullContext||{},null!=t?t.id:t,"==",null!=(d=null!=c[1]?c[1].group:c[1])?d.company:d,{name:"ifCond",hash:{},fn:n.program(3,i,0,s,c),inverse:n.noop,data:i,loc:{start:{line:8,column:39},end:{line:8,column:96}}}))?d:"")+">"+r(u(null!=t?t.name:t,t))+"</option>\n"},3:function(n,t,e,a,l){return" selected "},compiler:[8,">= 4.3.0"],main:function(n,t,a,o,i,s,c){var d,u=null!=t?t:n.nullContext||{},r=n.escapeExpression;return(null!=(d=a.if.call(u,null!=t?t.isSuper:t,{name:"if",hash:{},fn:n.program(1,i,0,s,c),inverse:n.noop,data:i,loc:{start:{line:1,column:0},end:{line:14,column:7}}}))?d:"")+'<div class="form-group">\n    <label for="textfield" class="col-sm-2 control-label">'+r(l(e(688)).call(u,"_permissionsTemplate",{name:"L",hash:{},data:i,loc:{start:{line:16,column:58},end:{line:16,column:86}}}))+'</label>\n    <div class="col-sm-10">\n        <div class="col-sm-4 template-id">\n            <select class="form-control">\n                <option value="-">(Optional) Choose a template ...</option>\n                <option value="pyplan_admin">Pyplan Admin</option>\n                <option value="company_admin">Company Admin</option>\n                <option value="company_user">Company User</option>\n            </select>\n        </div>\n        <div class="warning">'+r(l(e(688)).call(u,"_overridePermissions",{name:"L",hash:{},data:i,loc:{start:{line:26,column:29},end:{line:26,column:57}}}))+'</div>\n    </div>\n</div>\n</div>\n<div class="form-group">\n    <label for="textfield" class="col-sm-2 control-label">'+r(l(e(688)).call(u,"_name",{name:"L",hash:{},data:i,loc:{start:{line:31,column:58},end:{line:31,column:71}}}))+'</label>\n    <div class="col-sm-10">\n        <div class="col-sm-5 group-name">\n            <input type="text" value="'+r(n.lambda(null!=(d=null!=t?t.group:t)?d.name:d,t))+'" class="form-control" name="groupname" data-rule-required="true"\n                data-rule-minlength="3">\n        </div>\n    </div>\n</div>'},useData:!0,useDepths:!0})},709:function(n,t,e){var a=e(690);n.exports=(a.default||a).template({compiler:[8,">= 4.3.0"],main:function(n,t,e,a,l){var o,i=null!=t?t:n.nullContext||{},s=n.hooks.helperMissing,c=n.escapeExpression;return'<div class="abm-base-tmp '+c("function"==typeof(o=null!=(o=e.tmpClass||(null!=t?t.tmpClass:t))?o:s)?o.call(i,{name:"tmpClass",hash:{},data:l,loc:{start:{line:1,column:25},end:{line:1,column:37}}}):o)+' container-fluid mainTask" data-id="'+c("function"==typeof(o=null!=(o=e.id||(null!=t?t.id:t))?o:s)?o.call(i,{name:"id",hash:{},data:l,loc:{start:{line:1,column:73},end:{line:1,column:79}}}):o)+'" data-rel="'+c("function"==typeof(o=null!=(o=e.dataRel||(null!=t?t.dataRel:t))?o:s)?o.call(i,{name:"dataRel",hash:{},data:l,loc:{start:{line:1,column:91},end:{line:1,column:102}}}):o)+'" data-type="tab-content">\n    <div class="row">\n        <div class="col-sm-12">\n            <div class="box">\n                <div class="box-title">\n                    <h3><i class="fa fa-th-list"></i>'+c("function"==typeof(o=null!=(o=e.title||(null!=t?t.title:t))?o:s)?o.call(i,{name:"title",hash:{},data:l,loc:{start:{line:6,column:53},end:{line:6,column:62}}}):o)+'</h3>\n                    <div class="actions abm-top-options">\n                        <a href="#" class="btn btn-close"><i class="fa fa-times"></i></a>\n                    </div>\n                </div>\n        <div class="box-content nopadding abm-content">\n\n                </div>\n            </div>\n        </div>\n    </div>\n</div>\n'},useData:!0})},723:function(n,t,e){var a=e(690);function l(n){return n&&(n.__esModule?n.default:n)}n.exports=(a.default||a).template({compiler:[8,">= 4.3.0"],main:function(n,t,a,o,i){var s=null!=t?t:n.nullContext||{},c=n.escapeExpression;return'<form action="#" id="baseForm" method="POST" class=\'form-horizontal form-bordered form-validate\' novalidate="novalidate">\n    <div class="form-content">\n\n    </div>\n    <div class="submit form-actions col-sm-12">\n        <button type="submit" class="btn btn-primary btn-save">'+c(l(e(688)).call(s,"_save",{name:"L",hash:{},data:i,loc:{start:{line:6,column:63},end:{line:6,column:76}}}))+'</button>\n        <button type="button" class="btn btn-cancel">'+c(l(e(688)).call(s,"cancel",{name:"L",hash:{},data:i,loc:{start:{line:7,column:53},end:{line:7,column:67}}}))+"</button>\n    </div>\n</form>\n"},useData:!0})},756:function(n,t,e){"use strict";(function(a){var l,o=e(693);void 0===(l=function(){return a.Model.extend({list:function(n,t){var e=null!=n?"?company_id=".concat(n):"";(0,o.send)("groups/".concat(e),null,{type:"GET",contentType:"application/json;charset=utf-8",dataType:"text"},t)},get:function(n,t){(0,o.send)("groups/".concat(n,"/"),null,{type:"GET",contentType:"application/json;charset=utf-8",dataType:"text"},t)},update:function(n,t,e){(0,o.send)("groups/".concat(n,"/"),JSON.stringify(t),{type:"PUT",contentType:"application/json;charset=utf-8",dataType:"text"},e)},create:function(n,t){(0,o.send)("groups/",JSON.stringify(n),{type:"POST",contentType:"application/json;charset=utf-8",dataType:"text"},t)},delete:function(n,t){(0,o.send)("groups/".concat(n,"/"),null,{type:"DELETE"},t)},listPermissions:function(n){(0,o.send)("permissions/",null,{type:"GET",contentType:"application/json;charset=utf-8",dataType:"text"},n)},updateGroupPermissions:function(n,t){(0,o.send)("groups/update_groups_permissions/",JSON.stringify(n),{type:"PATCH",contentType:"application/json;charset=utf-8",dataType:"text"},t)}})}.apply(t,[]))||(n.exports=l)}).call(this,e(218))}}]);