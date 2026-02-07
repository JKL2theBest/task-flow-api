import React from 'react';
import { format } from 'date-fns';
import { TaskStatus } from '../types/task';
import type { Task } from '../types/task';
import { useCompleteTask } from '../api/tasks';
import styles from './TaskItem.module.css';
import { clsx } from 'clsx';

interface Props {
  task: Task;
}

export const TaskItem: React.FC<Props> = ({ task }) => {
  const completeMutation = useCompleteTask();
  const isCompleted = task.status === TaskStatus.COMPLETED;

  return (
    <div className={clsx(styles.card, isCompleted && styles.completed)}>
      <div className={styles.content}>
        <h3>{task.title}</h3>
        {task.description && <p className={styles.description}>{task.description}</p>}
        
        <div className={styles.footer}>
          <span className={clsx(
            styles.status, 
            isCompleted ? styles.statusCompleted : styles.statusActive
          )}>
            {isCompleted ? 'Выполнена' : 'Активна'}
          </span>
          <span className={styles.date}>
            {format(new Date(task.created_at), 'MMM d, HH:mm')}
          </span>
        </div>
      </div>

      {!isCompleted && (
        <button
          className={styles.completeBtn}
          onClick={() => completeMutation.mutate(task.id)}
          disabled={completeMutation.isPending}
        >
          {completeMutation.isPending ? '...' : 'Готово'}
        </button>
      )}
    </div>
  );
};
