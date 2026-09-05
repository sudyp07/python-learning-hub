#!/usr/bin/env python3
"""
Smart Habit Tracker with AI Predictions - Single File Project
Features:
- Track daily habits with streaks and goals
- AI-powered habit completion predictions
- Progress visualization with trends
- Smart reminders and notifications
- Habit analytics and insights
"""

import os
import sys
import json
import sqlite3
import pickle
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple, Any
from collections import defaultdict
import math
import random

# Machine Learning libraries
try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    ML_AVAILABLE = True
except ImportError:
    print("⚠️  scikit-learn not installed. AI features will be disabled.")
    print("   Install with: pip install scikit-learn numpy")
    ML_AVAILABLE = False

# Visualization libraries
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.patches import Rectangle
    plt.style.use('seaborn-v0_8-darkgrid')
    VIZ_AVAILABLE = True
except ImportError:
    print("⚠️  matplotlib not installed. Visualization features will be disabled.")
    print("   Install with: pip install matplotlib")
    VIZ_AVAILABLE = False

# ============== DATABASE ==============

class HabitDatabase:
    """SQLite database for habit tracking"""
    
    def __init__(self, db_path: str = "habits.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Habits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                frequency TEXT DEFAULT 'daily',
                goal_days_per_week INTEGER DEFAULT 5,
                target_count INTEGER DEFAULT 1,
                unit TEXT DEFAULT 'times',
                created_date DATE NOT NULL,
                active INTEGER DEFAULT 1,
                reminder_time TEXT,
                color TEXT DEFAULT '#4CAF50'
            )
        ''')
        
        # Habit logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                log_date DATE NOT NULL,
                count INTEGER DEFAULT 1,
                note TEXT,
                FOREIGN KEY (habit_id) REFERENCES habits (id),
                UNIQUE(habit_id, log_date)
            )
        ''')
        
        # Habit streaks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_streaks (
                habit_id INTEGER PRIMARY KEY,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_log_date DATE,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )
        ''')
        
        # AI predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                prediction_date DATE NOT NULL,
                probability REAL,
                model_version TEXT,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_habit(self, name: str, description: str = "", category: str = "General",
                  frequency: str = "daily", goal_days_per_week: int = 5,
                  target_count: int = 1, unit: str = "times",
                  reminder_time: Optional[str] = None,
                  color: str = "#4CAF50") -> int:
        """Add a new habit"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO habits 
            (name, description, category, frequency, goal_days_per_week,
             target_count, unit, created_date, reminder_time, color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, category, frequency, goal_days_per_week,
              target_count, unit, date.today().isoformat(), reminder_time, color))
        
        habit_id = cursor.lastrowid
        
        # Initialize streak
        cursor.execute('''
            INSERT INTO habit_streaks (habit_id, current_streak, longest_streak)
            VALUES (?, 0, 0)
        ''', (habit_id,))
        
        conn.commit()
        conn.close()
        return habit_id
    
    def log_habit(self, habit_id: int, count: int = 1, note: str = ""):
        """Log a habit completion"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = date.today().isoformat()
        
        # Check if already logged today
        cursor.execute('''
            SELECT count FROM habit_logs
            WHERE habit_id = ? AND log_date = ?
        ''', (habit_id, today))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing log
            new_count = existing[0] + count
            cursor.execute('''
                UPDATE habit_logs
                SET count = ?, note = ?
                WHERE habit_id = ? AND log_date = ?
            ''', (new_count, note, habit_id, today))
        else:
            # Insert new log
            cursor.execute('''
                INSERT INTO habit_logs (habit_id, log_date, count, note)
                VALUES (?, ?, ?, ?)
            ''', (habit_id, today, count, note))
        
        # Update streaks
        self._update_streaks(habit_id)
        
        conn.commit()
        conn.close()
    
    def _update_streaks(self, habit_id: int):
        """Update streak for a habit"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all logs for this habit
        cursor.execute('''
            SELECT log_date FROM habit_logs
            WHERE habit_id = ?
            ORDER BY log_date DESC
        ''', (habit_id,))
        
        logs = [row[0] for row in cursor.fetchall()]
        
        if not logs:
            cursor.execute('''
                UPDATE habit_streaks
                SET current_streak = 0, last_log_date = NULL
                WHERE habit_id = ?
            ''', (habit_id,))
            conn.commit()
            conn.close()
            return
        
        # Calculate current streak
        current_streak = 0
        check_date = date.today()
        
        # Get goal days per week for this habit
        cursor.execute('SELECT goal_days_per_week FROM habits WHERE id = ?', (habit_id,))
        goal_days = cursor.fetchone()[0]
        
        # Check if habit was logged today
        if date.today().isoformat() not in logs:
            # If not logged today, check if yesterday was logged
            yesterday = (date.today() - timedelta(days=1)).isoformat()
            if yesterday not in logs:
                # Streak broken
                current_streak = 0
            else:
                # Count backwards from yesterday
                check_date = date.today() - timedelta(days=1)
        
        # Count consecutive days
        while check_date.isoformat() in logs:
            current_streak += 1
            check_date -= timedelta(days=1)
        
        # Get longest streak
        cursor.execute('SELECT longest_streak FROM habit_streaks WHERE habit_id = ?', (habit_id,))
        longest_streak = cursor.fetchone()[0]
        
        if current_streak > longest_streak:
            longest_streak = current_streak
        
        # Update streaks
        cursor.execute('''
            UPDATE habit_streaks
            SET current_streak = ?, longest_streak = ?, last_log_date = ?
            WHERE habit_id = ?
        ''', (current_streak, longest_streak, date.today().isoformat(), habit_id))
        
        conn.commit()
        conn.close()
    
    def get_habits(self, active_only: bool = True) -> List[Dict]:
        """Get all habits"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM habits"
        if active_only:
            query += " WHERE active = 1"
        query += " ORDER BY created_date DESC"
        
        cursor.execute(query)
        habits = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        # Add streak info
        for habit in habits:
            streak = self.get_streak_info(habit['id'])
            habit['current_streak'] = streak['current']
            habit['longest_streak'] = streak['longest']
            habit['today_completed'] = self.is_logged_today(habit['id'])
        
        return habits
    
    def get_streak_info(self, habit_id: int) -> Dict:
        """Get streak information for a habit"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT current_streak, longest_streak, last_log_date
            FROM habit_streaks
            WHERE habit_id = ?
        ''', (habit_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'current': result[0] or 0,
                'longest': result[1] or 0,
                'last_log': result[2]
            }
        return {'current': 0, 'longest': 0, 'last_log': None}
    
    def is_logged_today(self, habit_id: int) -> bool:
        """Check if habit was logged today"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM habit_logs
            WHERE habit_id = ? AND log_date = ?
        ''', (habit_id, date.today().isoformat()))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    def get_logs(self, habit_id: int, days: int = 30) -> List[Dict]:
        """Get habit logs for the last N days"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        start_date = (date.today() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT * FROM habit_logs
            WHERE habit_id = ? AND log_date >= ?
            ORDER BY log_date ASC
        ''', (habit_id, start_date))
        
        logs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return logs
    
    def get_logs_by_date(self, habit_id: int, start_date: str, end_date: str) -> List[Dict]:
        """Get habit logs for a date range"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM habit_logs
            WHERE habit_id = ? AND log_date BETWEEN ? AND ?
            ORDER BY log_date ASC
        ''', (habit_id, start_date, end_date))
        
        logs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return logs
    
    def delete_habit(self, habit_id: int) -> bool:
        """Delete a habit and all associated data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM habit_logs WHERE habit_id = ?', (habit_id,))
            cursor.execute('DELETE FROM habit_streaks WHERE habit_id = ?', (habit_id,))
            cursor.execute('DELETE FROM habit_predictions WHERE habit_id = ?', (habit_id,))
            cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
            conn.commit()
            conn.close()
            return True
        except:
            conn.close()
            return False
    
    def update_habit(self, habit_id: int, **kwargs):
        """Update habit details"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        for key, value in kwargs.items():
            if key in ['name', 'description', 'category', 'frequency', 
                      'goal_days_per_week', 'target_count', 'unit', 
                      'reminder_time', 'color', 'active']:
                updates.append(f"{key} = ?")
                values.append(value)
        
        if updates:
            values.append(habit_id)
            query = f"UPDATE habits SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()

