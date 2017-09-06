$(function() {
	//设置搜索框样式
	$("#header input[type='search']").focus(function() {
		var email_txt = $(this).val();
		if(email_txt == this.defaultValue) {
			$(this).val("");
		}
	});
	$("#header input").blur(function() {
		var email_txt = $(this).val();
		if(email_txt == "") {
			$(this).val(this.defaultValue);
		}
	});
	
	//设置搜索按钮和停止按钮的鼠标滑过样式
	$(".SerButton").mouseover(function(){
		$(".SerButton").addClass("SerButton_hover");
	});
	$(".SerButton").mouseout(function(){
		$(".SerButton").removeClass("SerButton_hover");
	});
	$(".StopButton").mouseover(function(){
		$(".StopButton").addClass("StopButton_hover");
	});
	$(".StopButton").mouseout(function(){
		$(".StopButton").removeClass("StopButton_hover");
	});
	
	//设置点击“GO”按钮的效果
	$("#SerButton").click(function(){
		$("#header").animate({"margin": '5px auto 5px auto'},100);
		$("#content").fadeIn(1000);
	});
	var h = $("#content").height();
	
	$("#main textarea").css({"height":h});
	

});