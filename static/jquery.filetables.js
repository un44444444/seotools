/*!
 * jQuery File Tables Plugin
 *
 * Date: 2012-09-08
 */
(function( $ ){
	$.fn.filetables = function( options ) {
		var settings = $.extend( {
			'functionurl'   : '/queryexlink',
			'debug'         : 0
		}, options);
		
		return this.each(function() {
			var $this = $(this);
			if (settings.debug != 0) {
				var filelist = ['xxxxxxx.txt','yyyyyyyy.txt'];
				$this.append(to_ul(filelist));
				return;
			}
			ONERING.getJSON(settings.functionurl+'/files', function(json) {
				//alert(allPrpos(json));
				var filelist = json.files;
				//alert(filelist);
				$this.append(to_ul(filelist));
			});
function notify(msg)
{
	props = {};
	ONERING.createWindow('/warning/'+msg, 400, 300, props)
}
function allPrpos(obj)
{
	var props = "";
	for(var p in obj)
	{ 
		if(typeof(obj[p])=="function"){
			props+= p + "=function(..)\r\n";
		}else{
			props+= p + "=" + obj[p]+"\r\n";
		}
	}
	return props;
}
function do_query(seqnum, filename){
	//email=$('#email_'+seqnum).val();
	//passwd=$('#pass_'+seqnum).val();
	post_data = {email:'',passwd:''};
	ONERING.post(settings.functionurl+'/handle/'+filename, post_data, function(json) {
		$('#li_'+seqnum).text('开始处理文件：'+allPrpos(json));
	}, 'json');
	//
	var timerid;
	function query_status(){
		ONERING.getJSON(settings.functionurl+'/query/'+filename, function(json) {
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
	var ul = $('<ul></ul>');
	// --v loop through its children
	for (var f = 0; f < filelist.length; f++) {
		li = $('<li></li>').appendTo(ul);
		table = $('<table></table>').appendTo(li);
		//
		tr1 = $('<tr></tr>').appendTo(table);
		td1 = $('<td></td>').appendTo(tr1);
		td1.append('<a>'+filelist[f]+'</a> | ');
		(function(idx){
		a_send = $('<a href="#">批量查询..<a>').appendTo(td1).click(function(event){
			do_query(idx, filelist[idx]);
			event.preventDefault();
		});
		})(f);
		td1.append(a_send);
		//
/*		tr2 = document.createElement ('tr');
		td2 = document.createElement ('td');
		input_email = document.createElement ('input');
		input_email.setAttribute('id', 'email_'+f);
		input_email.setAttribute('type', 'text');
		td2.appendChild (input_email);
		input_pass = document.createElement ('input');
		input_pass.setAttribute('id', 'pass_'+f);
		input_pass.setAttribute('type', 'text');
		td2.appendChild (input_pass);
		tr2.appendChild (td2)
		table.appendChild (tr2)
*/		//
		tr3 = $('<tr></tr>').appendTo(table);
		td3 = $('<td id="li_'+f+'">等待处理...</td>').appendTo(tr3);
	}
	return ul;
}
		});
	};
})( jQuery );
