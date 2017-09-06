$(function() {
	var clear = null;
	$("#upload").click(function() {
		setTimeout(function() {
			$(".loader").css({
				"display": "block"
			})
		}, 1000);
		clearInterval(clear);
		//		clearInterval(total);
		clear = setInterval(ajax, 5000);
		total = setInterval(totalPage, 1000);
		$(".pageList").fadeIn(1000);
	});
	//page, tplname
	var p = 0; //
	var tplname;
	var tplname = $('option:selected').val();
	//	console.log("----" + tplname)
	var a = [];
	var page = 0;

	function ajax(p = "") {
		if(p != "") page = p;

		$.ajax({
			type: "get",
			url: "http://zrb.gotohard.cn/structdata?page=" + page + "&tplname=" + tplname,
			async: true,
			success: function(e) {
				if(e == 11) {
					page = 0;
				} else if(e == 22) {
					clearInterval(clear);
					alert("结构化已完成！");
				} else {
					$(".loader").css({
						"display": "none"
					});
					var keys = [];
					for(p in e.data[0])
						keys.push(p);
					for(var i = 0; i < e.data.length; i++) {
						for(var j = 0; j < keys.length; j++) {
							a.push("<span class='keyColor'>" + keys[j] + "</span>" + ":" + e.data[i][keys[j]] + '<br/>');
						}
						a.push('<br/>');
					}
					$(".block1").html(a);
					//var a = [];
				}
			}
		});

		$.ajax({
			type: "get",
			url: "http://zrb.gotohard.cn/structdata?page=" + (page + 1) + "&tplname=" + tplname,
			async: true,
			success: function(e) {
				if(e == 11) {
					totalPage = 0;
					page = 0;
				} else if(e == 22) {
					clearInterval(clear);
					clearInterval(total);
					alert("结构化已完成！");
				} else {
					$(".loader").css({
						"display": "none"
					});
					var keys = [];
					//console.log(e.data[0])
					for(p in e.data[0])
						keys.push(p);
					for(var i = 0; i < e.data.length; i++) {
						for(var j = 0; j < keys.length; j++) {
							a.push("<span class='keyColor'>" + keys[j] + "</span>" + ":" + e.data[i][keys[j]] + '<br/>');
						}
						a.push('<br/>');
					}
					$(".block2").html(a);
					//var a = [];
				}
			}
		});
		page = page + 2;
	}
	//ajax();

	//点击“开始结构化”按钮获取参数
	$("#upload").click(function() {
		tplname = $(".tpls option:selected").val();
	});

});

var b = [];

