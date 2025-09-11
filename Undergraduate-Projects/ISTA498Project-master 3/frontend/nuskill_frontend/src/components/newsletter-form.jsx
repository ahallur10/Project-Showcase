import React from 'react'
import classnames from 'clsx'
import {Navigate, useNavigate} from 'react-router-dom';

export function NewsletterForm({ className, onSubmit, submitBtn }) {
  const [id, setId] = React.useState('')
  const [password, setPassword] = React.useState('')

  const [success, setSuccess] = React.useState(false)
  const nav = useNavigate()
  function submit(event){
    event.preventDefault();
    fetch('http://localhost:8080/user/login',{method: 'POST',  headers: {'content-type': 'application/json'},
        body: JSON.stringify({"user_id":id.toString(),"password":password.toString()})
    }).then(async (res)=>
    {res = await res.json();
      window.localStorage.setItem('id',id.toString())

    res.body == 'Success'?nav('/dashboard'):alert('incorrect creds')})
    
  }
  function r_submit(e){
   
    fetch('http://localhost:8080/user/register',{method: 'POST',  headers: {'content-type': 'application/json'},
        body: JSON.stringify({"user_id":this.state.r_username.toString(),"password":this.state.r_password.toString()})
    }).then(async (res)=>
    
    {res = await res.json();res.body== 'Success'?alert('REGISTERED! YOU CAN NOW LOGIN!'):alert('ERROR OR ID ALREADY REGISTERED')})
    
  }

  function handleChange(event) {
    setId(event.target.value)
  }
  
  function handlepasswordChange(event) {
    setPassword(event.target.value)
  }

  return (

    <>
    <form
      className={classnames('newsletter-form is-revealing md:flex', className)}
    >
      <div className="mr-2 flex-shrink flex-grow">
        <label className="hidden" htmlFor="id" aria-hidden="true">
          Id
        </label>
        <input
          required
          placeholder="Your Coinbase Wallet-Id&hellip;"
          id="id"
          name="id"
          type="text"
          value={id}
          onChange={handleChange}
          autoComplete="off"
          className="w-full rounded-sm border border-gray-300 bg-white px-4 py-3 text-sm text-gray-500 shadow-none"
        />&nbsp; 
        <label className="hidden" htmlFor="id" aria-hidden="true">
          Password
        </label>
        <input
          required
          placeholder="Enter password&hellip;"
          id="password"
          name="password"
          type="password"
          value={password}
          onChange={handlepasswordChange}
          autoComplete="off"
          className="w-full rounded-sm border border-gray-300 bg-white px-4 py-3 text-sm text-gray-500 shadow-none"
        />
        {success && (
          <div className="mt-2 text-xs italic text-gray-500">
            Email submitted successfully!
          </div>
        )}
        &nbsp; 
        <div className="control">
        <button
          className="-mt-px inline-flex cursor-pointer justify-center whitespace-nowrap rounded-sm border-0 bg-gradient-to-r from-secondary-500 to-secondary-400 py-4 px-7 text-center font-medium leading-4 text-white no-underline shadow-lg"
          onClick={submit}
        >
          {submitBtn || 'Submit'}
        </button>
        &nbsp; 
        or
        &nbsp; 
        <button
          className="-mt-px inline-flex cursor-pointer justify-center whitespace-nowrap rounded-sm border-0 bg-gradient-to-r from-secondary-500 to-secondary-400 py-4 px-7 text-center font-medium leading-4 text-white no-underline shadow-lg"
          onClick={submit}>
            Login
         </button>
      </div>  
      </div>
      &nbsp; 
    </form>
    <div>&nbsp;</div>
    
  </> 
  )
}
