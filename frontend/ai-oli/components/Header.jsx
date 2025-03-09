import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../src/assets/logo2.png';
import '../src/App.css';

const Header = () => {
    return (
        <header className="bg-primary-color text-white p-1">
            <div className="flex flex-row items-center">
                <Link to="/" className="flex items-center space-x-2">
                    <img src={logo} alt="Logo" className="logo" />
                    <h1 className="text-4xl font-bold">Aioli</h1>
                </Link>
            </div>
        </header>
    );
};

export default Header;