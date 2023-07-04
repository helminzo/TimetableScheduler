import React from 'react'
import "./Signin.css";

function Signin() {
  return (
    <section className='signinbody'>
        <div className = "register">
            <div className='col-1'>
            <h2>Sign In</h2>
            <spam>register and join our community</spam>

            <form id='signin' className='flex flex-col'>
                <input type="text" placeholder='username' />
                <input type="text" placeholder='password' />
                <input type="text" placeholder='email' />
                <input type="text" placeholder='phone number' />

                <button className='btn'>Sign</button>
            </form>
            </div>
            <div className='col-2'>
                <img src="https://t4.ftcdn.net/jpg/02/00/90/53/360_F_200905394_2u1hKNTSawkcR6N1X0aX0PiSBR1tvUMn.jpg"
                alt=" " />
            </div>
        </div>
    </section>
  )
}

export default Signin