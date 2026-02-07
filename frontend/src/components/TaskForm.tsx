import React, { useState } from 'react';
import { useCreateTask } from '../api/tasks';
import styles from './TaskForm.module.css';

export const TaskForm: React.FC = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const createMutation = useCreateTask();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    createMutation.mutate(
      { title, description },
      {
        onSuccess: () => {
          setTitle('');
          setDescription('');
        },
      }
    );
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <div className={styles.inputs}>
        <input
          className={styles.input}
          type="text"
          placeholder="Заголовок новой задачи..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <textarea
          className={styles.textarea}
          placeholder="Описание (опционально)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>
      <button 
        type="submit" 
        className={styles.submitBtn} 
        disabled={createMutation.isPending}
      >
        {createMutation.isPending ? 'Добавление...' : 'Добавить задачу'}
      </button>
    </form>
  );
};
