import express from "express";
import cors from 'cors'
import mongoose from "mongoose";

const app = express();
const PORT = 3001

// mongoose.connect('mongodb+srv://qwaradie:**********@cluster0.0q079aj.mongodb.net/?retryWrites=true&w=majority').then(()=>{
//     console.log("DB Okey")
// })

var courses = []

app.use(cors())
app.use(express.json())

app.post('/choosecourse', async (req, res)=>{
    try{
        const course = req.body.course
        // const name = req.body.name
        courses.push(course)

        res.json({message:courses})

    }catch(err){
        res.json({message:"error on login"})
    }
})

app.get('/getcourses', async (req, res)=>{
    try{
        res.json({courses})

    }catch(err){
        res.json({message:"error on getcourses"})
    }
})

app.get('/getinfo', async (req, res)=>{
    try{
        res.json({sname, grade, age, company, contribution})

    }catch(err){
        res.json({message:"error on getcourses"})
    }
})


app.listen(PORT,(err)=>{
    if(err){
        return console.log(err);
    }
    console.log("ok")
});