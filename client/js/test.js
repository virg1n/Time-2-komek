test = {
    1:{"question":"Which Unity method allows you to create objects during the game?",
    "ansA":"function - Instantiate();",
    "ansB":"function - Coroutine();",
    "ansC":"function - Update();",
    "ansD":"function - Create();", 
    "answer":"1"}, 
    2:{"question":"In which line is the component of the variable correctly assigned in Unity?",
    "ansA":"rb = GetComponent <Rigidbody> ();",
    "ansB":"rb = GetComponent (Rigidbody);",
    "ansC":"rb = GetComponent (Rigidbody) <>;",
    "ansD":"rb = GetComponent <Rigidbody>;", 
    "answer":"1"},
    3:{"question":"What are the differences between Update and Fixedupdate in Unity?",
    "ansA":"FixedUpdate has a fixed call time, the Update function is called without a fixed time",
    "ansB":"There are no differences",
    "ansC":"Fixedupdate is called only a few times during the entire game, Update is constantly",
    "ansD":"FixedUpdate works only with physical objects, Update with all", 
    "answer":"1"},
    4:{"question":"Mark the truthful information about libgdx?",
    "ansA":"developers are forced to create their own development tools on LibGDX, a map editor.",
    "ansB":"you can make games without programming.",
    "ansC":"suitable only for 2D game development",
    "ansD":"there are no difficulties with publishing the game on iOS, since this platform supports Java.", 
    "answer":"1"},
    5:{"question":"Which word is responsible for creating a constant in the Dart language?",
    "ansA":"const",
    "ansB":"constant",
    "ansC":"ver",
    "ansD":"dynamic", 
    "answer":"1"},
    6:{"question":"Which class is responsible for tooltips in Android?",
    "ansA":"Toast",
    "ansB":"Message",
    "ansC":"Alert",
    "ansD":"Hint", 
    "answer":"1"},
    7:{"question":"What property stretches an element to the full width of the screen in XML?",
    "ansA":"match_parent",
    "ansB":"parent_wrap",
    "ansC":"fill_parent",
    "ansD":"size_parent", 
    "answer":"1"}
}
answers = {
    1:"uncorrect",
    2:"uncorrect",
    3:"uncorrect",
    4:"uncorrect",
    5:"uncorrect",
    6:"uncorrect",
    7:"uncorrect",
    8:"uncorrect"
}


lenOfTest = 7
let questionNow = 1
let nowAnswer = 0

function putCircles(len){
    for (let i = 1; i <= len; i+= 1){
        const box = document.createElement("a");
        box.href='#'
        box.className = "button-7 w-button";
        box.id = `box${i}`
        document.getElementById("smt").appendChild(box);
    }
}

putCircles(lenOfTest)
document.getElementById("box1").className = "button-5 w-button"


function putQuestion(question, ans1, ans2, ans3, asn4, answer){
    document.getElementById("question").innerHTML = question;


    document.getElementById("answer1").innerHTML = ans1;
    document.getElementById("answer2").innerHTML = ans2;
    document.getElementById("answer3").innerHTML = ans3;
    document.getElementById("answer4").innerHTML = asn4;
}

function nextQuestion(){
    try {
        document.getElementById(`box${questionNow}`).className = "button-4 w-button"
        document.getElementById(`box${questionNow+1}`).className = "button-5 w-button"
        if (nowAnswer == test[`${questionNow}`]["answer"]){
            answers[`${questionNow}`] = "correct"
        }
        else{
            answers[`${questionNow}`] = "uncorrect"
        }
        if (questionNow != lenOfTest){
            questionNow += 1
            putQuestion(test[`${questionNow}`]["question"], test[`${questionNow}`]["ansA"], test[`${questionNow}`]["ansB"], test[`${questionNow}`]["ansC"], test[`${questionNow}`]["ansD"], test[`${questionNow}`]["answer"]);
            
        }
        else{
            console.log(answers);
            axios.post('http://localhost:3001/testanswers', {
                "answers":answers
            })
            window.location.href = "http://127.0.0.1:5500/client/RoadMap.html#";
        }
    } catch (error) {
        window.location.href = "http://127.0.0.1:5500/client/RoadMap.html#";
    }
    
    

}

function chooseAnswer1(){
    nowAnswer = 1
}

function chooseAnswer2(){
    nowAnswer = 2
}

function chooseAnswer3(){
    nowAnswer = 3
}

function chooseAnswer4(){
    nowAnswer = 4
}

