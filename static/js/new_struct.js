var change = null;
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
var names = []; //模板英文名
var tplname; //模板名
var page; //页码
var footer = document.getElementsByClassName("footer");
var borad = document.getElementsByClassName("borad");
//获取所有可用模板
$.ajax({
	type: "get",
	url: "http://zrb.gotohard.cn/gettpl",
	async: true,
	success: function(tpls) {
//		console.log("返回数据："+tpls.data);
		
		for(var i = 0; i < tpls.data.length; i++) {
			var u = unescape(tpls.data[i].inputName.replace(/\\u/g, '%u'));
			html = "<option>" + u + "</option>";
			$(".tpls").append(html);
			names.push(tpls.data[i].name);
		}
		$(".tpls option").each(function(index) { //遍历全部option  
			$(this).val(tpls.data[index].inputName);
		});
	}
});

$("#upload").click(function() {
	$("#uploadForm").animate({
		"margin": '5px auto 5px auto'
	}, 100);
	$("#content").fadeIn(1000);

	$(".loader").css({
		"display": "block"
	})
	doUpload();

	function doUpload() {
		var i = $('option:selected').index();
		var formData = new FormData($("#uploadForm")[0]);
		tplname = names[i];
		formData.append("select", tplname);
		console.log(formData);
		$.ajax({
			url: 'http://zrb.gotohard.cn/structd',
			type: 'POST',
			data: formData,
			async: true,
			cache: false,
			contentType: false,
			processData: false,
			dataType: "text",
			success: function() {
				clearInterval(change);
				//定时器更改总页数 
				change = setInterval(changeTotole, 3000);
				structPut(0);
				console.log("即将隐藏loader");
				$(".loader").css({
					"display": "none"
				});
				console.log("2");
				changeTotole();
			},
			error: function() {
				alert("提交失败");
			}
		});
	}
})

//url: "http://zrb.gotohard.cn/structdata?page=" + page + "&tplname=" + tplname,
//展示数据
function structPut(p) {
	page = p;
	$.ajax({
		type: "get",
		url: "http://zrb.gotohard.cn/structdata?tplname=" + tplname + "&page=" + page,
		async: true,
		success: function(e) {
			
			borad[0].innerText = "";

			for(var i = 0; i < e.data.length; i++) {
				
				var item = e.data[i]
				for (tkey in item){
					var qkey = tkey.replace(/\\/g, "%");
					zn_key = unescape(qkey);
					var value = item[tkey].replace(/\\/g, "%");
					zn_value = unescape(value);
					
					$(".borad").append("<li>" + zn_key+" :        "+zn_value + "</li>");
				}
//				console.log(e.data[i])
//				var key = e.data[i].replace(/\\/g, "%");
//				var d = $.parseJSON(e.data[i]).replace(/\\/g, "%");
//				var v = unescape(d);
//				console.log(v);
//				$(".borad").append("<li>" + v + "</li>");
				
			}
		}
	});
}

function changeTotole() {
	var last;
	$.ajax({
		type: "GET",
		url: "http://zrb.gotohard.cn/yema?tplname=" + tplname,
		async: false,
		success: function(msg) {
			totalPages = Math.floor(msg/2);
			last = Math.ceil(msg/2);
		}
	});
	$.ajax({
		type: "get",
		url: "http://zrb.gotohard.cn/structdata?tplname=" + tplname + "&page=" + last,
		async: true,
		success: function(e) {
			if( e == 22){
				alert("结构化已完成！");
				clearInterval(change);
			}
		}
	});
	footer[0].style.display = "block";
	var obj = $('#pagination').twbsPagination({
		totalPages: totalPages,
		visiblePages: 10,
		onPageClick: function(event, page) {
			p = page - 1;
			structPut(p);
		}
	});
}