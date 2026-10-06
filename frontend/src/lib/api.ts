import {
  User,
  UserProfile,
  LearningPath,
  SkillSummary,
  LessonDetail,
  LessonStartResponse,
  AnswerSubmission,
  AnswerResponse,
  LessonCompleteResponse,
  LeaderboardEntry,
  Achievement,
  AuthResponse
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
const TOKEN_KEY = "duo_access_token";

export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string | null): void {
  if (typeof window === "undefined") return;
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    localStorage.removeItem(TOKEN_KEY);
  }
}

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const token = getStoredToken();
  const authHeaders: Record<string, string> = {};
  if (token) {
    authHeaders["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${url}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders,
      ...(options?.headers || {})
    },
    ...options
  });

  if (!res.ok) {
    let errMessage = `Error ${res.status}: ${res.statusText}`;
    try {
      const errData = await res.json();
      if (errData && errData.detail) {
        errMessage = errData.detail;
      }
    } catch {
      // ignore json parse error
    }
    if (res.status === 401) {
      setStoredToken(null);
    }
    throw new Error(errMessage);
  }

  return res.json();
}

export async function apiRegister(body: {
  username: string;
  email: string;
  password: string;
  display_name: string;
}): Promise<AuthResponse> {
  const data = await fetchJson<AuthResponse>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify(body)
  });
  if (data.access_token) {
    setStoredToken(data.access_token);
  }
  return data;
}

export async function apiLogin(body: {
  email: string;
  password: string;
}): Promise<AuthResponse> {
  const data = await fetchJson<AuthResponse>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(body)
  });
  if (data.access_token) {
    setStoredToken(data.access_token);
  }
  return data;
}

export async function apiLogout(): Promise<void> {
  try {
    await fetchJson("/api/auth/logout", {
      method: "POST"
    });
  } catch {
    // Ignore network error on logout
  } finally {
    setStoredToken(null);
  }
}

export async function apiGetMe(): Promise<User> {
  return fetchJson<User>("/api/auth/me");
}

export async function fetchCurrentUser(): Promise<User> {
  return fetchJson<User>("/api/me");
}

export async function fetchUserProfile(): Promise<UserProfile> {
  return fetchJson<UserProfile>("/api/profile");
}

export async function fetchLearningPath(): Promise<LearningPath> {
  return fetchJson<LearningPath>("/api/path");
}

export async function fetchSkillDetail(skillId: number): Promise<SkillSummary> {
  return fetchJson<SkillSummary>(`/api/skills/${skillId}`);
}

export async function fetchLesson(lessonId: number): Promise<LessonDetail> {
  return fetchJson<LessonDetail>(`/api/lessons/${lessonId}`);
}

export async function startLesson(lessonId: number): Promise<LessonStartResponse> {
  return fetchJson<LessonStartResponse>(`/api/lessons/${lessonId}/start`, {
    method: "POST"
  });
}

export async function submitAnswer(lessonId: number, body: AnswerSubmission): Promise<AnswerResponse> {
  return fetchJson<AnswerResponse>(`/api/lessons/${lessonId}/answer`, {
    method: "POST",
    body: JSON.stringify(body)
  });
}

export async function completeLesson(lessonId: number, attemptId?: number): Promise<LessonCompleteResponse> {
  return fetchJson<LessonCompleteResponse>(`/api/lessons/${lessonId}/complete`, {
    method: "POST",
    body: JSON.stringify({ attempt_id: attemptId })
  });
}

export async function fetchLeaderboard(): Promise<LeaderboardEntry[]> {
  return fetchJson<LeaderboardEntry[]>("/api/leaderboard");
}

export async function fetchAchievements(): Promise<Achievement[]> {
  return fetchJson<Achievement[]>("/api/achievements");
}

export async function refillHearts(): Promise<{ hearts: number; message: string }> {
  return fetchJson<{ hearts: number; message: string }>("/api/hearts/refill", {
    method: "POST"
  });
}

export async function practiceHearts(): Promise<{ hearts: number; message: string }> {
  return fetchJson<{ hearts: number; message: string }>("/api/hearts/practice", {
    method: "POST"
  });
}

export async function simulateActivity(date: string, xpGained: number = 20): Promise<any> {
  return fetchJson("/api/dev/simulate-activity", {
    method: "POST",
    body: JSON.stringify({ simulated_date: date, xp_gained: xpGained })
  });
}

export async function updateDailyGoal(dailyGoal: number): Promise<any> {
  return fetchJson("/api/dev/update-goal", {
    method: "POST",
    body: JSON.stringify({ daily_goal: dailyGoal })
  });
}

export async function resetProgress(): Promise<any> {
  return fetchJson("/api/dev/reset-progress", {
    method: "POST"
  });
}
