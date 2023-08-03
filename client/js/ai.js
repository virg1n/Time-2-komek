$("#generate_btn").click(async function(){
    let req = $("#Name").val()
    req.replace(' ',"-");
    let res;
    await $.get('http://127.0.0.1:5000/ai?req='+req, function(data) {
        res = JSON.parse(data);
        console.log(res);
    }, 'text');
    $("#answer").text(`with a percentage of ${res['procent']}% you are - ${res['prof']}`);
    await $.get('http://127.0.0.1:5000/get-tests?skill='+res['prof'], function(data) {
        res = JSON.parse(data);
    }, 'text');
    var id, sk;
    $.each(res, function( key, value ) {
        id = key;
        sk = value["name"];
    })
    $("#answer").append(`.You can take the test - <a href="http://127.0.0.1:5500/client/test.html?id=${id}">${sk}</a> to get a checklist`);
});