/*!
 * jQuery File Tables Plugin
 *
 * Date: 2012-09-08
 */
(function( $ ){
	$.fn.filetables = function( options ) {
		var settings = $.extend( {
			'location'         : 'top',
			'background-color' : 'blue'
		}, options);
		
		return this.each(function() {
			var $this = $(this);
			ONERING.getJSON('/queryexlink/files', function(json) {
				//alert(allPrpos(json));
				var filelist = json.files;
				//alert(filelist);
				$this.append(to_ul(filelist));
			});
			//var filelist = ['xxxxxxx.txt','yyyyyyyy.txt'];
			//this.appendChild(to_ul(filelist));
function query_weight(seqnum, filename){
	//email=$('#email_'+seqnum).val();
	//passwd=$('#pass_'+seqnum).val();
	post_data = {email:'',passwd:''};
	ONERING.post('/queryexlink/handle/'+filename, post_data, function(json) {
		$('#li_'+seqnum).text('开始处理文件：'+allPrpos(json));
	}, "json");
	//
	var timerid;
	function query_status(){
		ONERING.getJSON('/queryexlink/query/'+filename, function(json) {
			status=json.status;
			if (status<=0)
			{
				clearInterval(timerid);
				total_count=json.count1;
				dealed_count=json.count2;
				lasterror=json.lasterror;
				$('#li_'+seqnum).text('处理完毕：'+lasterror+'当前已完成'+dealed_count+'/'+total_count+'。');
				notify(lasterror);
			}
			else
			{
				current_dealed_count=json.count1;
				$('#li_'+seqnum).text('处理中：本次已处理'+current_dealed_count+'条。');
			}
		});
	}
	timerid = window.setInterval(query_status, 1000);
}
function to_ul (filelist) {
	// --------v create an <ul> element
	var f, li, ul = document.createElement ("ul");
	// --v loop through its children
	for (f = 0; f < filelist.length; f++) {
		li = document.createElement ("li");
		table = document.createElement ("table");
		//
		tr1 = document.createElement ("tr");
		td1 = document.createElement ("td");
		link = document.createElement("a");
		link.appendChild (document.createTextNode (filelist[f]));
		td1.appendChild (link)
		td1.appendChild (document.createTextNode(" | "));
		a_send = document.createElement("a");
		a_send.setAttribute("href", "#");
		a_send.setAttribute("onclick", "javascript:query_weight('"+f+"', '"+filelist[f]+"');");
		a_send.appendChild (document.createTextNode("批量查询.."));
		td1.appendChild (a_send)
		tr1.appendChild (td1)
		table.appendChild (tr1)
		//
/*		tr2 = document.createElement ("tr");
		td2 = document.createElement ("td");
		input_email = document.createElement ("input");
		input_email.setAttribute("id", "email_"+f);
		input_email.setAttribute("type", "text");
		td2.appendChild (input_email);
		input_pass = document.createElement ("input");
		input_pass.setAttribute("id", "pass_"+f);
		input_pass.setAttribute("type", "text");
		td2.appendChild (input_pass);
		tr2.appendChild (td2)
		table.appendChild (tr2)
*/		//
		tr3 = document.createElement ("tr");
		td3 = document.createElement ("td");
		td3.setAttribute("id", "li_"+f);
		td3.appendChild (document.createTextNode("等待处理..."));
		tr3.appendChild (td3)
		table.appendChild (tr3)
		//
		li.appendChild (table);
		ul.appendChild (li);
	}
	return ul;
}
		});
	};
})( jQuery );
