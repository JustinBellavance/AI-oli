import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../src/assets/logo2.png';
import '../src/App.css';

const Header = () => {
    return (
        <header className="bg-primary-color text-white p-1">
            <div className="flex flex-row items-center">
                <Link to="/" className="flex items-end space-x-2">
                    <img src={logo} alt="Logo" className="logo" />
                    <h1 className="text-5xl font-bold  mr-0 mb-2 ml-1">Ai</h1>
                    <h1 className="text-4xl ml-0 mb-2">oli</h1>
                </Link>
            </div>
        </header>
    );
};

export default Header;