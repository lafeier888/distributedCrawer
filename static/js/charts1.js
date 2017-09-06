var pChart1; //获取数据总条数计时器
function charts1() {
	var myChart = echarts.init(document.getElementById('charts1'));
	var base = +new Date(2014, 9, 3);
	var oneDay = 24 * 3600 * 1000;
	var date = [];
	var data = [];
	var now = new Date();
	var value;
	var start = (new Date()).valueOf();

	function formatDuring(mss) {
		var days = parseInt(mss / (1000 * 60 * 60 * 24));
		var hours = parseInt((mss % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		var minutes = parseInt((mss % (1000 * 60 * 60)) / (1000 * 60));
		var seconds = parseInt((mss % (1000 * 60)) / 1000);
		var ms = (mss % (1000 * 60)) / 1000;
		var ms2 = ms.toString();
		var ms3 = ms2.split('.');
		//	return days + " 天 " + hours + " 小时 " + minutes + " 分钟 " + seconds + " 秒 "+ms3[1]+'毫秒';
		if(typeof(ms3[1])=="undefined")
			ms3[1] =0;
		var times = [hours, minutes, seconds, ms3[1]];
		return times;
	}

	function addData(shift) {
	//	console.log("chart-1 running" + new Date());
//		return

		var xianzai = (new Date()).valueOf();
		var chazhi = parseInt(xianzai) - parseInt(start);
		var cc = formatDuring(chazhi);
		//	    console.log(start,'---',xianzai,'---',chazhi,'---',cc);

		now = [cc[0] + '小时', cc[1] + '分钟', cc[2] + '秒', cc[3] + '毫秒'].join('-');
		date.push(now);

		$.ajax({
			type: "GET",
			url: "http://zrb.gotohard.cn/getdata/items?url_domain=" + taskName,
			async: false,
			success: function(msg) {
				value = msg;
				$("#p1").html(msg);
			}
		});

		data.push(value);
		

		now = new Date();
	}
	for(var i = 1; i < 5; i++) {
			addData();
		}
	// 指定图表的配置项和数据
	var option = {
		title: {
			left: 'left',
			text: '数据总条数',
		},
		grid: {
			left: 75
		},
		tooltip: {
			trigger: 'axis',
			position: function(pt) {
				return [pt[0], '10%'];
			}
		},
		xAxis: {
			type: 'category',
			boundaryGap: false,
			data: date
		},
		yAxis: {
			boundaryGap: [0, '50%'],
			type: 'value'
		},
		series: [{
			name: '数据总条数',
			type: 'line',
			smooth: true,
			symbol: 'none',
			stack: 'a',
			areaStyle: {
				normal: {}
			},
			data: data
		}]
	};

	// 使用刚指定的配置项和数据显示图表。
	myChart.setOption(option);

		pChart1 =  setInterval(function() {
		//	console.log("charts1数据总条数表插入新数据" + new Date());
			addData(true);
			myChart.setOption({
				xAxis: {
					data: date
				},
				series: [{
					name: '数据总条数',
					data: data
				}]
			});
		}, 2000);
}