function ajax2(p = "") {
	a = b;
	if(p != "") page = p;

	$.ajax({
		type: "get",
		url: "http://zrb.gotohard.cn/structdata?page=" + page + "&tplname=" + tplname,
		async: true,
		success: function(e) {
			if(e == 11) {
				page = 0;
			} else if(e == 22) {
				clearInterval(clear);
				alert("结构化已完成！");
			} else {
				$(".loader").css({
					"display": "none"
				});
				var keys = [];
				for(p in e.data[0])
					keys.push(p);
				for(var i = 0; i < e.data.length; i++) {
					for(var j = 0; j < keys.length; j++) {
						a.push("<span class='keyColor'>" + keys[j] + "</span>" + ":" + e.data[i][keys[j]] + '<br/>');
					}
					a.push('<br/>');
				}
				$(".block1").html(a);
				//var a = [];
			}
		}
	});

	$.ajax({
		type: "get",
		url: "http://zrb.gotohard.cn/structdata?page=" + (page + 1) + "&tplname=" + tplname,
		async: true,
		success: function(e) {
			if(e == 11) {
				totalPage = 0;
				page = 0;
			} else if(e == 22) {
				clearInterval(clear);
				clearInterval(total);
			} else {
				$(".loader").css({
					"display": "none"
				});
				var keys = [];
				//console.log(e.data[0])
				for(p in e.data[0])
					keys.push(p);
				for(var i = 0; i < e.data.length; i++) {
					for(var j = 0; j < keys.length; j++) {
						a.push("<span class='keyColor'>" + keys[j] + "</span>" + ":" + e.data[i][keys[j]] + '<br/>');
					}
					a.push('<br/>');
				}
				$(".block2").html(a);
				//var a = [];
			}
		}
	});
	page = page + 2;
}
//function ajax3(p="") {
function ajax3(page) {
	var a = [];
	$.ajax({
		type: "get",
		url: "http://zrb.gotohard.cn/structdata?page=" + page + "&tplname=" + tplname,
		async: true,
		success: function(e) {
			if(e == 11) {
				totalPage = 0;
				page = 0;
			} else if(e == 22) {
//				clear = setInterval(ajax, 5000);
				clearInterval(clear);
				clearInterval(total);
			} else {
				
				$("#demo1").css({
					"display": "none"
				});
				$("#demo2").css({
					"display": "none"
				});
				$(".loader").css({
					"display": "none"
				});
				var keys = [];
				//console.log(e.data[0])
				for(p in e.data[0])
					keys.push(p);
				for(var i = 0; i < e.data.length; i++) {
					for(var j = 0; j < keys.length; j++) {
						a.push("<span class='keyColor'>" + keys[j] + "</span>" + ":" + e.data[i][keys[j]] + '<br/>');
					}
					a.push('<br/>');
				}
				$("#main").css({"display":"none"});
//				clearInterval(ajax);
				$(".contentArea").css({"display":"block"});
				$(".contentArea").html(a);
			//	console.log(a);
				//var a = [];
			}
		}
	});
}
//page
function TotalPage() {
	totalPageNum = 0;
	tplname = $(".tpls option:selected").val();
	$.ajax({
		type: "get",
		url: "http://zrb.gotohard.cn/yema?tplname=" + tplname,
		async: true,
		success: function(data) {
			totalPageNum = data;
			totalPageNum = parseInt(totalPageNum);

			$(".pageList li[class=itempage]").remove();
			$(".pageList span").remove();
			if(totalPageNum <= 7) {
				for(var i = 1; i < totalPageNum; i++) {
					$("#nextPage").last().before("<li class='itempage'><a onclick='getData1(" + i + ")' >" + i + "</a></li>")
				}
			} else {

				for(var i = 1; i < 5; i++) {

					$("#nextPage").last().before("<li class='itempage'><a onclick='getData1(" + i + ")' >" + i + "</a></li>")
				}

				$("#nextPage").last().before("<span>" + "..." + "</span>");
				for(var i = totalPageNum - 3; i < totalPageNum; i++) {
					$("#nextPage").last().before("<li class='itempage'><a onclick='getData1(" + i + ")' >" + i + "</a></li>")
				}
			}
		}
	});

}
setInterval(TotalPage, 2000);

var totalPage = 20; //总页数
var pageSize = 5; //分页尺寸
crPage = -1;

function getData1(page) {
	crPage = page; //更新当前选择页
	TotalPage(); //更新总页数
	ajax3(page);

	return page;
}
//首页
$("#indexPage").click(function() {
	getData1(1);
})
//末页
$("#endPage").click(function() {
	getData1(totalPage);
})
//上一页
$("#prePage").click(function() {

	getData1(crPage - 1);
})
//下一页
$("#nextPage").click(function() {
//	if( crPage > )
	getData1(crPage + 1);
})

if(totalPage <= 7) {
	for(var i = 1; i < totalPage; i++) {
		$("#nextPage").last().before("<li class='itempage'><a onclick='getData1(" + i + ")' >" + i + "</a></li>")
	}
} else {
	for(var i = 1; i < 5; i++) {
		$("#nextPage").last().before("<li class='itempage'><a onclick='getData1(" + i + ")' >" + i + "</a></li>")
	}
	//				$("#nextPage").last().before("...");
	$("#nextPage").last().before("<span>" + "..." + "</span>");
	for(var i = totalPage - 3; i < totalPage; i++) {
		$("#nextPage").last().before("<li class='itempage'><a onclick='getData1(" + i + ")' >" + i + "</a></li>")
	}
}
$(".pageList li:eq(2),.pageList li:eq(3),.pageList li:eq(4),.pageList li:eq(5)").click(function() {
	t = $($(".pageList li").get(6)).text()
	currPage = parseInt($(this).text());

	if(currPage < t - 1) {
		if(currPage < 4) currPage = 3;
		currPage += 1;
		if(currPage >= 4) {
			for(var i = 5; i > 1; i--) {
				$($(".pageList li").get(i)).html("<a onclick='getData1(" + currPage + ")' >" + currPage + "</a>")
				currPage = currPage - 1;
			}
		}
	}
})