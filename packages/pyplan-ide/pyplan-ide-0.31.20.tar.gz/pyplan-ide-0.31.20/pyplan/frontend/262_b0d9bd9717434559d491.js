/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[262,5,32],{1287:function(n,e,t){"use strict";(function(a,l){var s,o,i=t(18);s=[t(683),t(706),t(2036),t(2037)],void 0===(o=function(n,e,t,s){return a.View.extend({el:l("#main"),render:function(a){var o=this;o.fromDashboard=!1;var r=void 0,u=!1,c=void 0,d="New task";null!==a&&(o.fromDashboard=!!a.fromDashboard,a.id&&(u=!0,d=a.taskTitle));var m=function(){(new Date).add("d",1);var m=r;c&&(m.histories=c,m.hasHistory=!0);var p=t();(new n).show({title:d,html:p,modalClass:"mediumModal",buttons:[{title:(0,i.translate)("close"),code:"close"}],callback:function(n,e){if("yes"===n){if(!e.find("form").valid())return!1;r&&r.taskId,e.find("input[data-id='name']").val(),e.find("textarea[data-id='description']").val(),parseInt(e.find("select[data-id='code']").val()),e.find("input[data-id='start']").val(),e.find("input[data-id='end']").val(),e.find("input[data-id='progress']").val(),parseInt(e.find("select[data-id='user']").val()),e.find("select[data-id='status']").val(),e.find("textarea[data-id='comment']").val(),e.find("select[data-id='relatedUsers']").chosen().val()}},onLoad:function(n){setTimeout(function(){var t=s(m);n.find("ul.timeline").append(t),l(".ganttTaskEditorHistory").scrollTop(l(".ganttTaskEditorHistory").prop("scrollHeight"));var d=(0,i.haveAccess)("BYPASSWORKFLOWTASKTRANSITIONS");if(r){var p=l("form[id='taskForm']"),f=(0,i.haveAccess)("UPDATEALLWORKFLOWTASKS"),h=(0,i.haveAccess)("UPDATEMYWORKFLOWTASK"),v=(0,i.haveAccess)("UPDATEASSIGNEDWORKFLOWTASKS"),k=parseInt(r.ownerId)===__currentSession.loginId,y=r.userId===__currentSession.loginId;f||(k?h||y&&v||p.find('input, textarea, button[data-code="yes"], select').attr("disabled","disabled"):y&&v||p.find('input, textarea, button[data-code="yes"], select').attr("disabled","disabled"))}else d||n.find("select[data-id='status']").attr("disabled",!0);n.find(".txtComment").on("change, keyup",function(){""===l(this).val()?n.find(".btnSendComment").enable(!1):n.find(".btnSendComment").enable(!0)}),n.find(".btnSendComment").on("click",function(){var t=new e,i=n.find(".txtComment").val(),d={taskId:a.id,comment:i};u&&t.createComment(d,function(e){n.find(".txtComment").val(""),t.getTask(a.id,function(e){r=e,c=o.createHistory(e);var t=s({histories:c});n.find("ul.timeline").empty(),n.find("ul.timeline").append(t),l(".ganttTaskEditorHistory").scrollTop(l(".ganttTaskEditorHistory").prop("scrollHeight"))})})})},500),(0,i.postRender)(n)},onClose:function(n){o.destroy(n)}})};u?(new e).getTask(a.id,function(n){r=n,c=o.createHistory(n),m()}):m()},createHistory:function(n){var e;if(n&&n.history&&n.comments&&(n.history.length>0||n.comments.length>0)){e=[];for(var t=-1,a=0;a<n.history.length;a++){var l=n.history[a].date.substring(0,10),s=n.history[a].date,o={};if(0==a)o.historyDate=l,o.items=[{created:!0,userFullName:n.history[a].userFullName,taskUserFullName:n.history[a].taskUserFullName}],e.push(o),t=n.history[a].taskUserId;else{for(var i=!1,r=0;r<e.length;r++)if(e[r].historyDate==l){o=e[r],i=!0;break}i||(o.historyDate=l,o.items=[],e.push(o)),n.history[a].percent>0&&o.items.push({fullDate:s,userFullName:n.history[a].userFullName,changePercent:!0,percent:n.history[a].percent}),n.history[a].stateId>0&&o.items.push({fullDate:s,userFullName:n.history[a].userFullName,changeState:!0,stateName:n.history[a].stateName}),"0001-01-01"!=n.history[a].startDate.substring(0,10)&&o.items.push({fullDate:s,userFullName:n.history[a].userFullName,changeStartDate:!0,startDate:n.history[a].startDate}),"0001-01-01"!=n.history[a].endDate.substring(0,10)&&o.items.push({fullDate:s,userFullName:n.history[a].userFullName,changeEnbDate:!0,endDate:n.history[a].endDate}),t!=n.history[a].taskUserId&&(t=n.history[a].taskUserId,o.items.push({fullDate:s,userFullName:n.history[a].userFullName,changeResponsible:!0,taskUserFullName:n.history[a].taskUserFullName}))}}for(a=0;a<n.comments.length;a++){for(l=n.comments[a].date.substring(0,10),s=n.comments[a].date,i=!1,o={},r=0;r<e.length;r++)if(e[r].historyDate==l){o=e[r],i=!0;break}if(!i){o.historyDate=l,o.items=[];var u=0;for(r=0;r<e.length&&(u=r,!(l<e[r].historyDate));r++);e.splice(u,0,o)}var c={fullDate:s,addComment:!0,comment:n.comments[a].comment,userFullName:n.comments[a].userFullName},d=!1;for(r=0;r<o.items.length;r++){var m=o.items[r];if(c.fullDate<=m.fullDate){o.items.splice(r,0,c),d=!0;break}}d||o.items.push(c)}}return e},destroy:function(n){n.find("input[data-id='code']").select2("destroy"),n.find(".datepick").datepicker("remove")}})}.apply(e,s))||(n.exports=o)}).call(this,t(218),t(1))},2036:function(n,e,t){var a=t(690);n.exports=(a.default||a).template({compiler:[8,">= 4.3.0"],main:function(n,e,t,a,l){return'<div class="box">\n\n  <div class="box-content nopadding">\n\n      <div class="tab-content padding tab-content-inline tab-content-bottom">\n\n\n          <div class="ganttTaskEditorHistory tab-pane active" id="workflowTaskHistoryTab" >\n            \n            <ul class="timeline">\n\n              \n                \n             </ul>\n\n        </div>\n\n      </div>\n\n      <div class="row">\n        <div class="col-sm-11">\n          <textarea class="form-control txtComment" placeholder="Add a comment here..."></textarea>\n        </div>\n        <div class="col-sm-1">\n          <button class="btn btn-primary btnSendComment" disabled="disabled">Send</button>\n        </div>\n      </div>\n  </div>\n</div>\n'},useData:!0})},2037:function(n,e,t){var a=t(690);function l(n){return n&&(n.__esModule?n.default:n)}n.exports=(a.default||a).template({1:function(n,e,a,s,o){var i,r=null!=e?e:n.nullContext||{};return'\n                    <li>\n\n                        <div class="timeline-content">\n                    \n                    <div class="left">\n                                <div class="date">'+n.escapeExpression(l(t(782)).call(r,null!=e?e.historyDate:e,{name:"formatDate",hash:{},data:o,loc:{start:{line:8,column:50},end:{line:8,column:76}}}))+'</div>\n                            </div>\n\n                            <div class="activity">\n\n'+(null!=(i=a.each.call(r,null!=e?e.items:e,{name:"each",hash:{},fn:n.program(2,o,0),inverse:n.noop,data:o,loc:{start:{line:13,column:24},end:{line:45,column:33}}}))?i:"")+'                            </div>\n                        </div>\n\n                       <div class="line"></div>\n\n                  </li>\n\n'},2:function(n,e,t,a,l){var s,o=null!=e?e:n.nullContext||{};return'\n                                    <div class="user">\n\n                              <span class="user">'+n.escapeExpression(n.lambda(null!=e?e.userFullName:e,e))+"</span>\n"+(null!=(s=t.if.call(o,null!=e?e.created:e,{name:"if",hash:{},fn:n.program(3,l,0),inverse:n.noop,data:l,loc:{start:{line:18,column:30},end:{line:21,column:37}}}))?s:"")+(null!=(s=t.if.call(o,null!=e?e.addComment:e,{name:"if",hash:{},fn:n.program(5,l,0),inverse:n.noop,data:l,loc:{start:{line:22,column:30},end:{line:24,column:37}}}))?s:"")+(null!=(s=t.if.call(o,null!=e?e.changeState:e,{name:"if",hash:{},fn:n.program(7,l,0),inverse:n.noop,data:l,loc:{start:{line:25,column:30},end:{line:27,column:37}}}))?s:"")+(null!=(s=t.if.call(o,null!=e?e.changePercent:e,{name:"if",hash:{},fn:n.program(9,l,0),inverse:n.noop,data:l,loc:{start:{line:28,column:30},end:{line:30,column:37}}}))?s:"")+(null!=(s=t.if.call(o,null!=e?e.changeStartDate:e,{name:"if",hash:{},fn:n.program(11,l,0),inverse:n.noop,data:l,loc:{start:{line:31,column:30},end:{line:33,column:37}}}))?s:"")+(null!=(s=t.if.call(o,null!=e?e.changeEnbDate:e,{name:"if",hash:{},fn:n.program(13,l,0),inverse:n.noop,data:l,loc:{start:{line:34,column:30},end:{line:36,column:37}}}))?s:"")+(null!=(s=t.if.call(o,null!=e?e.changeResponsible:e,{name:"if",hash:{},fn:n.program(15,l,0),inverse:n.noop,data:l,loc:{start:{line:37,column:30},end:{line:39,column:37}}}))?s:"")+"                                    </div>\n\n                                      \x3c!--"+(null!=(s=t.if.call(o,null!=e?e.addComment:e,{name:"if",hash:{},fn:n.program(17,l,0),inverse:n.noop,data:l,loc:{start:{line:42,column:42},end:{line:44,column:45}}}))?s:"")+"--\x3e\n"},3:function(n,e,a,s,o){var i=n.escapeExpression;return"                                  <span>"+i(l(t(688)).call(null!=e?e:n.nullContext||{},"task_history_created",{name:"L",hash:{},data:o,loc:{start:{line:19,column:40},end:{line:19,column:68}}}))+'</span>\n                                  <span class="user">'+i(n.lambda(null!=e?e.taskUserFullName:e,e))+"</span>\n"},5:function(n,e,t,a,l){return'                                  : <span class="comment">'+n.escapeExpression(n.lambda(null!=e?e.comment:e,e))+"</span>\n"},7:function(n,e,a,s,o){var i=n.escapeExpression;return"                                  <span>"+i(l(t(688)).call(null!=e?e:n.nullContext||{},"task_history_change_state",{name:"L",hash:{},data:o,loc:{start:{line:26,column:40},end:{line:26,column:73}}}))+'</span><span class="data"> '+i(n.lambda(null!=e?e.stateName:e,e))+"</span>\n"},9:function(n,e,a,s,o){var i=n.escapeExpression;return"                                  <span>"+i(l(t(688)).call(null!=e?e:n.nullContext||{},"task_history_change_percent",{name:"L",hash:{},data:o,loc:{start:{line:29,column:40},end:{line:29,column:75}}}))+'</span><span class="data"> '+i(n.lambda(null!=e?e.percent:e,e))+"%</span>\n"},11:function(n,e,a,s,o){var i=null!=e?e:n.nullContext||{},r=n.escapeExpression;return"                                  <span>"+r(l(t(688)).call(i,"task_history_change_startdate",{name:"L",hash:{},data:o,loc:{start:{line:32,column:40},end:{line:32,column:77}}}))+'</span><span class="data"> '+r(l(t(782)).call(i,null!=e?e.startDate:e,{name:"formatDate",hash:{},data:o,loc:{start:{line:32,column:104},end:{line:32,column:128}}}))+"</span>\n"},13:function(n,e,a,s,o){var i=null!=e?e:n.nullContext||{},r=n.escapeExpression;return"                                  <span>"+r(l(t(688)).call(i,"task_history_change_enddate",{name:"L",hash:{},data:o,loc:{start:{line:35,column:40},end:{line:35,column:75}}}))+'</span><span class="data"> '+r(l(t(782)).call(i,null!=e?e.endDate:e,{name:"formatDate",hash:{},data:o,loc:{start:{line:35,column:102},end:{line:35,column:124}}}))+"</span>\n"},15:function(n,e,a,s,o){var i=n.escapeExpression;return"                                  <span>"+i(l(t(688)).call(null!=e?e:n.nullContext||{},"task_history_change_responsible",{name:"L",hash:{},data:o,loc:{start:{line:38,column:40},end:{line:38,column:79}}}))+'</span><span class="user"> '+i(n.lambda(null!=e?e.taskUserFullName:e,e))+"</span>\n"},17:function(n,e,t,a,l){return"\n                                           <p>"+n.escapeExpression(n.lambda(null!=e?e.comment:e,e))+"</p>\n                                      "},compiler:[8,">= 4.3.0"],main:function(n,e,t,a,l){var s;return null!=(s=t.each.call(null!=e?e:n.nullContext||{},null!=e?e.histories:e,{name:"each",hash:{},fn:n.program(1,l,0),inverse:n.noop,data:l,loc:{start:{line:1,column:0},end:{line:53,column:21}}}))?s:""},useData:!0})},683:function(n,e,t){"use strict";(function(a){var l;void 0===(l=function(){return a.Controller.extend({name:"showModal",show:function(n){Promise.all([t.e(2),t.e(119)]).then(function(){var e=[t(700)];(function(e){(new e).render(n)}).apply(null,e)}).catch(t.oe)}})}.apply(e,[]))||(n.exports=l)}).call(this,t(694))},706:function(n,e,t){"use strict";(function(a){var l,s=t(693);void 0===(l=function(){return a.Model.extend({url:"myFileManager",getWorkflow:function(n,e){var t="Workflow/getWorkflow";n&&(t="Workflow/getWorkflow/"+n),(0,s.send)(t,null,{type:"GET"},e)},createTask:function(n,e){(0,s.send)("Workflow/createTask",n,{type:"POST"},e)},updateTask:function(n,e){(0,s.send)("Workflow/updateTask",n,{type:"PUT"},e)},updateTasksProperty:function(n,e){(0,s.send)("Workflow/updateTasksProperty",n,{type:"PUT"},e)},deleteTask:function(n,e){(0,s.send)("Workflow/deleteTask/"+n,null,{type:"DELETE"},e)},getTask:function(n,e){(0,s.send)("Workflow/getTask/"+n,null,null,e)},createState:function(n,e){(0,s.send)("Workflow/createState/",n,{type:"POST"},e)},listStates:function(n){(0,s.send)("Workflow/listStates",null,{type:"GET"},n)},getState:function(n,e){(0,s.send)("Workflow/getState/"+n,null,{type:"GET"},e)},updateState:function(n,e){(0,s.send)("Workflow/updateState",n,{type:"PUT"},e)},deleteState:function(n,e){(0,s.send)("Workflow/deleteState/"+n,null,{type:"DELETE"},e)},listTransitions:function(n){(0,s.send)("Workflow/listTransitions",null,{type:"GET"},n)},createTransition:function(n,e){(0,s.send)("Workflow/createTransition",n,{type:"POST"},e)},updateTransition:function(n,e){(0,s.send)("Workflow/updateTransition",n,{type:"PUT"},e)},deleteTransition:function(n,e){(0,s.send)("Workflow/deleteTransition/"+n,null,{type:"DELETE"},e)},listUsers:function(n){(0,s.send)("Workflow/listUsers",null,null,n)},getTaskGroup:function(n,e){(0,s.send)("Workflow/getTaskGroup/"+n,null,{type:"GET"},e)},listTaskGroups:function(n){(0,s.send)("Workflow/listTaskGroups",null,{type:"GET"},n)},createTaskGroup:function(n,e){(0,s.send)("Workflow/createTaskGroup",n,{type:"POST"},e)},updateTaskGroup:function(n,e){(0,s.send)("Workflow/updateTaskGroup",n,{type:"PUT"},e)},deleteTaskGroup:function(n,e){(0,s.send)("Workflow/DeleteTaskGroup/"+n,null,{type:"DELETE"},e)},updateOrder:function(n,e){(0,s.send)("Workflow/ChangeOrder",{values:n},{type:"PUT"},e)},updateRolTransitions:function(n,e){(0,s.send)("Workflow/updateRolTransitions",n,{type:"PUT"},e)},getWorkflowByGroups:function(n,e){(0,s.send)("Workflow/getWorkflowByGroups/",{values:n},{type:"POST"},e)},createComment:function(n,e){(0,s.send)("Workflow/createComment/",n,{type:"POST"},e)}})}.apply(e,[]))||(n.exports=l)}).call(this,t(218))},782:function(n,e,t){"use strict";var a=t(18);n.exports=function(n){return(0,a.formatDate)(n)}}}]);