import { useState } from 'react';
import TopBar from './TopBar';
import Sidebar from './Sidebar';
import './MainLayout.css';

function MainLayout({ children, currentPage, onPageChange }) {
  return (
    <div className="main-layout">
      {/* TopBar en haut */}
      <TopBar />
      
      {/* Container pour sidebar + contenu */}
      <div className="layout-body">
        {/* Sidebar à gauche */}
        <Sidebar 
          currentPage={currentPage} 
          onPageChange={onPageChange} 
        />
        
        {/* Zone de contenu principale */}
        <div className="layout-content">
          {children}
        </div>
      </div>
    </div>
  );
}

export default MainLayout;