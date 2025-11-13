import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAuthorized, setIsAuthorized] = useState(false);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('jwt_token'));

  // Check if user has valid token on app load
  useEffect(() => {
    const storedToken = localStorage.getItem('jwt_token');
    const storedUser = localStorage.getItem('user_info');
    
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
      setIsAuthorized(true);
    }
    setLoading(false);
  }, []);

  const login = async (googleCredential) => {
    try {
      setLoading(true);
      
      // Send Google credential to your backend for verification
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/google`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ credential: googleCredential }),
      });

      const data = await response.json();
      
      if (data.success) {
        // Store JWT token and user info
        localStorage.setItem('jwt_token', data.token);
        localStorage.setItem('user_info', JSON.stringify(data.user));
        
        setToken(data.token);
        setUser(data.user);
        setIsAuthenticated(true);
        setIsAuthorized(data.authorized);
        
        return { success: true };
      } else {
        return { success: false, message: data.message };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, message: 'Login failed' };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_info');
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
    setIsAuthorized(false);
  };

  const value = {
    user,
    isAuthenticated,
    isAuthorized,
    loading,
    token,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;