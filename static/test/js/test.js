var msz = new Object();
var targets = [];
msz.data = targets;
var type;
var dekey = 0; //key值为空时，默认key值的参数
var keys = [];
var signs = [];
var xvalue, xkey;
var values = [];
var obj1, txt, body;
var getXpath = "";
var ancXpath, focXpath;
var fileName;
var upload = document.getElementById("upload");
var Mname = document.getElementById("name");
var file = document.getElementById("file");
var begin = document.getElementById("begin");
var content = document.getElementById("content");
var loading = document.getElementById("loading");
var shade = document.getElementById("shade");
var key = document.getElementById("key");
var value = document.getElementById("value");
var xpath = document.getElementById("xpath");
var board = document.getElementById("board");
var box = document.getElementById("box");
var ensure = document.getElementById("ensure");
var final = document.getElementById("final");
var addItem = document.getElementById("addItem");
var check = document.getElementById("check");
var iframe = document.getElementById("iframe");
$("#iframe").load(function() { //iframe加载之后再加载js
	loading.style.display = "none";
	if(iframe.contentDocument.body.innerText == "网页找不到,错误代码404，2秒之后刷新页面！") {
		setTimeout(function() { //使用  setTimeout（）方法设定定时2000毫秒
			window.location.reload(); //页面刷新
		}, 2000);
	//	console.log("404");
	} else {
		var
			//		txt,
			txtClass,
			txtValue,
			getValue,
			ancSelect,
			focSelect,
			getValue;
		obj1 = window.frames["myframe"]; //获取iframe的Windows对象
		body = window.frames["myframe"].document.body;
	//	console.log(body);
		loading.style.display = "none";
		box.style.display = "block";
		Mname.style.display = "none";
		Mname.value = "";
		console.log("iframe页面加载了！！");
		//	body.onbeforeunload = "return myFunction()";
		$(obj1.document).click(function() {
			return false;
		});
		//	var a = obj1.document.getElementsByTagName("a");		//重置iframe页面的a标签的href
		//	for(var i = 0; i < a.length; i++){
		//	    a[i].href = "javascript:void(0);";
		//	    console.log(a[i].href);
		//	}
		//	obj1.onbeforeunload = function(e) { return false; };	//设置iframe页面不可跳转
		//	$(obj1).mousedown(function(e) {
		//		box.style.display = "none";
		//	});
		$(obj1).mouseup(function(e) { //获取iframe页面内Selection对象
			shade.style.display = "none";
			Mname.style.display = "none";
			//		box.style.display = "block";
			$(addItem).removeClass("shake-little");
			txt = obj1.getSelection();
			txtValue = txt.anchorNode.data; //鼠标起始位置的节点内容
			ancSelect = txt.anchorNode.parentElement;
			focSelect = txt.focusNode.parentElement;
			ancXpath = getXPath(ancSelect);
			focXpath = getXPath(focSelect);
			//		var a = obj1.document.getElementsByTagName("a");		//重置iframe页面的a标签的href
			//		for(var i = 0; i < a.length; i++){
			//		    a[i].href = "javascript:void(0);";
			//		    console.log(a[i].href);
			//		}
			var num = 0;
			if(ancXpath === focXpath) {
				getXpath = ancXpath;
				sign = 1;
			} else {
				sign = 0;
				for(var i = 0; i < ancXpath.length; i++) {
					var a = ancXpath.charAt(i);
					var b = focXpath.charAt(i)
					if(a !== b) {
						num = i;
						break;
					}
					getXpath = ancXpath.substring(0, i + 1);
				}
			}
			var sd = ancXpath.charAt(num);
			//		console.log(sd + getXpath);
			//处理字符串
			if(getXpath.search(/]/) == -1) {

			} else if(getXpath.charAt(getXpath.length - 1) == '/') {
				getXpath = getXpath.substring(0, getXpath.length - 1);
			} else if(getXpath.charAt(getXpath.length - 1) == ']') {
				getXpath = getXpath;
			} else {
				var lastNum = getXpath.lastIndexOf('/');
				getXpath = getXpath.substring(0, lastNum);
			}
			//		value.value = txtValue.replace(/\s/g, "");
			xpath.value = getXpath;
			key.focus();
			//		console.log(ancXpath);
			//		console.log(focXpath);
			//		console.log(getXpath);
			//		console.log("$x(\"" + getXpath + "\")[0].innerText");
			readXpath(getXpath);
		});
	}

	/*******************************************************************************************************
		"html/body/div[9]/div[2]/div[1]/div[2]/div[1]/div[1]/ul[2]/li[14]"
		getXpat.substring(11,getXpat.length)	"div[9]/div[2]/div[1]/div[2]/div[1]/div[1]/ul[2]/li[14]"
		getXpat.substring(11,getXpat.length-1).split(/\W+/)		["div", "9", "div", "2", "div", "1", "div", "2", "div", "1", "div", "1", "ul", "2", "li", "14"]
	*******************************************************************************************************/
	//通过Xpath获取用户选中的节点
	function readXpath(Xpath) {
		xparentNode = body.children;
		//		console.log(Xpath);
		var X = Xpath.substring(11, Xpath.length - 1).split(/\W+/);
		//		console.log(X);
		for(var i = 0; i < X.length; i++) { //遍历Xpath数组
			var nodeArray = [];
			for(var j = 0; j < xparentNode.length; j++) {
				var node = xparentNode[j].localName;
				if(node.indexOf(X[i]) == 0) {
					nodeArray.push(xparentNode[j]);
				}
			}
			var p = X[i + 1] - 1;
			Xlel = nodeArray[p];
			xparentNode = nodeArray[p].children;
			//			console.log(Xlel);
			//			for(var i = 0; i < xparentNode.length; i++){
			//				text = xparentNode[i].innerText;
			//			}
			i = i + 1;
		}
		//			$(Xlel).addClass("changeColor").not($(this)).removeClass("changeColor");
		board.innerHTML = Xlel.innerHTML;
		value.value = Xlel.innerText.replace(/\s/g, "");

	};
	//*******************************************************************************************************

	//获取选取元素的Xpath
	function getXPath(element) {
		//		if(element.id !== "") { //判断id属性，如果这个元素有id，则显 示//*[@id="xPath"]  形式内容
		//			return "//*[@id=\'" + element.id + "\']";
		//		}		//*[@id='wrap']/div[1]/div[1]/div[1]/p[1]

		if(element == obj1.document.body) { //递归到body处，结束递归
			return '/html/' + element.localName;
		}

		var ix = 0, //在nodelist中的位置，且每次点击初始化
			siblings = element.parentNode.children; //同级的子元素
		//			console.log(element.parentNode.nodeName);
		//			console.log("*************************************************************************************************");
		//			console.log("兄弟节点个数"+siblings.length);
		for(var i = 0, l = siblings.length; i < l; i++) {
			var sibling = siblings[i];
			if(sibling == element) { //如果这个元素是siblings数组中的元素，则执行递归操作
				//				console.log("节点内容" + sibling.innerText);
				//				console.log("索引下标"+ ix);
				return arguments.callee(element.parentNode) + '/' + element.localName + ((ix + 1) == 0 ? '' : '[' + (ix + 1) + ']'); //ix+1是因为xpath是从1开始计数的，element.localName+((ix+1)==1?'':'['+(ix+1)+']')三元运算符，如果是第一个则不显示，从2开始显示
			} else if(sibling.nodeType == 1 && sibling.localName == element.localName) { //如果不符合，判断是否是element元素，并且是否是相同元素，如果是相同的就开始累加
				ix++;
			}
		}
	};
});

