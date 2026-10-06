"""initial_schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-10-06 22:58:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0001_initial_schema'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=False),
        sa.Column('avatar', sa.String(length=255), server_default='/avatars/alex.png', nullable=True),
        sa.Column('xp', sa.Integer(), server_default='0', nullable=False),
        sa.Column('gems', sa.Integer(), server_default='500', nullable=False),
        sa.Column('hearts', sa.Integer(), server_default='5', nullable=False),
        sa.Column('streak', sa.Integer(), server_default='0', nullable=False),
        sa.Column('daily_goal', sa.Integer(), server_default='20', nullable=False),
        sa.Column('last_active_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. courses
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('source_language', sa.String(length=50), server_default='English', nullable=False),
        sa.Column('target_language', sa.String(length=50), server_default='Spanish', nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.String(length=50), server_default='Beginner', nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)

    # 3. units
    op.create_table(
        'units',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('order_index', sa.Integer(), server_default='1', nullable=False),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_units_id'), 'units', ['id'], unique=False)

    # 4. skills
    op.create_table(
        'skills',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('unit_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('order_index', sa.Integer(), server_default='1', nullable=False),
        sa.Column('xp_reward', sa.Integer(), server_default='10', nullable=False),
        sa.ForeignKeyConstraint(['unit_id'], ['units.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_skills_id'), 'skills', ['id'], unique=False)

    # 5. lessons
    op.create_table(
        'lessons',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), server_default='1', nullable=False),
        sa.Column('xp_reward', sa.Integer(), server_default='10', nullable=False),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lessons_id'), 'lessons', ['id'], unique=False)

    # 6. exercises (questions)
    op.create_table(
        'exercises',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('correct_answer', sa.Text(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), server_default='1', nullable=False),
        sa.Column('xp', sa.Integer(), server_default='2', nullable=False),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercises_id'), 'exercises', ['id'], unique=False)

    # 7. exercise_options
    op.create_table(
        'exercise_options',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('exercise_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(length=255), nullable=False),
        sa.Column('is_correct', sa.Boolean(), server_default='0', nullable=False),
        sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercise_options_id'), 'exercise_options', ['id'], unique=False)

    # 8. user_skill_progresses
    op.create_table(
        'user_skill_progresses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), server_default='locked', nullable=False),
        sa.Column('xp', sa.Integer(), server_default='0', nullable=False),
        sa.Column('crown_level', sa.Integer(), server_default='0', nullable=False),
        sa.Column('completed_lessons', sa.Integer(), server_default='0', nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'skill_id', name='uq_user_skill')
    )
    op.create_index(op.f('ix_user_skill_progresses_id'), 'user_skill_progresses', ['id'], unique=False)
    op.create_index(op.f('ix_user_skill_progresses_user_id'), 'user_skill_progresses', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_skill_progresses_skill_id'), 'user_skill_progresses', ['skill_id'], unique=False)

    # 9. lesson_attempts
    op.create_table(
        'lesson_attempts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('score', sa.Integer(), server_default='0', nullable=False),
        sa.Column('correct_answers', sa.Integer(), server_default='0', nullable=False),
        sa.Column('wrong_answers', sa.Integer(), server_default='0', nullable=False),
        sa.Column('xp_earned', sa.Integer(), server_default='0', nullable=False),
        sa.Column('hearts_lost', sa.Integer(), server_default='0', nullable=False),
        sa.Column('completed', sa.Boolean(), server_default='0', nullable=False),
        sa.Column('attempts', sa.Integer(), server_default='1', nullable=False),
        sa.Column('last_attempted_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lesson_attempts_id'), 'lesson_attempts', ['id'], unique=False)
    op.create_index(op.f('ix_lesson_attempts_user_id'), 'lesson_attempts', ['user_id'], unique=False)
    op.create_index(op.f('ix_lesson_attempts_lesson_id'), 'lesson_attempts', ['lesson_id'], unique=False)

    # 10. user_answers
    op.create_table(
        'user_answers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('lesson_id', sa.Integer(), nullable=True),
        sa.Column('attempt_id', sa.Integer(), nullable=True),
        sa.Column('submitted_answer', sa.String(length=500), nullable=False),
        sa.Column('is_correct', sa.Boolean(), server_default='0', nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['attempt_id'], ['lesson_attempts.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['question_id'], ['exercises.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_answers_id'), 'user_answers', ['id'], unique=False)
    op.create_index(op.f('ix_user_answers_user_id'), 'user_answers', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_answers_question_id'), 'user_answers', ['question_id'], unique=False)
    op.create_index(op.f('ix_user_answers_lesson_id'), 'user_answers', ['lesson_id'], unique=False)
    op.create_index(op.f('ix_user_answers_attempt_id'), 'user_answers', ['attempt_id'], unique=False)

    # 11. daily_activities
    op.create_table(
        'daily_activities',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('activity_date', sa.Date(), nullable=False),
        sa.Column('xp_earned', sa.Integer(), server_default='0', nullable=False),
        sa.Column('lessons_completed', sa.Integer(), server_default='0', nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'activity_date', name='uq_user_daily_activity')
    )
    op.create_index(op.f('ix_daily_activities_id'), 'daily_activities', ['id'], unique=False)
    op.create_index(op.f('ix_daily_activities_user_id'), 'daily_activities', ['user_id'], unique=False)

    # 12. achievements
    op.create_table(
        'achievements',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('icon', sa.String(length=50), nullable=False),
        sa.Column('requirement_type', sa.String(length=50), nullable=False),
        sa.Column('requirement_value', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_achievements_id'), 'achievements', ['id'], unique=False)

    # 13. user_achievements
    op.create_table(
        'user_achievements',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('achievement_id', sa.Integer(), nullable=False),
        sa.Column('unlocked_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'achievement_id', name='uq_user_achievement')
    )
    op.create_index(op.f('ix_user_achievements_id'), 'user_achievements', ['id'], unique=False)
    op.create_index(op.f('ix_user_achievements_user_id'), 'user_achievements', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_achievements_achievement_id'), 'user_achievements', ['achievement_id'], unique=False)


def downgrade() -> None:
    op.drop_table('user_achievements')
    op.drop_table('achievements')
    op.drop_table('daily_activities')
    op.drop_table('user_answers')
    op.drop_table('lesson_attempts')
    op.drop_table('user_skill_progresses')
    op.drop_table('exercise_options')
    op.drop_table('exercises')
    op.drop_table('lessons')
    op.drop_table('skills')
    op.drop_table('units')
    op.drop_table('courses')
    op.drop_table('users')
