window.onload = function(){
	$(document).click(function(){return false;});
}
var msz = new Object();
var targets = [];
msz.data = targets;
var obj1, body;
var ancXpath, focXpath;
var shade = document.getElementById("shade");
var key = document.getElementById("key");
var value = document.getElementById("value");
var xpath = document.getElementById("xpath");
var board = document.getElementById("board");
var ensure = document.getElementById("ensure");
var addItem = document.getElementById("addItem");
$("#iframe").load(function() { //iframe加载之后再加载js
	var
		txt,
		txtClass,
		txtValue,
		getValue,
		ancSelect,
		focSelect,
		getValue;
	obj1 = window.frames["myframe"]; //获取iframe的Windows对象
	body = window.frames["myframe"].document.body;
	$(obj1.document).click(function(){
	//	console.log(this.innerText);
		return false;
	});
	$(obj1).mouseup(function(e) { //获取iframe页面内Selection对象
		var getXpath = "";
		shade.style.display = "none";
		board.style.backgroundColor = "white";
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
		} else {
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

	/*******************************************************************************************************
		"html/body/div[9]/div[2]/div[1]/div[2]/div[1]/div[1]/ul[2]/li[14]"
		getXpat.substring(11,getXpat.length)	"div[9]/div[2]/div[1]/div[2]/div[1]/div[1]/ul[2]/li[14]"
		getXpat.substring(11,getXpat.length-1).split(/\W+/)		["div", "9", "div", "2", "div", "1", "div", "2", "div", "1", "div", "1", "ul", "2", "li", "14"]
	*******************************************************************************************************/
	//通过Xpath获取用户选中的节点
	function readXpath(Xpath){
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

	var target = {};

	target.key = key.value;
	target.value = value.value.replace(/\s/g, "");
	target.xpath = xpath.value;
	//判断是否输入key值
	if(target.key !== "" && target.value !== "" && target.xpath !== "") {
		shade.style.display = "none";
		key.style.borderColor = "";
		board.style.backgroundColor = "#f5f5f5";
		$(addItem).removeClass("shake-little");
		targets.push(target);
		board.innerText = JSON.stringify(msz);
		key.value = "";
		value.value = "";
		xpath.value = "";
	} else {
		key.focus();
		shade.style.display = "block";
		key.style.borderColor = "#dc7777";
		$(addItem).addClass("shake-little");
	}
});

$(ensure).click(function() { //提交按钮事件
	board.innerText = JSON.stringify(msz);
	alert(JSON.stringify(msz));
});