//-----------------信息采集框 拖动js代码------------------------
var offset_x;
var offset_y;

function Milan_StartMove(oEvent) { //拖动函数
	var whichButton;
	if(document.all && oEvent.button == 1) whichButton = true;
	else {
		if(oEvent.button == 0) whichButton = true;
	}
	if(whichButton) {
		var title = document.getElementById("box");
		offset_x = parseInt(oEvent.clientX - title.offsetLeft);
		offset_y = parseInt(oEvent.clientY - title.offsetTop);
		document.documentElement.onmousemove = function(mEvent) {
			var eEvent;
			if(document.all) eEvent = event;
			else {
				eEvent = mEvent;
			}
			var oDiv = document.getElementById("box");
			var x = eEvent.clientX - offset_x;
			var y = eEvent.clientY - offset_y;
			oDiv.style.left = (x) + "px";
			oDiv.style.top = (y) + "px";
		}
	}
}

function Milan_StopMove(oEvent) { //离开函数
	document.documentElement.onmousemove = null;
}

//-----------------前端数据处理代码------------------------
$(addItem).click(function() { //添加按钮事件
	if(value.value == "") { //如果没有选中内容
		shade.style.display = "block";
		shade.getElementsByTagName("span")[0].innerText = "请重新选择内容";
		$(addItem).addClass("shake-little");
		return 0;
	} else {
		if(key.value == "") { //判断key值是否为空
			key.value = "default" + dekey;
			dekey = dekey + 1;
			var target = {};
			keys = [];
			values = [];
			signs = [];
			target.xkey = key.value.replace(/\s/g, "");
			target.xvalue = value.value.replace(/\s/g, "");
			target.signs = sign;
			targets.push(target);
			show(msz); //展示数据
			key.value = "";
			value.value = "";
			return 0;
		} else { //key值不为空
			var target = {};
			for(var i = 0; i < msz.data.length; i++) {
				keys.push(msz.data[i].xkey); //数组，存储所有的key值
				values.push(msz.data[i].xvalue);
			}
			if(keys.indexOf(key.value) == -1) { //判断key是否重复，key不重复
				shade.style.display = "none";
				keys = [];
				values = [];
				target.xkey = key.value.replace(/\s/g, "");
				target.xvalue = value.value.replace(/\s/g, "");
				target.xpath = xpath.value;
				target.signs = sign;
				targets.push(target);
				show(msz); //展示数据
				key.value = "";
				value.value = "";
				return 0;
			} else { //key值重复
				shade.style.display = "block";
				shade.getElementsByTagName("span")[0].innerText = `输入的key值  "` + key.value + `  "重复，请重新输入key值`;
				key.value = "";
				key.focus();
				return 0;
			}
		}
	}
});

