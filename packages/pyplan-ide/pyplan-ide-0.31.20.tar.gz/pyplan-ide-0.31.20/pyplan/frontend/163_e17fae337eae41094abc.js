/*! Copyright Pyplan 2020. All rights reserved. */
(window.webpackJsonp=window.webpackJsonp||[]).push([[163],{1019:function(n,e,t){"use strict";(function(a){var s,o=t(693);void 0===(s=function(){return a.Model.extend({getComments:function(n,e,t){(0,o.send)("DashboardComment/List/",{dashboardId:n},null,e,t)},createComment:function(n,e,t){(0,o.send)("DashboardComment/Create/",n,{type:"POST"},e,t)}})}.apply(e,[]))||(n.exports=s)}).call(this,t(218))},1020:function(n,e,t){var a=t(690);function s(n){return n&&(n.__esModule?n.default:n)}n.exports=(a.default||a).template({1:function(n,e,a,o,l){var i=null!=e?e:n.nullContext||{},r=n.escapeExpression;return'        <div class="message-text">\n            <textarea name="comment_text" placeholder="Write here..." rows="3"\n                class="input-block-level form-control"></textarea>\n            <button class="btn btn-small btn-satblue btnAddComment"><i class="fa fa-check"></i>\n                '+r(s(t(688)).call(i,"add_comment",{name:"L",hash:{},data:l,loc:{start:{line:28,column:16},end:{line:28,column:35}}}))+"</button>\n            <span> "+r(s(t(688)).call(i,"_or",{name:"L",hash:{},data:l,loc:{start:{line:29,column:19},end:{line:29,column:30}}}))+' </span>\n            <span class="btn btn-small btn-satblue btnDragComment"><i class="fa fa-arrows"></i>\n                '+r(s(t(688)).call(i,"drag_to_indicator",{name:"L",hash:{},data:l,loc:{start:{line:31,column:16},end:{line:31,column:41}}}))+"</span>\n        </div>\n"},compiler:[8,">= 4.3.0"],main:function(n,e,a,o,l){var i,r=null!=e?e:n.nullContext||{};return'<div class="dashboard-comments">\n\n\n\n    <div class="box">\n        <div class="box-title">\n            <h3>\n                <i class="fa fa-comments"></i>\n                '+n.escapeExpression(s(t(688)).call(r,"comments",{name:"L",hash:{},data:l,loc:{start:{line:9,column:16},end:{line:9,column:32}}}))+'\n            </h3>\n            <div class="actions">\n                <button class="btn btn-mini content-refresh btnRefresh"><i class="fa fa-refresh"></i></button>\n                \x3c!--<button class="btn btn-mini content-slideUp"><i class="fa fa-angle-left"></i></button>--\x3e\n            </div>\n        </div>\n        <div class="box-content nopadding  message-list  ">\n\n            <ul class="messages">\n\n            </ul>\n        </div>\n\n'+(null!=(i=s(t(695)).call(r,"add_dashboardcomment",{name:"haveAccess",hash:{},fn:n.program(1,l,0),inverse:n.noop,data:l,loc:{start:{line:23,column:8},end:{line:33,column:23}}}))?i:"")+"\n    </div>\n\n\n\n</div>"},useData:!0})},1021:function(n,e,t){var a=t(690);function s(n){return n&&(n.__esModule?n.default:n)}n.exports=(a.default||a).template({1:function(n,e,a,o,l){var i,r=null!=e?e:n.nullContext||{},m=n.lambda,d=n.escapeExpression;return'\n<li class="'+(null!=(i=a.if.call(r,null!=e?e.iAm:e,{name:"if",hash:{},fn:n.program(2,l,0),inverse:n.program(4,l,0),data:l,loc:{start:{line:3,column:11},end:{line:3,column:46}}}))?i:"")+'" data-itemId="'+d(m(null!=(i=null!=e?e.extraData:e)?i.itemId:i,e))+'">\n    <div class="image">\n        \x3c!--img src="'+d(s(t(718)).call(r,{name:"baseURL",hash:{},data:l,loc:{start:{line:5,column:21},end:{line:5,column:32}}}))+"thumbs/view.ashx?img=users-"+d(m(null!=(i=null!=e?e.user:e)?i.imageUrl:i,e))+'&w=32&h=40&t=crop" width="32" height="40" /--\x3e\n    </div>\n    <span class="time">'+d(s(t(801)).call(r,null!=e?e.createdDate:e,{name:"timeAgo",hash:{},data:l,loc:{start:{line:7,column:23},end:{line:7,column:46}}}))+'</span>\n    <div class="message">\n        <span class="caret"></span>\n        <span class="name">'+d(m(null!=(i=null!=e?e.user:e)?i.fullName:i,e))+"</span>\n        <p>"+d(m(null!=e?e.comment:e,e))+"</p>\n    </div>\n</li>\n\n"},2:function(n,e,t,a,s){return"right"},4:function(n,e,t,a,s){return"left"},compiler:[8,">= 4.3.0"],main:function(n,e,t,a,s){var o;return null!=(o=t.each.call(null!=e?e:n.nullContext||{},e,{name:"each",hash:{},fn:n.program(1,s,0),inverse:n.noop,data:s,loc:{start:{line:1,column:0},end:{line:15,column:9}}}))?o:""},useData:!0})},1489:function(n,e,t){"use strict";(function(a,s){var o,l,i=t(18);o=[t(1019),t(1020),t(1021)],void 0===(l=function(n,e,t){return a.View.extend({el:s("#main"),options:void 0,render:function(n){if(this.options=n,0==this.$el.find(".dashboard-comments").length){var t=e();this.$el.append(t),this.addHandlers(this.$el.find(".dashboard-comments")),this.getComments()}else this.$el.find(".dashboard-comments").trigger("removeCommentView")},getComments:function(){var e=this;(new n).getComments(this.options.dashboardId,function(n){if(n){s.each(n,function(n,e){e.iAm=e.user.userId==__currentSession.userId,e.extraData&&""!=e.extraData&&(e.extraData=s.parseJSON(e.extraData))});var a=t(n);e.$el.find(".dashboard-comments ul").empty(),e.$el.find(".dashboard-comments ul").append(a),e.$el.find(".message-list").animate({scrollTop:e.$el.find(".dashboard-comments ul").height()},1e3),e.addItemsHandlers(e.$el.find(".dashboard-comments"))}})},removeView:function(){this.$el.find(".dashboard-comments").empty(),this.$el.find(".dashboard-comments").remove(),this.$el.find(".btnDragComment").draggable("destroy")},addComment:function(e){var t=this.$el.find(".dashboard-comments"),a=t.find("textarea[name='comment_text']").val();if(a&&""!=a){var s=this,o=new n,l={dashboardId:this.options.dashboardId,comment:a,extraData:JSON.stringify({itemId:e})};o.createComment(l,function(n){t.find("textarea[name='comment_text']").val(""),s.getComments(),(0,i.triggerNodeJsEvent)("AfterCreateDashboardComment",s.options.dashboardId)})}else t.find("textarea[name='comment_text']").focus()},addHandlers:function(n){var e=this;n.on("removeCommentView",function(){e.removeView()}),n.on("addReferencedComment",function(n,t){e.addComment(t)}),n.find(".btnAddComment").on("click",function(){e.addComment()}),n.find(".btnDragComment").draggable({scroll:!1,appendTo:e.options.parent,helper:function(n){return s('<span class="btn btn-small btn-satblue btnDragComment ui-draggable" style="z-index:1000" ><i class="fa fa-arrows-alt"></i> Drop on indicator</span>"')}}),n.find(".btnRefresh").on("click",function(){e.getComments()}),n.on("refreshExternalComments",function(n,t){t==e.options.dashboardId&&e.getComments()})},addItemsHandlers:function(n){n.find("ul.messages li").off(),n.find("ul.messages li").hover(function(){var n=s(this).attr("data-itemId");if(n&&""!=n){var e=s(this).closest(".mainTask");e.find(".pane[data-itemId='"+n+"']").addClass("commented"),e.find(".pane[data-itemId!='"+n+"']").addClass("uncommented")}},function(){s(this).closest(".mainTask").find(".pane").removeClass("commented").removeClass("uncommented")})},timeSince:function(n){var e=Math.floor((new Date-n)/1e3),t=Math.floor(e/31536e3);return t>1?t+" "+(0,i.translate)("years_ago"):(t=Math.floor(e/2592e3))>1?t+" "+(0,i.translate)("months_ago"):(t=Math.floor(e/86400))>1?t+0+(0,i.translate)("days_ago"):(t=Math.floor(e/3600))>1?t+" "+(0,i.translate)("hours_ago"):(t=Math.floor(e/60))>1?t+" "+(0,i.translate)("minutes_ago"):(0,i.translate)("right_now")}})}.apply(e,o))||(n.exports=l)}).call(this,t(218),t(1))},801:function(n,e,t){"use strict";var a=t(18);n.exports=function(n){return(0,a.timeAgo)(n)}}}]);