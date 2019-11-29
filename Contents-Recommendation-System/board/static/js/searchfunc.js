$("#f_submit").click(function(){
         if($("#f_keyword").val()==''){
            alert("키워드를 입력해주세요");
            return false
         }
         mySubmit(1);
    }
)

$("#s_submit").click(function(){
        if($("#f_keyword").val()==''){
            alert("첫번째 키워드를 입력해주세요");
            return false
        }
        if($("#s_keyword").val()==''){
            alert("키워드를 입력해주세요");
            return false
        }
        mySubmit(2);
    }
)
$("#csvInput").click(function(){
        if($("#f_keyword").val()==''){
            alert("첫번째 키워드를 입력해주세요");
            return false
        }
        mySubmit(3);
    }
)

function mySubmit(index){
    if(index==1){
        var furl = $("#fUrl").attr("data-url");
        document.f_searchform.action = furl;
    }
    if(index==2){
        var surl = $("#sUrl").attr("data-url");
        //alert("test");
        document.f_searchform.action = surl;
    }
    if(index==3){
        var durl = $("#dCSV").attr("data-url");
        document.f_searchform.action = durl;
    }
    document.f_searchform.submit();
}

function click_tag(temp)
{
    var select = $("input[type=hidden][name=select_tag]").val();
    if(!select)
    {
        $("input[type=hidden][name=select_tag]").val(temp);
    }
    else
    {
        $("input[type=hidden][name=select_tag]").val(select + "," + temp);
    }
    $('#searchform').submit();
}