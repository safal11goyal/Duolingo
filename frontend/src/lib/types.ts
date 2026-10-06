export interface User {
  id: number;
  username: string;
  display_name: string;
  avatar: string;
  xp: number;
  gems: number;
  hearts: number;
  streak: number;
  daily_goal: number;
  last_active_at: string;
  created_at: string;
  updated_at: string;
}

export interface UserProfile extends User {
  daily_goal_progress: number;
  daily_goal_completed: boolean;
  completed_skills_count: number;
  completed_lessons_count: number;
  crowns_count: number;
  league: string;
  rank: number;
}

export interface ExerciseOption {
  id: number;
  text: string;
}

export interface Exercise {
  id: number;
  lesson_id: number;
  type: "multiple_choice" | "translate" | "word_bank" | "match_pairs" | "fill_blank" | "type_answer";
  question: string;
  order_index: number;
  xp: number;
  options: ExerciseOption[];
  metadata?: {
    tokens?: string[];
    left_items?: string[];
    right_items?: string[];
    pairs_count?: number;
  };
}

export interface LessonSummary {
  id: number;
  skill_id: number;
  title: string;
  order_index: number;
  xp_reward: number;
  exercise_count: number;
}

export interface LessonDetail {
  id: number;
  skill_id: number;
  title: string;
  order_index: number;
  xp_reward: number;
  exercises: Exercise[];
}

export interface SkillSummary {
  id: number;
  unit_id: number;
  title: string;
  description: string;
  order_index: number;
  xp_reward: number;
  status: "locked" | "available" | "in_progress" | "completed";
  crown_level: number;
  completed_lessons: number;
  total_lessons: number;
  lessons: LessonSummary[];
}

export interface UnitSummary {
  id: number;
  course_id: number;
  title: string;
  description: string;
  order_index: number;
  skills: SkillSummary[];
}

export interface LearningPath {
  course_name: string;
  source_language: string;
  target_language: string;
  units: UnitSummary[];
}

export interface LessonStartResponse {
  attempt_id: number;
  lesson_id: number;
  started_at: string;
  hearts_remaining: number;
  total_exercises: number;
}

export interface AnswerSubmission {
  exercise_id: number;
  answer: any;
  attempt_id?: number;
}

export interface AnswerResponse {
  correct: boolean;
  correct_answer: string;
  explanation?: string;
  xp_earned: number;
  hearts_remaining: number;
  is_lesson_complete: boolean;
}

export interface LessonCompleteResponse {
  success: boolean;
  lesson_id: number;
  xp_earned: number;
  total_xp: number;
  hearts_remaining: number;
  streak: number;
  skill_progress: {
    skill_id: number;
    status: string;
    crown_level: number;
    completed_lessons: number;
    total_lessons: number;
  };
  next_skill_unlocked: boolean;
  achievements_unlocked: string[];
}

export interface LeaderboardEntry {
  rank: number;
  user_id: number;
  username: string;
  display_name: string;
  avatar: string;
  xp: number;
  is_current_user: boolean;
}

export interface Achievement {
  id: number;
  name: string;
  description: string;
  icon: string;
  requirement_type: string;
  requirement_value: number;
  unlocked: boolean;
  unlocked_at?: string;
  progress: number;
}
