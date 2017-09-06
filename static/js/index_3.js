$("#upload").mouseover(function() {
	$("#upload").addClass("upload_hover");
});
$("#upload").mouseout(function() {
	$("#upload").removeClass("upload_hover");
});
$("#add").mouseover(function() {
	$("#add").addClass("add_hover");
});
$("#add").mouseout(function() {
	$("#add").removeClass("add_hover");
});
var names = [];
//获取所有可用模板
var tplSource = "http://zrb.gotohard.cn/gettpl"
$.ajax({
	type: "get",
	url: tplSource,
	async: true,
	success: function(tpls) {
	//	console.log(tpls.data);
		
		for(var i = 0; i < tpls.data.length; i++) {
			var u = unescape(tpls.data[i].inputName.replace(/\\u/g, '%u')); 
			html = "<option>" +  u+ "</option>";
			$(".tpls").append(html);
			names.push(tpls.data[i].name);
		}
		$(".tpls option").each(function(index) { //遍历全部option  
			$(this).val(tpls.data[index].inputName);
		});
//		console.log($(".tpls option"));
	}
});

function doUpload() {
	var i = $('option:selected').index();
	var formData = new FormData($("#uploadForm")[0]);
	formData.append("select", names[i])
	$.ajax({
		url: 'http://zrb.gotohard.cn/structd',
		type: 'POST',
		data: formData,
		async: true,
		cache: false,
		contentType: false,
		processData: false,
		dataType:"text",
		success: function(returndata) {
			
		},
		error: function(returndata) {
			
			alert("提交失败");
		}
	});
}
$("#upload").click(function() {
	doUpload();
	$("#uploadForm").animate({
		"margin": '5px auto 5px auto'
	}, 100);
	$("#content").fadeIn(1000);
	
})