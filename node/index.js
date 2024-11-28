import express from "express";
import mongoose from "mongoose";
import bodyParser from "body-parser";
import cors from "cors";
import dotenv from "dotenv";

import authRouter from "./routes/authRouter.js"
import productRouter from "./routes/productRouter.js";

const app = express();
app.use(bodyParser.json());
app.use(cors());
dotenv.config();

const PORT = process.env.PORT || 7005;
const URL = process.env.MONGOURL;

mongoose.connect(URL).then(()=>{
    console.log("DB connected Successfully:");

    app.listen(PORT,()=>{
        console.log(`Listening to Port : ${PORT}`);
    })
}).catch(error => console.log(error));


app.use("/api/auth",authRouter);
//app.use("/api/products",productRouter);