var two = null;
var one = null;
var box = document.getElementById("box");
var cheack = document.getElementById("cheack");
var nav = document.getElementById("nav");
var main = document.getElementById("main");
var taskUrls = [];
var taskNames = [];
var taskStatuss = [];
var data = new Object();
var signs; //可删除
var taskName; //站名
var datas; //从服务器获取的数据包
var totalPages; //数据总页数
var myscroll = document.getElementsByClassName("myscroll");
var footer = document.getElementsByClassName("footer")[0];
var Puase = document.getElementById("Puase");
var SerButton = document.getElementById("SerButton");
var StopButton = document.getElementById("StopButton");
var borad = document.getElementsByClassName("borad");
var add;
var j = 0;
var p = 0;
//点击go按钮之后
$("#SerButton").click(function() {
	//console.log("点击了开始按钮，清除一下定时器");
	//如果从停止状态或暂停状态，转为开始状态，先取消定时器
	clearInterval(one);
	clearInterval(two);
	clearInterval(pChart1);
	clearInterval(pChart2);
	//等待框
	setTimeout(function() {
		$(".loader").css({
			"display": "block"
		});
		$(".tips").css({
			"display": "block"
		});
	}, 650);

	var begin = $("#header select").val(); //选取http(s)
	var start = begin + $("#header input[type=search]").val(); //获取网址
	var number = $("#header input[type=number]").val(); //获取线程数

	var url = begin + 'zrb.gotohard.cn/run?num=' + number + '&start=' + start; //传递的url值
	//console.log("爬取接口：" + url);
	//调用运行爬虫接口
	$.ajax({
		type: "get",
		url: url,
		async: true,
		success: function(result) {
			//			alert(result.taskname);
			taskName = result.taskname;
			if(taskName !== "") {
				j = 0;
				$(".tips span")[0].innerText = "正在爬取中，  ";
				$(".tips span")[1].innerText = result.path;
				charts2(); //请求数  2秒后执行
				charts1(); //数据条数  2秒后执行
				two = setInterval(getdata, 5000); //获取数据  5秒后执行
				$(SerButton).prop("disabled", true);
				SerButton.style.cursor = "not-allowed";
				$(StopButton).prop("disabled", false);
				StopButton.style.cursor = "pointer";
				$(Puase).prop("disabled", false);
				Puase.style.cursor = "pointer";
				if(myscroll[0].style.display = "none") { //如果麻雀在显示，那么就麻雀隐藏
					myscroll[0].style.display = "block";
				}
				footer.style.display = "none";
				
			}

		},
		error: function() {
			alert("爬取失败！");
		}
	});

});
//点击结束按钮
$("#StopButton").click(function() {
	//console.log("点击了结束按钮，清除一下定时器");
	clearInterval(pChart1); //取消
	clearInterval(pChart2);
	clearInterval(one);
	clearInterval(two);
	$.ajax({
		type: "get",
		url: "http://zrb.gotohard.cn/stop?url_domain=" + taskName,
	});
	$.ajax({
		type: "GET",
		url: "http://zrb.gotohard.cn/getdata/items?url_domain=" + taskName,
		async: false,
		success: function(msg) {
			totalPages = Math.floor(msg / 20);
		}
	});
	myscroll[0].style.display = "none";
	var obj = $('#pagination').twbsPagination({
		totalPages: totalPages,
		visiblePages: 10,
		onPageClick: function(event, page) {
			p = page - 1;
			dataPage(p);
		}
	});

	footer.style.display = "block";
	$(".tips span")[0].innerText = "爬虫已結束，  ";
	$(SerButton).prop("disabled", false);
	SerButton.style.cursor = "pointer";
	$(StopButton).prop("disabled", true);
	StopButton.style.cursor = "not-allowed";
	$(Puase).prop("disabled", false);
	Puase.style.cursor = "pointer";
});
$("#Puase").click(function() {
	//console.log("点击了暂停按钮，清除一下定时器");
	clearInterval(pChart1); //取消
	clearInterval(pChart2);
	clearInterval(one);
	clearInterval(two);
	$.ajax({
		type: "get",
		url: "http://zrb.gotohard.cn/pause?url_domain=" + taskName,
	});
	if(myscroll[0].style.display = "true") { //如果麻雀在显示，那么就麻雀隐藏
		myscroll[0].style.display = "none";
	}
	$.ajax({
		type: "GET",
		url: "http://zrb.gotohard.cn/getdata/items?url_domain=" + taskName,
		async: false,
		success: function(msg) {
			totalPages = Math.floor(msg / 20);
		}
	});
	footer.style.display = "block";
	var obj = $('#pagination').twbsPagination({
		totalPages: totalPages,
		visiblePages: 10,
		onPageClick: function(event, page) {
			p = page - 1;
			dataPage(p);
		}
	});
	$(SerButton).prop("disabled", false);
	SerButton.style.cursor = "pointer";
	$(StopButton).prop("disabled", false);
	StopButton.style.cursor = "pointer";
	$(Puase).prop("disabled", true);
	Puase.style.cursor = "not-allowed";
	$(".tips span")[0].innerText = "爬虫已暂停，  ";
});

