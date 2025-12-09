import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from './AuthContext';

function UserProfile() {
  const { currentUser, logout } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  if (!currentUser) return null;

  const handleLogout = async () => {
    try {
      await logout();
      setIsDropdownOpen(false);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <div className="user-profile" ref={dropdownRef}>
      <div 
        className="user-avatar-container"
        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
      >
        <img 
          src={currentUser.photoURL || '/default-avatar.png'} 
          alt={currentUser.displayName || 'User'} 
          className="user-avatar"
        />
        <span className="user-name">{currentUser.displayName}</span>
        <span className={`dropdown-arrow ${isDropdownOpen ? 'open' : ''}`}>▼</span>
      </div>
      
      {isDropdownOpen && (
        <div className="user-dropdown">
          <div className="user-info">
            <img 
              src={currentUser.photoURL || '/default-avatar.png'} 
              alt={currentUser.displayName || 'User'} 
              className="dropdown-avatar"
            />
            <div className="user-details">
              <div className="user-name-large">{currentUser.displayName}</div>
              <div className="user-email">{currentUser.email}</div>
            </div>
          </div>
          <div className="dropdown-divider"></div>
          <button className="dropdown-item" onClick={handleLogout}>
            🚪 Đăng xuất
          </button>
        </div>
      )}
    </div>
  );
}

export default UserProfile;