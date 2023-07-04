import React from 'react';
import "./Institution.css";

function Institution() {
  return (
    <section className='institutionbody'>
        <div className = "register">
            <div className='col-1'>
            <h2>Registration</h2>
            <spam>register and join our large community of prestigious institutions</spam>

            <form id='signin' className='flex flex-col'>
                <input type="text" placeholder='Institution Name' />
                <input type="text" placeholder='Registration ID' />
                <input type="text" placeholder='email' />
                <input type="text" placeholder='phone number' />
                <input type="text" placeholder='Pin Code' />
                <input type="text" placeholder='Licence Number' />
                <input type="text" placeholder='State' />
                <input type="text" placeholder='Country' />


                <button className='btn'>Register Now</button>
            </form>
            </div>
            <div className='col-2'>
                <img src="https://images.unsplash.com/photo-1543505298-b8be9b52a21a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aW5zdGl0dXRpb258ZW58MHx8MHx8fDA%3D&w=1000&q=80"
                alt=" " />
            </div>
        </div>
    </section>
  )
}

export default Institution