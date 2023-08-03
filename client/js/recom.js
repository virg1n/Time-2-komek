// import { loginUser } from '../axi/chooseCourse/choose.js'
// const loginUser = require('../axi/chooseCourse/choose.js');
// import axios from '../utils/axios.js'
// import axios from 'axios'

// const { default:axios } = require("axios");



function handleSubmit(course){
  console.log(12);
    try {
      axios.post('http://localhost:3001/choosecourse', {
        "course":course
      }).then(alert("added"))

    } catch (error) {
      console.log(error);
    }
  }

  document.getElementById("Android Studio: Kotlin For Android Studio For Beginners").onclick = ()=>{handleSubmit('Android Studio: Kotlin For Android Studio For Beginners')}
  document.getElementById("Android Studio: Creating Android Apps with Java").onclick = ()=>{handleSubmit('Android Studio: Creating Android Apps with Java')}
  document.getElementById("Python: PyGame Advanced Level").onclick = ()=>{handleSubmit('Python: PyGame Advanced Level')}
  document.getElementById("UnrealEngine: The Complete UnrealEngine Course").onclick = ()=>{handleSubmit('UnrealEngine: The Complete UnrealEngine Course')}
  document.getElementById("UnrealEngine: Unreal Engine For Beginners").onclick = ()=>{handleSubmit('UnrealEngine: Unreal Engine For Beginners')}
  document.getElementById("PyGame: Creating Web Games").onclick = ()=>{handleSubmit('PyGame: Creating Web Games')}
  document.getElementById("Unity: Unity For Beginners With C#").onclick = ()=>{handleSubmit('Unity: Unity For Beginners With C#')}
  document.getElementById("Unity: Advanced Unity with C#").onclick = ()=>{handleSubmit('Unity: Advanced Unity with C#')}
  document.getElementById("Flutter: Creating Mobile Apps with Dart").onclick = ()=>{handleSubmit('Flutter: Creating Mobile Apps with Dart')}
  document.getElementById("Flutter: Advanced Flutter Course For Junior").onclick = ()=>{handleSubmit('Flutter: Advanced Flutter Course For Junior')}
  document.getElementById("libGDX: The Complete libGDX Course").onclick = ()=>{handleSubmit('libGDX: The Complete libGDX Course')}
  document.getElementById("Android Studio: Learn Java For Beginners").onclick = ()=>{handleSubmit('Android Studio: Learn Java For Beginners')}