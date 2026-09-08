import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext({
  user: null,
  isAuthenticated: true,
  isOpeningSplashActive: false,
  triggerOpeningSplash: () => {},
  login: async () => {},
  signup: async () => {},
  logout: () => {},
  resetPassword: async () => {}
});

const DEFAULT_USER = {
  name: 'Aakash S.',
  email: 'akash@foodguard.ai',
  role: 'Admin',
  avatar: 'AS'
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const savedUser = localStorage.getItem('foodguard_user');
      if (savedUser) {
        return JSON.parse(savedUser);
      }
      return DEFAULT_USER; // Default logged in for seamless demo experience
    } catch {
      return DEFAULT_USER;
    }
  });

  const [isOpeningSplashActive, setIsOpeningSplashActive] = useState(false);

  const triggerOpeningSplash = (callback) => {
    setIsOpeningSplashActive(true);
    setTimeout(() => {
      setIsOpeningSplashActive(false);
      if (callback) callback();
    }, 1400);
  };

  const login = async (email, password, remember = true) => {
    // Basic validation
    if (!email || !password) {
      throw new Error('Please enter both email and password.');
    }
    if (!email.includes('@')) {
      throw new Error('Please enter a valid email address.');
    }
    if (password.length < 6) {
      throw new Error('Password must be at least 6 characters.');
    }

    // Extract name from email or default
    const namePart = email.split('@')[0];
    const formattedName = namePart.charAt(0).toUpperCase() + namePart.slice(1);
    
    const authenticatedUser = {
      name: formattedName || 'Aakash S.',
      email: email,
      role: 'Inspector / Admin',
      avatar: (formattedName.slice(0, 2) || 'AS').toUpperCase()
    };

    if (remember) {
      try {
        localStorage.setItem('foodguard_user', JSON.stringify(authenticatedUser));
      } catch (e) {
        console.warn(e);
      }
    }

    setUser(authenticatedUser);
    return new Promise((resolve) => {
      triggerOpeningSplash(() => resolve(authenticatedUser));
    });
  };

  const signup = async (name, email, password) => {
    if (!name.trim()) {
      throw new Error('Please enter your full name.');
    }
    if (!email || !email.includes('@')) {
      throw new Error('Please enter a valid email address.');
    }
    if (password.length < 6) {
      throw new Error('Password must be at least 6 characters.');
    }

    const newUser = {
      name: name.trim(),
      email: email.trim(),
      role: 'Analyst',
      avatar: name.trim().slice(0, 2).toUpperCase()
    };

    try {
      localStorage.setItem('foodguard_user', JSON.stringify(newUser));
    } catch (e) {
      console.warn(e);
    }

    setUser(newUser);
    return new Promise((resolve) => {
      triggerOpeningSplash(() => resolve(newUser));
    });
  };

  const logout = () => {
    try {
      localStorage.removeItem('foodguard_user');
    } catch (e) {
      console.warn(e);
    }
    setUser(null);
  };

  const resetPassword = async (email) => {
    if (!email || !email.includes('@')) {
      throw new Error('Please enter a valid email address.');
    }
    // Simulate API delay
    await new Promise((res) => setTimeout(res, 800));
    return true;
  };

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated: Boolean(user),
      isOpeningSplashActive,
      triggerOpeningSplash,
      login,
      signup,
      logout,
      resetPassword
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
