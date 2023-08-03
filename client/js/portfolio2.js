var porfoioData;
await $.get('http://127.0.0.1:5000/user/2', function(data) {
    porfoioData = JSON.parse(data);
}, 'text');
console.log(porfoioData);
$('#nameText').text(porfoioData["name"] + " " + porfoioData['age']+"y.o");
$('#raiting').text(porfoioData['total_contibution']+"/5");
$('#count_feedback').text("Out of "+porfoioData['feedback_count']);

function getFeedback(name,text,stars){
    let active_star = `<span class="fa fa-star checked"></span>`
    let unactive_star = `<span class="fa fa-star"></span>`
    let res = "<div>"
    for (let i = 0; i < stars; i++) {
        res = res + active_star;
    }
    for (let i = 0; i < 5-stars; i++) {
        res = res + unactive_star;
    }
    res+="<div/>"

    return `<div class="uui-team08_item">
    <div class="uui-team08_image-wrapper">
      <img
        src="https://uploads-ssl.webflow.com/64038e074b57269e7b7c75a4/64039e30ec8bf789f5578c12_Avatar%20Image%206.png"
        loading="lazy"
        alt=""
        class="uui-team08_image"
      />
    </div>
    <div class="uui-team08_item-content">
      <div
        id="w-node-_1c956454-562c-7f9e-74ba-b32253d4cb5e-25b0b491"
        class="namereviewer"
      >
        ${name}
      </div>
      <div>${text}</div>
      <div>${res}</div>
    </div>
  </div>`
}
let fb = getFeedback("david","123",4);
$('#review_list').html(fb);