"use client";

import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { User } from "@/lib/types";
import { apiGetMe, apiLogin, apiRegister, apiLogout, getStoredToken } from "@/lib/api";

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: {
    username: string;
    email: string;
    password: string;
    display_name: string;
  }) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const refreshUser = useCallback(async () => {
    try {
      const currentUser = await apiGetMe();
      setUser(currentUser);
      setToken(getStoredToken());
    } catch {
      setUser(null);
      setToken(null);
    }
  }, []);

  useEffect(() => {
    const initAuth = async () => {
      try {
        const currentUser = await apiGetMe();
        setUser(currentUser);
        setToken(getStoredToken());
      } catch {
        setUser(null);
        setToken(null);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const res = await apiLogin({ email, password });
    setUser(res.user);
    setToken(res.access_token);
  };

  const register = async (data: {
    username: string;
    email: string;
    password: string;
    display_name: string;
  }) => {
    const res = await apiRegister(data);
    setUser(res.user);
    setToken(res.access_token);
  };

  const logout = async () => {
    try {
      await apiLogout();
    } finally {
      setUser(null);
      setToken(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
