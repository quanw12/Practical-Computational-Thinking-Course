import React, { useState } from 'react';
import { useAuth } from './AuthContext';

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
}

function LoginModal({ isOpen, onClose }: LoginModalProps) {
  const { login } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleGoogleLogin = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      await login();
      onClose();
    } catch (error: any) {
      console.error('Login error:', error);
      
      // Hiển thị lỗi cụ thể hơn
      let errorMessage = 'Đăng nhập thất bại. ';
      if (error.code === 'auth/popup-closed-by-user') {
        errorMessage += 'Bạn đã đóng cửa sổ đăng nhập.';
      } else if (error.code === 'auth/popup-blocked') {
        errorMessage += 'Trình duyệt đã chặn popup. Vui lòng cho phép popup.';
      } else if (error.code === 'auth/operation-not-allowed') {
        errorMessage += 'Google đăng nhập chưa được kích hoạt.';
      } else if (error.code === 'auth/unauthorized-domain') {
        errorMessage += 'Domain không được ủy quyền.';
      } else {
        errorMessage += `Lỗi: ${error.message}`;
      }
      
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>🌟 Đăng nhập Vietnam Explorer</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        
        <div className="modal-body">
          <p>Đăng nhập để lưu các địa điểm yêu thích và trải nghiệm tính năng cá nhân hóa!</p>
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          <button 
            className={`google-login-button ${isLoading ? 'loading' : ''}`}
            onClick={handleGoogleLogin}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Đang đăng nhập...
              </>
            ) : (
              <>
                <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google" />
                Đăng nhập với Google
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default LoginModal;