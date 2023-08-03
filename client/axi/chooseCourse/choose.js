// import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from '../../utils/axios.js'

export const loginUser = async ({email, password})=>{
    try {
        const {data} = await axios.post('/choosecourse', {
            email,
            password
        })
        if(data.token){
            window.localStorage.setItem('token', data.token)
        }
        return data
    } catch (error) {
        console.log(error);
    }
}