function changeData() {
//	console.log("ajax2 index changeData插入数据 " + new Date());
	add = datas[j];
	$(".myscroll ul li:last-child").html(add);
	j++;
}

function getdata() {
	//console.log("ajax2 index getdata获取数据" + new Date())
	//	return 
	var max;
	$.ajax({
		type: "get",
		url: "http://zrb.gotohard.cn/getdata/items?url_domain=" + taskName,
		async: true,
		success: function(m) {
			max = Math.floor(m / 20);
			$.ajax({
				type: "get",
				url: "http://zrb.gotohard.cn/getdata/getdata?url_domain=" + taskName + "&page=" + p,
				async: true,
				success: function(e) {
					datas = e.data;
					clearInterval(one);
					one = setInterval(changeData, 250); //插入数据
					document.getElementsByClassName("loader")[0].style.display = "none";
					//			alert("数据获取成功");
				},
				error: function() {
					alert('数据获取失败');
				}
			});
			if(p > max) {
				j = 0;
				return false;
			} else {
				p = p + 1;
				j = 0;
			}
		}
	});

}

$('#cheack').click(function() { //侧边任务栏
	$.ajax({
		type: "get",
		url: "http://zrb.gotohard.cn/task/task",
		async: true,
		success: function(e) {
			data = e;
			show(data);
		}
	});
	var sideWidth = box.style.left;
	if(sideWidth == "0px") {
		$(box).animate({
			left: '-455'
		}); //admin-footer
	} else {
		$(box).animate({
			left: '0'
		}); //admin-footer
	}
});

function show(data) {
	nav.innerHTML = "";
	taskUrls = [];
	taskNames = [];
	taskStatuss = [];
	taskNums = [];
	data.data.forEach(function(target) {
		var target = JSON.parse(target);
		taskUrls.push(target.taskUrl);
		taskNames.push(target.taskName);
		taskStatuss.push(target.taskStatus);
		taskNums.push(target.taskNum)
	})
	for(var j = 0; j < taskStatuss.length; j++) {
		var k = String(taskUrls[j]);
		var v = String(taskNames[j]);
		var u = String(taskStatuss[j]);
		var t = String(taskNums[j]);
		var html = "<div class='list'><div class='taskName'></div><div class='taskStatus'></div><div class='taskNum'></div></div>";
		$("#nav").append(html);
		document.getElementsByClassName("taskName")[j].innerText = v;
		if(u == 0) {
			document.getElementsByClassName("taskStatus")[j].innerText = "已结束";
		} else if(u == 1) {
			document.getElementsByClassName("taskStatus")[j].innerText = "暂停中";
		} else if(u == 2) {
			document.getElementsByClassName("taskStatus")[j].innerText = "运行中";
		}

		document.getElementsByClassName("taskNum")[j].innerText = t;
	}
	set();
}

