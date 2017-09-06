window.onload=function(){ 
//	var el = obj1.document.body; //声明一个变量，默认值为body
	obj1.document.body.onmouseover = function(event) {
		el = event.target; //鼠标每经过一个元素，就把该元素赋值给变量el
		console.log(el.innerText);
		$(el).css("background-color","yellow");
		
	}
	obj1.document.body.onmouseout = function(event) {
		el = event.target; //鼠标每经过一个元素，就把该元素赋值给变量el
		$(el).css("background-color","white");
	}
}