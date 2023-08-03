var datetos; 
await $.get('http://127.0.0.1:5000/gettopcontribution', function(data) {
  datetos = JSON.parse(data);
}, 'text');

function addTableRow(nm,name, email, about, skill, contibution){
    return `<div class="table-row">
    <div class="div-block-406 _2">
      <div class="table-row-nr">${nm}</div>
    </div>
    <div class="table-box _2">
      <img
        src="https://uploads-ssl.webflow.com/64038e074b57269e7b7c75a4/64041ee8aecfdb97ab532fee_5dd1ca04edfe6a591970a2cd_face-chad.jpg"
        width="32"
        alt=""
        class="image-7"
      />
      <div class="table-data name">${name}</div>
    </div>
    <div class="table-box _2">
      <a href="#" class="table-data link">${email}m</a>
    </div>
    <div class="table-box _2">
      <div class="table-data">${about}</div>
    </div>
    <div class="table-box _2">
      <div class="table-data">${skill}</div>
    </div>
    <div class="table-box _2 small">
      <div class="table-data">${contibution}</div>
    </div>
  </div>
  `
}
 let i =1;
Object.keys(datetos).forEach(key => {
  $("#scroll-table-content").append(addTableRow(i, datetos[key]["name"], datetos[key]["email"], datetos[key]["about"], datetos[key]["skills"], datetos[key]["total_contribution"]));
  i+=1;
});