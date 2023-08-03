roadmap = ["UnrealEngine", "PyGame", "GODOT", "Unity", "Flutter", "C#", "libGDX", "Pyglet", "Android Studio", "Kivy", "PANDA3D", "Cocos2d", "OOP", "Unity", "C++", "C"]
learned = {1:true, 2:false, 3:false, 4:true, 5:true, 6:false, 7:true, 8:false, 9:false, 10:false, 11:false, 12:false, 13:false, 14:false, 15:false, 16:false}
grade = "Game Dev Junior"

document.getElementById("ForWhom").innerHTML = "For " + grade

//div-block-3

function putRoadMap(len){
    for (let i = 0; i < len; i+= 1){
        const box = document.createElement("div");
        box.className = "div-block-2";
        box.id = `box${i}`
        document.getElementById("maindiv").appendChild(box);
        for (let j = 0; j < 4; j+= 1){
            const butt = document.createElement("a");
            butt.href = "#"
            if (learned[`${i*4 + j + 1}`] == false){
                butt.className = "button-2 w-button"
            }
            else{
                butt.className = "button-3 w-button"
            }
            butt.id = `butt${i*4 + j}`
             
            butt.textContent = roadmap[i*4 + j]
            document.getElementById(`box${i}`).appendChild(butt);
            document.getElementById(`butt${i*4 + j}`).onclick = function() {  
                document.getElementById(`butt${i*4 + j}`).className = "button-3 w-button"
            }; 
        }
    }
}

function torecomnded(){
    window.location.href = "http://127.0.0.1:5500/client/recomended.html#";
}
putRoadMap(roadmap.length / 4)