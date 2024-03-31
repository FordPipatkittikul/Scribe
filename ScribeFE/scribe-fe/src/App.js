import React, {Component} from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from "react";

import './styles/App.css';

import UserPage from "./components/pages/UserPage"
import Layout from './Layout';
import About from './components/pages/AboutUs';
import SignupPage from './components/pages/SignupPage';
import LoginSignupPage from './components/pages/LoginSignupPage';
import FormSubmissionPage from "./components/pages/FormsubmissionPage";
import Welcomepage from "./components/pages/WelcomePage";

const App = () => {
    const [isSignin,setIsSignin] = useState(false);

    const signin = () => {
        setIsSignin(true)
    }

    const signout = () => {
        setIsSignin(false)
    }

    return (
        <div>
        {/* <ParticlesBg type="square" bg={true} /> */}
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Layout isSignin={isSignin} signout={signout}/>}>
                    <Route index element={<Welcomepage />} />
                    <Route path="userpage" element={<UserPage />} />
                    <Route path='aboutus' element={<About />} />
                    <Route path="loginSignupPage" 
                        element={<LoginSignupPage 
                        signin={signin}/>} 
                    />
                    <Route path="SignupPage" 
                        element={<SignupPage
                            signin={signin}/>} 
                    />
                    <Route path="formsubmission" element={<FormSubmissionPage/>}/>
                </Route>
            </Routes>
        </BrowserRouter>
        </div>
    );

}

export default App;