function set() { //设置页面的内容
	$(".list").click(function() {
		var sideWidth = box.style.left;
		if(sideWidth == "0px") {
			$(box).animate({
				left: '-455'
			}); //admin-footer
		} else {
			$(box).animate({
				left: '0'
			}); //admin-footer
		}
		signNum = $(this).index();
		//		console.log(signNum);
		$("#header input[type=search]")[0].value = taskUrls[signNum].replace(/http(s)?:\/\//g, "");
		taskName = taskNames[signNum];
		//console.log("设置了tackName为： " + taskName);
		$("#header input[type=number]")[0].value = taskNums[signNum];
		ButTask(signNum);
	});
}

function ButTask(signNum) {

	$("#header").animate({
		"margin": '5px auto 5px auto'
	}, 100);
	$("#content").fadeIn(1000);
	var i = taskStatuss[signNum];
	//	console.log(i);
	if(i == 1) { //爬虫暂停中
		//		document.getElementById("charts1").style.display = "none";
		//		document.getElementById("charts2").style.display = "none";
		//		document.getElementById("p1").style.display = "none";
		//		document.getElementById("p2").style.display = "none";
		if(document.getElementById("charts1").style.display == "none") {
			document.getElementById("charts1").style.display = "block";
			document.getElementById("charts2").style.display = "block";
			document.getElementById("p1").style.display = "block";
			document.getElementById("p2").style.display = "block";
			charts2();
			charts1();
		}
		document.getElementsByClassName("loader")[0].style.display = "none";
		$(".tips span")[1].innerText = "/var/www/zrbspider/zrbspider/web/" + taskName;
		$.ajax({
			type: "GET",
			url: "http://zrb.gotohard.cn/getdata/items?url_domain=" + taskName,
			async: false,
			success: function(msg) {
				totalPages = Math.floor(msg / 20);
			}
		});
		var obj = $('#pagination').twbsPagination({
			totalPages: totalPages,
			visiblePages: 10,
			onPageClick: function(event, page) {
				p = page - 1;
				dataPage(p);
			}
		});
		$("#header").animate({
			"margin": '5px auto 5px auto'
		}, 100);
		if(myscroll[0].style.display = "true") { //如果麻雀在显示，那么就麻雀隐藏
			myscroll[0].style.display = "none";
		}
		$("#content").fadeIn(1000);
		setTimeout(function() {
			$(".tips").css({
				"display": "block"
			});
			footer.style.display = "block";
		}, 650);
		$(".tips span")[0].innerText = "爬虫已暂停，  ";
		$("loader p").html("数据读取中...");
		clearInterval(pChart1);
		clearInterval(pChart2);
		clearInterval(one); //获取数据
		clearInterval(two); //插入数据
		dataPage(p);

		$(SerButton).prop("disabled", false);
		SerButton.style.cursor = "pointer";
		$(Puase).prop("disabled", true);
		Puase.style.cursor = "not-allowed";
		$(StopButton).prop("disabled", true);
		StopButton.style.cursor = "not-allowed";
	} else if(i == 0) { //爬虫结束
		//		document.getElementById("charts1").style.display = "block";
		//		document.getElementById("charts2").style.display = "block";
		//		document.getElementById("p1").style.display = "block";
		//		document.getElementById("p2").style.display = "block";
		if(document.getElementById("charts1").style.display == "none") {
			document.getElementById("charts1").style.display = "block";
			document.getElementById("charts2").style.display = "block";
			document.getElementById("p1").style.display = "block";
			document.getElementById("p2").style.display = "block";
			charts2();
			charts1();
		}
		document.getElementsByClassName("loader")[0].style.display = "none";
		$(".tips span")[1].innerText = "/var/www/zrbspider/zrbspider/web/" + taskName;
		$.ajax({
			type: "GET",
			url: "http://zrb.gotohard.cn/getdata/items?url_domain=" + taskName,
			async: false,
			success: function(msg) {
				totalPages = Math.floor(msg / 20);
			//	console.log(totalPages);
			}
		});
		var obj = $('#pagination').twbsPagination({
			totalPages: totalPages,
			visiblePages: 10,
			onPageClick: function(event, page) {
				p = page - 1;
				dataPage(p);
			}
		});
		$("#header").animate({
			"margin": '5px auto 5px auto'
		}, 100);
		if(myscroll[0].style.display = "true") { //如果麻雀在显示，那么就麻雀隐藏
			myscroll[0].style.display = "none";
		}
		$("#content").fadeIn(1000);
		setTimeout(function() {
			$(".tips").css({
				"display": "block"
			});
			footer.style.display = "block";
		}, 650);
		$(".tips span")[0].innerText = "爬虫已结束，  ";
		$("loader p").html("数据读取中...");
		setTimeout(function() {
			clearInterval(pChart1);
			clearInterval(pChart2);
			clearInterval(one);
			clearInterval(two);
		}, 1000);
		dataPage(p);
		$(SerButton).prop("disabled", false);
		SerButton.style.cursor = "pointer";
		$(Puase).prop("disabled", true);
		Puase.style.cursor = "not-allowed";
		$(StopButton).prop("disabled", true);
		StopButton.style.cursor = "not-allowed";
	} else if(i == 2) { //爬虫进行中
		$("#header").animate({
			"margin": '5px auto 5px auto'
		}, 100);
		j = 0;
		$("#content").fadeIn(1000);
		clearInterval(one);
		clearInterval(two);
		charts2();
		charts1();
		setTimeout(function() {
			$(".loader").css({
				"display": "block"
			});
			$(".tips").css({
				"display": "block"
			});
		}, 650);
		$(".tips span")[0].innerText = "正在爬取中，  ";
		two = setInterval(getdata, 5000);
		one = setInterval(changeData, 250);
		$(SerButton).prop("disabled", true);
		SerButton.style.cursor = "not-allowed";
		$(StopButton).prop("disabled", false);
		StopButton.style.cursor = "pointer";
		$(Puase).prop("disabled", false);
		Puase.style.cursor = "pointer";
	}
}

function dataPage(p) {
	$.ajax({
		type: "get",
		url: "http://zrb.gotohard.cn/getdata/getdata?url_domain=" + taskName + "&page=" + p,
		async: true,
		success: function(e) {
			borad[0].innerText = "";
			if(myscroll[0].style.display = "true") { //如果麻雀在显示，那么就麻雀隐藏
				myscroll[0].style.display = "none";
			}
			for(var i = 0; i < e.data.length; i++) {
			//	console.log(11121321321);
				$(".borad").append("<li>" + e.data[i] + "</li>");
			}

		//	console.log(e.data);
		}
	});

}