# ============== AI PREDICTOR ==============

class HabitPredictor:
    """AI-powered habit completion predictor"""
    
    def __init__(self, db: HabitDatabase):
        self.db = db
        self.models = {}
        self.scalers = {}
        self.model_file = "habit_models.pkl"
        self.load_models()
    
    def load_models(self):
        """Load trained models from file"""
        if not ML_AVAILABLE:
            return
        
        try:
            if os.path.exists(self.model_file):
                with open(self.model_file, 'rb') as f:
                    data = pickle.load(f)
                    self.models = data.get('models', {})
                    self.scalers = data.get('scalers', {})
        except:
            pass
    
    def save_models(self):
        """Save trained models to file"""
        if not ML_AVAILABLE:
            return
        
        try:
            with open(self.model_file, 'wb') as f:
                pickle.dump({
                    'models': self.models,
                    'scalers': self.scalers
                }, f)
        except:
            pass
    
    def prepare_features(self, habit_id: int, days_back: int = 30) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for ML model"""
        # Get habit data
        habit = self.db.get_habits(active_only=False)
        habit = next((h for h in habit if h['id'] == habit_id), None)
        if not habit:
            return None, None
        
        logs = self.db.get_logs(habit_id, days_back)
        log_dict = {log['log_date']: log['count'] for log in logs}
        
        # Create feature matrix
        features = []
        targets = []
        
        for i in range(days_back - 7):  # Need at least 7 days of history
            current_date = date.today() - timedelta(days=days_back - i)
            
            # Features
            feat = []
            
            # Day of week (0-6)
            feat.append(current_date.weekday())
            
            # Day of month (1-31)
            feat.append(current_date.day)
            
            # Month (1-12)
            feat.append(current_date.month)
            
            # Is weekend
            feat.append(1 if current_date.weekday() >= 5 else 0)
            
            # Previous 7 days' status
            for j in range(1, 8):
                prev_date = current_date - timedelta(days=j)
                prev_str = prev_date.isoformat()
                feat.append(1 if prev_str in log_dict else 0)
            
            # Rolling average (last 7 days)
            avg = sum(1 for j in range(1, 8) 
                     if (current_date - timedelta(days=j)).isoformat() in log_dict) / 7
            feat.append(avg)
            
            # Streak at this point
            streak = 0
            check_date = current_date - timedelta(days=1)
            while check_date.isoformat() in log_dict:
                streak += 1
                check_date -= timedelta(days=1)
            feat.append(streak)
            
            features.append(feat)
            
            # Target: was habit completed on this day?
            target = 1 if current_date.isoformat() in log_dict else 0
            targets.append(target)
        
        return np.array(features), np.array(targets)
    
    def train_model(self, habit_id: int) -> bool:
        """Train AI model for a habit"""
        if not ML_AVAILABLE:
            print("❌ ML libraries not available")
            return False
        
        X, y = self.prepare_features(habit_id, 60)  # Use 60 days of data
        
        if X is None or len(X) < 10:
            return False
        
        try:
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train multiple models and use ensemble
            models = [
                RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42),
                GradientBoostingClassifier(n_estimators=50, learning_rate=0.1, random_state=42)
            ]
            
            best_model = None
            best_accuracy = 0
            
            for model in models:
                # Train-test split
                X_train, X_test, y_train, y_test = train_test_split(
                    X_scaled, y, test_size=0.2, random_state=42
                )
                
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_model = model
            
            if best_model:
                self.models[habit_id] = best_model
                self.scalers[habit_id] = scaler
                self.save_models()
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Model training failed: {e}")
            return False
    
    def predict_completion(self, habit_id: int, days_ahead: int = 7) -> List[Dict]:
        """Predict habit completion probabilities for future days"""
        if not ML_AVAILABLE:
            return []
        
        if habit_id not in self.models:
            # Try to train model
            if not self.train_model(habit_id):
                return []
        
        try:
            model = self.models[habit_id]
            scaler = self.scalers[habit_id]
            
            # Get recent data for feature preparation
            logs = self.db.get_logs(habit_id, 30)
            log_dict = {log['log_date']: log['count'] for log in logs}
            
            predictions = []
            
            for i in range(1, days_ahead + 1):
                future_date = date.today() + timedelta(days=i)
                
                # Prepare features for this day
                feat = []
                feat.append(future_date.weekday())
                feat.append(future_date.day)
                feat.append(future_date.month)
                feat.append(1 if future_date.weekday() >= 5 else 0)
                
                # Previous 7 days (using historical or predicted data)
                for j in range(1, 8):
                    prev_date = future_date - timedelta(days=j)
                    prev_str = prev_date.isoformat()
                    feat.append(1 if prev_str in log_dict else 0)
                
                # Rolling average
                avg = sum(1 for j in range(1, 8) 
                         if (future_date - timedelta(days=j)).isoformat() in log_dict) / 7
                feat.append(avg)
                
                # Current streak
                streak = 0
                check_date = future_date - timedelta(days=1)
                while check_date.isoformat() in log_dict:
                    streak += 1
                    check_date -= timedelta(days=1)
                feat.append(streak)
                
                # Predict
                feat_scaled = scaler.transform([feat])
                probability = model.predict_proba(feat_scaled)[0][1]  # Probability of completion
                
                predictions.append({
                    'date': future_date.isoformat(),
                    'probability': float(probability),
                    'day_name': future_date.strftime('%A'),
                    'weekday': future_date.weekday()
                })
            
            return predictions
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            return []

# ============== VISUALIZER ==============

class HabitVisualizer:
    """Visualize habit data"""
    
    @staticmethod
    def plot_habit_progress(habit: Dict, logs: List[Dict], days: int = 30):
        """Plot habit progress over time"""
        if not VIZ_AVAILABLE:
            print("❌ Matplotlib not available")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Habit completion heatmap
        ax1 = axes[0, 0]
        HabitVisualizer._plot_heatmap(habit, logs, ax1)
        
        # 2. Streak history
        ax2 = axes[0, 1]
        HabitVisualizer._plot_streaks(habit, logs, ax2)
        
        # 3. Weekly pattern
        ax3 = axes[1, 0]
        HabitVisualizer._plot_weekly_pattern(habit, logs, ax3)
        
        # 4. Predictions (if available)
        ax4 = axes[1, 1]
        HabitVisualizer._plot_predictions(habit, ax4)
        
        plt.suptitle(f"📊 Habit Progress: {habit['name']}", fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def _plot_heatmap(habit: Dict, logs: List[Dict], ax):
        """Plot heatmap of habit completion"""
        # Create calendar data
        today = date.today()
        start_date = today - timedelta(days=90)
        
        # Create matrix for 13 weeks (3 months)
        dates = [start_date + timedelta(days=i) for i in range(91)]
        log_dates = {log['log_date']: log['count'] for log in logs}
        
        # Prepare data for heatmap
        weeks = []
        week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        current_week = []
        for dt in dates:
            current_week.append(1 if dt.isoformat() in log_dates else 0)
            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []
        
        if current_week:
            while len(current_week) < 7:
                current_week.append(0)
            weeks.append(current_week)
        
        # Convert to numpy array
        data = np.array(weeks)
        
        # Plot heatmap
        im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
        
        # Formatting
        ax.set_yticks(range(len(weeks)))
        ax.set_yticklabels([f'Week {i+1}' for i in range(len(weeks))])
        ax.set_xticks(range(7))
        ax.set_xticklabels(week_days)
        ax.set_title('90-Day Habit Heatmap')
        
        # Add colorbar
        plt.colorbar(im, ax=ax, label='Completed')
    
    @staticmethod
    def _plot_streaks(habit: Dict, logs: List[Dict], ax):
        """Plot streak history"""
        if not logs:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            ax.set_title('Streak History')
            return
        
        # Calculate daily streak
        log_dates = {log['log_date']: log['count'] for log in logs}
        start_date = date.today() - timedelta(days=30)
        
        streak_data = []
        current_streak = 0
        
        for i in range(30):
            current_date = start_date + timedelta(days=i)
            is_completed = current_date.isoformat() in log_dates
            
            if is_completed:
                current_streak += 1
            else:
                if current_streak > 0:
                    streak_data.append((current_date.isoformat(), current_streak))
                current_streak = 0
        
        if streak_data:
            dates = [datetime.fromisoformat(d[0]) for d in streak_data]
            streaks = [d[1] for d in streak_data]
            ax.bar(dates, streaks, color='#4CAF50', alpha=0.7)
            ax.set_xlabel('Date')
            ax.set_ylabel('Streak Length (days)')
            ax.set_title(f'Streak History (Current: {habit["current_streak"]} days)')
            
            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        else:
            ax.text(0.5, 0.5, 'No streaks yet', ha='center', va='center')
            ax.set_title('Streak History')
    
    @staticmethod
    def _plot_weekly_pattern(habit: Dict, logs: List[Dict], ax):
        """Plot weekly completion pattern"""
        if not logs:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            ax.set_title('Weekly Pattern')
            return
        
        # Aggregate by day of week
        day_counts = defaultdict(int)
        day_totals = defaultdict(int)
        
        for log in logs:
            log_date = datetime.fromisoformat(log['log_date'])
            day_name = log_date.strftime('%A')
            day_counts[day_name] += log['count']
            day_totals[day_name] += 1
        
        # Calculate average
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        averages = []
        
        for day in day_order:
            if day_totals[day] > 0:
                avg = day_counts[day] / day_totals[day]
            else:
                avg = 0
            averages.append(avg)
        
        # Plot
        bars = ax.bar(day_order, averages, color='#2196F3', alpha=0.7)
        
        # Color weekend differently
        for i, bar in enumerate(bars):
            if i >= 5:  # Saturday and Sunday
                bar.set_color('#FF9800')
        
        ax.set_ylabel('Average Completions')
        ax.set_title('Weekly Pattern (Average per Day)')
        ax.set_ylim(0, max(averages) * 1.2 if averages else 1)
        
        # Add value labels
        for i, v in enumerate(averages):
            if v > 0:
                ax.text(i, v + 0.05, f'{v:.1f}', ha='center', va='bottom')
    
    @staticmethod
    def _plot_predictions(habit: Dict, ax):
        """Plot AI predictions"""
        # Placeholder - will be filled with actual predictions
        if habit.get('id') and False:  # Disabled until we implement prediction visualization
            pass
        else:
            ax.text(0.5, 0.5, 'AI Predictions Coming Soon', ha='center', va='center')
            ax.set_title('Completion Predictions')
            ax.set_xlabel('Day')
            ax.set_ylabel('Probability')

# ============== HABIT TRACKER ==============

class SmartHabitTracker:
    """Main habit tracker application"""
    
    def __init__(self):
        self.db = HabitDatabase()
        self.predictor = HabitPredictor(self.db)
        self.visualizer = HabitVisualizer()
    
    def run(self):
        """Run the habit tracker CLI"""
        self.show_welcome()
        
        while True:
            try:
                command = input("\n💪 > ").strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Keep building those habits!")
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd in ['list', 'ls']:
                    self.list_habits()
                elif cmd in ['add', 'a']:
                    self.add_habit()
                elif cmd in ['log', 'l']:
                    self.log_habit(parts[1] if len(parts) > 1 else None)
                elif cmd in ['track', 't']:
                    self.track_habit(parts[1] if len(parts) > 1 else None)
                elif cmd in ['predict', 'p']:
                    self.show_predictions(parts[1] if len(parts) > 1 else None)
                elif cmd in ['analyze', 'an']:
                    self.analyze_habit(parts[1] if len(parts) > 1 else None)
                elif cmd in ['train', 'tr']:
                    self.train_ai(parts[1] if len(parts) > 1 else None)
                elif cmd in ['stats', 'st']:
                    self.show_stats()
                elif cmd in ['delete', 'del']:
                    self.delete_habit(parts[1] if len(parts) > 1 else None)
                elif cmd == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    print(f"❌ Unknown command: {cmd}")
                    print("   Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Keep building those habits!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_welcome(self):
        """Show welcome message"""
        print("\n" + "="*60)
        print("💪 SMART HABIT TRACKER with AI Predictions")
        print("="*60)
        print("\n🎯 Track your habits with AI-powered insights!")
        print("🤖 Get predictions on when you're most likely to succeed")
        print("📊 Visualize your progress and patterns")
        print("\nType 'help' to see all commands")
        print("="*60)
    
    def show_help(self):
        """Show help message"""
        print("\n" + "="*60)
        print("💪 Available Commands:")
        print("="*60)
        print("\n  📝 add / a          - Add a new habit")
        print("  📋 list / ls        - List all habits")
        print("  ✅ log / l <id>     - Log habit completion")
        print("  📊 track / t <id>   - View habit progress")
        print("  🤖 predict / p <id> - Get AI predictions")
        print("  📈 analyze / an <id>- Analyze habit patterns")
        print("  🧠 train / tr <id>  - Train AI model for habit")
        print("  📊 stats / st       - Show overall statistics")
        print("  🗑️  delete / del <id>- Delete a habit")
        print("  🧹 clear            - Clear screen")
        print("  ❓ help             - Show this help")
        print("  🚪 quit / exit / q  - Exit")
        print("\n" + "="*60)
    
    def add_habit(self):
        """Add a new habit"""
        print("\n📝 Add New Habit")
        print("-" * 40)
        
        name = input("Habit name: ").strip()
        if not name:
            print("❌ Name is required")
            return
        
        description = input("Description (optional): ").strip()
        category = input("Category (Health/Productivity/Wellness/Other): ").strip() or "General"
        frequency = input("Frequency (daily/weekly): ").strip().lower() or "daily"
        
        goal_days = 5
        if frequency == "daily":
            goal_days = int(input("Goal days per week (1-7): ").strip() or "5")
            goal_days = max(1, min(7, goal_days))
        
        target_count = int(input("Target count per day: ").strip() or "1")
        unit = input("Unit (times/minutes/pages/etc): ").strip() or "times"
        
        color = input("Color (hex code, e.g., #4CAF50): ").strip() or "#4CAF50"
        
        # Add the habit
        habit_id = self.db.add_habit(
            name=name,
            description=description,
            category=category,
            frequency=frequency,
            goal_days_per_week=goal_days,
            target_count=target_count,
            unit=unit,
            color=color
        )
        
        print(f"✅ Habit added! (ID: {habit_id})")
        
        # Ask to log today
        log_now = input("Log it for today? (y/n): ").strip().lower()
        if log_now == 'y':
            self.db.log_habit(habit_id, target_count)
            print("✅ Logged for today!")
        
        # Train AI model
        train_ai = input("Train AI model for predictions? (y/n): ").strip().lower()
        if train_ai == 'y':
            if self.predictor.train_model(habit_id):
                print("✅ AI model trained successfully!")
            else:
                print("⚠️  Need at least 10 days of data to train AI")
    
    def list_habits(self):
        """List all habits"""
        habits = self.db.get_habits()
        
        if not habits:
            print("📭 No habits yet. Add one with 'add'")
            return
        
        print("\n📋 Your Habits")
        print("="*70)
        
        for habit in habits:
            # Determine status
            status = "✅ Today" if habit['today_completed'] else "⏳ Pending"
            if habit['frequency'] == 'daily':
                progress = f"{habit['current_streak']} day streak"
            else:
                progress = f"Streak: {habit['current_streak']} days"
            
            print(f"  [{habit['id']}] {habit['name']}")
            print(f"      {status} | {progress} | Longest: {habit['longest_streak']} days")
            if habit['description']:
                print(f"      📝 {habit['description']}")
            print(f"      🏷️  {habit['category']} | Target: {habit['target_count']} {habit['unit']} per day")
            print("-"*70)
    
    def log_habit(self, habit_id: str):
        """Log a habit completion"""
        if not habit_id:
            print("❌ Please provide habit ID: log <id>")
            return
        
        try:
            habit_id = int(habit_id)
        except:
            print("❌ Invalid habit ID")
            return
        
        # Get habit
        habits = self.db.get_habits(active_only=False)
        habit = next((h for h in habits if h['id'] == habit_id), None)
        
        if not habit:
            print(f"❌ Habit {habit_id} not found")
            return
        
        count = int(input(f"How many {habit['unit']}? (default: {habit['target_count']}): ").strip() or habit['target_count'])
        note = input("Note (optional): ").strip()
        
        self.db.log_habit(habit_id, count, note)
        print(f"✅ Logged {count} {habit['unit']} for {habit['name']}!")
        
        # Update predictions
        self.predictor.train_model(habit_id)
    
    def track_habit(self, habit_id: str):
        """View habit progress"""
        if not habit_id:
            print("❌ Please provide habit ID: track <id>")
            return
        
        try:
            habit_id = int(habit_id)
        except:
            print("❌ Invalid habit ID")
            return
        
        # Get habit
        habits = self.db.get_habits(active_only=False)
        habit = next((h for h in habits if h['id'] == habit_id), None)
        
        if not habit:
            print(f"❌ Habit {habit_id} not found")
            return
        
        # Get logs
        logs = self.db.get_logs(habit_id, 30)
        
        print(f"\n📊 Habit Progress: {habit['name']}")
        print("="*50)
        
        # Stats
        completed_days = len(logs)
        total_days = 30
        completion_rate = (completed_days / total_days) * 100
        
        print(f"  📅 Last 30 days:")
        print(f"     Completed: {completed_days}/{total_days} days")
        print(f"     Rate: {completion_rate:.1f}%")
        print(f"  🔥 Current streak: {habit['current_streak']} days")
        print(f"  🏆 Longest streak: {habit['longest_streak']} days")
        
        # Show last 7 days
        print("\n  📆 Last 7 days:")
        week_days = []
        for i in range(7, 0, -1):
            check_date = date.today() - timedelta(days=i)
            day_str = check_date.strftime('%a')
            is_completed = check_date.isoformat() in [log['log_date'] for log in logs]
            symbol = "✅" if is_completed else "⬜"
            week_days.append(f"{day_str}: {symbol}")
        print("     " + " ".join(week_days))
        
        # Show today
        today_str = date.today().strftime('%a')
        is_today = date.today().isoformat() in [log['log_date'] for log in logs]
        symbol = "✅" if is_today else "⏳"
        print(f"\n  Today ({today_str}): {symbol}")
        
        # Ask to visualize
        if VIZ_AVAILABLE:
            visualize = input("\n📊 Generate visualization? (y/n): ").strip().lower()
            if visualize == 'y':
                self.visualizer.plot_habit_progress(habit, logs)
    
    def show_predictions(self, habit_id: str):
        """Show AI predictions for a habit"""
        if not ML_AVAILABLE:
            print("❌ AI features not available (install scikit-learn)")
            return
        
        if not habit_id:
            print("❌ Please provide habit ID: predict <id>")
            return
        
        try:
            habit_id = int(habit_id)
        except:
            print("❌ Invalid habit ID")
            return
        
        # Get habit
        habits = self.db.get_habits(active_only=False)
        habit = next((h for h in habits if h['id'] == habit_id), None)
        
        if not habit:
            print(f"❌ Habit {habit_id} not found")
            return
        
        print(f"\n🤖 AI Predictions for: {habit['name']}")
        print("="*50)
        
        # Check if model exists
        if habit_id not in self.predictor.models:
            print("⏳ No AI model found. Training now...")
            if not self.predictor.train_model(habit_id):
                print("❌ Not enough data to train AI model (need 10+ days of data)")
                return
            print("✅ Model trained!")
        
        # Get predictions for next 7 days
        predictions = self.predictor.predict_completion(habit_id, 7)
        
        if not predictions:
            print("❌ No predictions available")
            return
        
        print("\n📅 7-Day Prediction:")
        print("-" * 50)
        
        for pred in predictions:
            prob = pred['probability'] * 100
            emoji = "🔥" if prob > 75 else "💪" if prob > 50 else "⏳" if prob > 25 else "😴"
            day = pred['day_name']
            
            # Highlight weekend
            if pred['weekday'] >= 5:
                day = f"\033[91m{day}\033[0m"  # Red for weekend
            
            print(f"  {day}: {emoji} {prob:.1f}% chance of completion")
        
        # Best day recommendation
        best_day = max(predictions, key=lambda x: x['probability'])
        print(f"\n🎯 Best day to succeed: {best_day['day_name']} "
              f"({best_day['probability']*100:.1f}% probability)")
        
        # Tips
        print("\n💡 Tips for success:")
        if best_day['probability'] > 0.7:
            print("  ✅ You're likely to succeed! Keep up the good work!")
        else:
            print("  💪 Try breaking it into smaller steps")
            print("  ⏰ Set a specific time for the habit")
            print("  👥 Find an accountability partner")
    
    def analyze_habit(self, habit_id: str):
        """Analyze habit patterns"""
        if not habit_id:
            print("❌ Please provide habit ID: analyze <id>")
            return
        
        try:
            habit_id = int(habit_id)
        except:
            print("❌ Invalid habit ID")
            return
        
        # Get habit
        habits = self.db.get_habits(active_only=False)
        habit = next((h for h in habits if h['id'] == habit_id), None)
        
        if not habit:
            print(f"❌ Habit {habit_id} not found")
            return
        
        logs = self.db.get_logs(habit_id, 90)
        
        if not logs:
            print("📭 No data to analyze")
            return
        
        print(f"\n📈 Habit Analysis: {habit['name']}")
        print("="*50)
        
        # Calculate patterns
        total_days = 90
        completed_days = len(logs)
        
        print(f"  📊 Completion Rate: {(completed_days/total_days)*100:.1f}%")
        print(f"  🔥 Current Streak: {habit['current_streak']} days")
        print(f"  🏆 Longest Streak: {habit['longest_streak']} days")
        
        # Weekly patterns
        day_counts = defaultdict(int)
        day_totals = defaultdict(int)
        
        for log in logs:
            log_date = datetime.fromisoformat(log['log_date'])
            day_name = log_date.strftime('%A')
            day_counts[day_name] += 1
            day_totals[day_name] += 1
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        best_day = max(day_order, key=lambda d: day_counts.get(d, 0))
        worst_day = min(day_order, key=lambda d: day_counts.get(d, 0))
        
        print(f"\n  📅 Best day: {best_day} ({day_counts.get(best_day, 0)} completions)")
        print(f"  📅 Worst day: {worst_day} ({day_counts.get(worst_day, 0)} completions)")
        
        # Monthly trend
        monthly_counts = defaultdict(int)
        for log in logs:
            month = datetime.fromisoformat(log['log_date']).strftime('%Y-%m')
            monthly_counts[month] += 1
        
        if monthly_counts:
            best_month = max(monthly_counts, key=monthly_counts.get)
            print(f"\n  📆 Best month: {best_month} ({monthly_counts[best_month]} completions)")
    
    def show_stats(self):
        """Show overall statistics"""
        habits = self.db.get_habits()
        
        if not habits:
            print("📭 No habits to show statistics for")
            return
        
        print("\n📊 Overall Statistics")
        print("="*50)
        
        total_habits = len(habits)
        active_habits = sum(1 for h in habits if h['active'])
        
        print(f"  📝 Total habits: {total_habits}")
        print(f"  ✅ Active habits: {active_habits}")
        
        # Categories
        categories = {}
        for habit in habits:
            cat = habit['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n  🏷️  Categories:")
        for cat, count in categories.items():
            print(f"     • {cat}: {count} habit(s)")
        
        # Streak stats
        streaks = [h['current_streak'] for h in habits]
        best_streak = max(streaks) if streaks else 0
        
        print(f"\n  🔥 Best overall streak: {best_streak} days")
        
        # Today's progress
        today_completed = sum(1 for h in habits if h['today_completed'])
        print(f"\n  📅 Today: {today_completed}/{len(habits)} habits completed")
    
    def delete_habit(self, habit_id: str):
        """Delete a habit"""
        if not habit_id:
            print("❌ Please provide habit ID: delete <id>")
            return
        
        try:
            habit_id = int(habit_id)
        except:
            print("❌ Invalid habit ID")
            return
        
        confirm = input(f"⚠️  Delete habit {habit_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            if self.db.delete_habit(habit_id):
                print(f"🗑️  Habit {habit_id} deleted")
            else:
                print(f"❌ Failed to delete habit {habit_id}")
    
    def train_ai(self, habit_id: str):
        """Train AI model for a habit"""
        if not ML_AVAILABLE:
            print("❌ AI features not available (install scikit-learn)")
            return
        
        if not habit_id:
            print("❌ Please provide habit ID: train <id>")
            return
        
        try:
            habit_id = int(habit_id)
        except:
            print("❌ Invalid habit ID")
            return
        
        print(f"🧠 Training AI model for habit {habit_id}...")
        
        if self.predictor.train_model(habit_id):
            print("✅ AI model trained successfully!")
            
            # Show feature importance if available
            if habit_id in self.predictor.models:
                model = self.predictor.models[habit_id]
                if hasattr(model, 'feature_importances_'):
                    print("\n📊 Feature Importance:")
                    features = ['Day of Week', 'Day of Month', 'Month', 'Is Weekend',
                              'D-1', 'D-2', 'D-3', 'D-4', 'D-5', 'D-6', 'D-7',
                              'Rolling Avg', 'Streak']
                    importances = model.feature_importances_
                    
                    # Show top 5
                    indices = np.argsort(importances)[-5:]
                    for idx in reversed(indices):
                        print(f"  • {features[idx]}: {importances[idx]*100:.1f}%")
        else:
            print("❌ Model training failed. Need at least 10 days of data with variation.")

# ============== MAIN ==============

def main():
    """Main entry point"""
    print("\n" + "🚀"*30)
    print("  SMART HABIT TRACKER WITH AI PREDICTIONS")
    print("🚀"*30)
    
    # Check dependencies
    if not ML_AVAILABLE:
        print("\n⚠️  Install scikit-learn for AI features:")
        print("   pip install scikit-learn numpy")
    
    if not VIZ_AVAILABLE:
        print("\n⚠️  Install matplotlib for visualizations:")
        print("   pip install matplotlib")
    
    # Run the tracker
    tracker = SmartHabitTracker()
    tracker.run()

if __name__ == "__main__":
    main()