function show(msz) {
	board.innerText = "";
	msz.data.forEach(function(target) {
		keys.push(target.xkey);
		values.push(target.xvalue);
	})
	for(var j = 0; j < keys.length; j++) {
		var k = String(keys[j]);
		var v = String(values[j]);
		var html = `<div class="list-data">
					<div class="key"></div>
					<div class="delete">删除</div>
					<div class="value"></div>
				</div>`;
		$("#board").append(html);
		document.getElementsByClassName("key")[j].innerText = k;
		document.getElementsByClassName("value")[j].innerText = v;
	}
	deploy();
	todelete();
}

function deploy() { //列表展开式
	$(".list-data").click(function() {
		$(this).toggleClass("height");
		$(this).children().eq(0).toggleClass("key-deploy");
		$(this).children().eq(2).toggleClass("deploy");
		$(this).siblings().removeClass("height");
		$(this).siblings().children().removeClass("key-deploy");
		$(this).siblings().children().removeClass("deploy");
	});
}

function todelete() { //删除按钮事件
	$(".delete").click(function() {
		var dnum = $(this).parent().index();
	//	console.log(dnum);
		msz.data.splice(dnum, 1);
		keys = [];
		values = [];
		board.innerText = "";
	//	console.log(msz);
		show(msz);
	});
}

$(ensure).click(function() { //提交按钮事件
	msz.inputName = Mname.value;
	msz.name = pinyin.getFullChars(Mname.value);
	if(msz.data == "") {
		shade.style.display = "block";
		shade.getElementsByTagName("span")[0].innerText = "请选择要获取的数据";
	} else {
		if(msz.name == "") {
			Mname.style.display = "block";
			Mname.focus();
		} else {
			//			ensure.disabled = 'true';
			//			ensure.style.cursor = "not-allowed";
			Mname.style.display = "none";
			$.ajax({
				url: 'http://zrb.gotohard.cn/train/totrain',
				type: 'POST',
				data: JSON.stringify(msz),
				async: true,
				cache: false,
				contentType: false,
				processData: false,
				success: function() {
					console.log("上传成功");
//					window.location.href = "http://zrb.gotohard.cn/static/struct.html";
				},
				error: function(url) {
					console.log("提交失败！");
				}
			});

		//	console.log(msz);
		}
	}

});
$(check).click(function() {
	shade.style.display = "none";
	keys = [];
	values = [];
	board.innerText = "";
	show(msz);
});
$("input[type='search']").focus(function() {
	var email_txt = $(this).val();
	if(email_txt == this.defaultValue) {
		$(this).val("");
	} else {
		$(this).select();
	}
});
$("input[type='search']").blur(function() {
	var email_txt = $(this).val();
	if(email_txt == "") {
		$(this).val(this.defaultValue);
	}
});

$("#begin div").click(function() {
	type = this.innerText;
	//console.log(type);
	if(type == "通过输入网址") {
		file.type = "search";
		file.name = "url";
	} else {
		file.type = "file";
		file.name = "htmlfile";
		document.getElementsByClassName("header")[0].style.paddingTop = "4px";
	}
	begin.style.display = "none";
	content.style.display = "block";
})

file.onchange = function() {
	if(this.value == '') {
		alert('请选择HTML文件');
	} else {
		fileName = this.value;
	}
}