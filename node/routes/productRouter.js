import express from "express";
import { ensureAuthenticated } from "../middlewares/auth.js";
const route = express.Router();

route.get("/",ensureAuthenticated,(req, res)=>{
    res.status(200).json(
        {
            name: "Krishchal",
            post: "Developer",
            desc: "Authorized Resourse..."
        }
    )
});
export default route;