import React, {useState} from 'react';
import "../styles/LoginSignup.css"
import email_icon from "./Assets/email.png"
import password_icon from "./Assets/password.png"
import { Link } from "react-router-dom";
import person_icon from "./Assets/person.png"

const Signup = ({signin}) => {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [signup, setSignup] = useState(false);

    const createUser = async () => {
        try {
            const response = await fetch(`http://localhost:8000/users/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                }),
            });
            const user = await response.json();
            if(user.msg === "successfully add new user"){
                setSignup(true)
            }else {
                setSignup(false)
            }
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    const canSignup = signup === true ? '/userpage' : '/SignupPage';

    return(
        <form method='POST'>
            <div className='container'>
                <div className='header'>
                    <div className='text'>Sign up</div>
                </div>
                <div className='inputs'>
                    <div className='input'>
                        <img src = {person_icon} alt=''/>
                        <input type='text' placeholder='Name' 
                            value={name}
                            onChange={(event) => setName(event.target.value)}
                        />
                    </div>
                    <div className='input'>
                        <img src={email_icon} alt=''/>
                        <input type='email'  placeholder='Email Id' 
                            value={email}
                            onChange={(event) => setEmail(event.target.value)}
                        />
                    </div>
                    <div className='input'>
                        <img src={password_icon} alt=''/>
                        <input type='password' 
                            placeholder='Password' 
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                        />
                    </div>
                </div>
                <div className='submit-container'>
                    <Link className="submit" to={canSignup} 
                    onClick={() => {
                        createUser();
                        signin();
                    }}>
                        Sign up
                    </Link>
                </div>
            </div>
        </form>
    );
}

export default Signup;