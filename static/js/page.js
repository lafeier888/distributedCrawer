var totalPage = 20; //总页数
var pageSize = 5; //分页尺寸
crPage = -1;

function getData(page) {
	crPage = page;
	$(".contentArea").text("我是第：" + page + "页的内容哦！")
	return page;
}
//首页
$("#indexPage").click(function() {
	getData(1);
})
//末页
$("#endPage").click(function() {
	getData(-999);
})
//上一页
$("#prePage").click(function() {

	getData(crPage - 1);
})
//下一页
$("#nextPage").click(function() {
	getData(crPage + 1);
})

if(totalPage <= 7) {
	for(var i = 1; i < totalPage; i++) {
		$("#nextPage").last().before("<li><a onclick='getData(" + i + ")' >" + i + "</a></li>")
	}
} else {
	for(var i = 1; i < 5; i++) {
		$("#nextPage").last().before("<li><a onclick='getData(" + i + ")' >" + i + "</a></li>")
	}
	$("#nextPage").last().before("...")
	for(var i = totalPage - 3; i < totalPage; i++) {
		$("#nextPage").last().before("<li><a onclick='getData(" + i + ")' >" + i + "</a></li>")
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
				$($(".pageList li").get(i)).html("<a onclick='getData(" + currPage + ")' >" + currPage + "</a>")
				currPage = currPage - 1;
			}
		}
	}
})