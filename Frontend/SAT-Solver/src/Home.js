import React from "react";
import "./Home.css";
import Product from "./Product";

function Home() {
  return (
    <div className="home">
      <div className="home_container">
        
        <img 
         className="home_image"
         src = "https://www.thoughtco.com/thmb/PjzmasuExRyhMheaefmKz4q94Fo=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/capitol-and-blue-sky-147722633-59fb84290d327a00363f8324.jpg" 
         alt="" />

         <div className="home_row">
            <Product id="1" info="Click here to add your institution" name="Select Institution" image={"https://s3-us-west-2.amazonaws.com/courses-images/wp-content/uploads/sites/1988/2017/05/31175400/4704325570-a6e07e260f-b.jpeg"} button="Add Subscription"/>
            <Product id="2" info="Click here to create a schedule or timetable" name="Create Timetable" image={"https://media.sproutsocial.com/uploads/2022/06/How-to-schedule-TikTok-posts_Artboard-1-copy.svg"} button="Create Now"/>
             
         </div>
         <div className="home_row">
         <Product id="3" info="Click here to view my schedules" name="View my Schedules" image={"https://png.pngtree.com/background/20220729/original/pngtree-work-schedule-organization-banner-kanban-picture-image_1860588.jpg"} button="View Now"/>
        
         </div>
      </div>
    </div>
  );
}

export default Home;
