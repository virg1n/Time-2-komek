data = axios.get('http://127.0.0.1:5000/TTjrsK0NflCYaMKmc6yZ/get_user').then((res)=>{

    document.getElementById("nameAndSurname").innerHTML = data['name']
    document.getElementById("yearsold").innerHTML = data['age'] + " years old"
    document.getElementById("nameOfCompany").innerHTML = data['company']
    document.getElementsByClassName("hisGrade")[0].innerHTML = data['grade']
    document.getElementsByClassName("hisGrade")[1].innerHTML = data['grade']
    document.getElementsByClassName("raitingg").innerHTML = data['contribution']
})
//raitingg

// const nameAndSurname = "Torossyan David"
// const age = 18
// const grade = "GameDev Middle"
// const company = "Company: No"
// const contribution = 777
// document.getElementById("nameAndSurname").innerHTML = nameAndSurname
// document.getElementById("yearsold").innerHTML = age + " years old"
// document.getElementById("nameOfCompany").innerHTML = company 
// document.getElementsByClassName("hisGrade")[0].innerHTML = grade
// document.getElementsByClassName("hisGrade")[1].innerHTML = grade



function setcourses(){
      try {
        axios.get('http://localhost:3001/getcourses').then((res)=>{
            var data = res['data']['courses']
            console.log(data);
            for (let i = 0; i < data.length / 3; i += 1){
                for(let j = 0; j < 3; j += 1){
                    if (data[i*3+j]){
                    $(`.golka${i}`).append(
                    `<div class="div-block-5100-copy" style="max-width: 300px;">
                        <div class="div-block-45-copy"></div>
                        <div class="text-block-24">You have successfully registered for the course| ${data[i*3+j]}</div>
                    </div>`)
                    
                }}
            }
            for (let i = 0; i < data.length; i += 1){
                $(`.div-block-11`).append(`
                <div class="div-block-49">
                    <div class="div-block-47"><h4 style="color:#52B788; margin-right: 5px;">0%</h4>
                        <div class="text-block-21"><a href="/client/course.html" style="color:white;">${data[i]}</a></div>
                    </div>
                    <div class="div-block-48">
                        <div class="text-block-23">Goals Remaining: 24/24</div>
                    </div>
                    <div>
                        <div class="text-block-23">Deadlines: not delivered</div>
                    </div>
                </div>
                `)

                $(`.jokin`).append(`
                <div class="columns-2 w-row">
                    <div class="">
                        <div class="div-block-13" style="margin: 15px;">
                            <div class="text-block-8" style="color:black">${data[i]}</div>
                            <div class="text-block-8-copy" style="color:black">0% done</div>
                        </div>
                    </div>
                </div>
                `)
            }
            //jokin

        })
  
      } catch (error) {
        console.log(error);
      }
    }



setcourses()