import { useTasks } from './api/tasks';
import { TaskForm } from './components/TaskForm';
import { TaskItem } from './components/TaskItem';
import styles from './App.module.css';

function App() {
  const { data: tasks, isLoading, isError } = useTasks();

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>Task Flow</h1>
      </header>
      
      <TaskForm />

      <main>
        {isLoading && <p style={{ textAlign: 'center' }}>Loading tasks...</p>}
        
        {isError && (
          <div style={{ color: 'var(--danger)', textAlign: 'center', padding: '20px' }}>
            Failed to load tasks. Is the backend running?
          </div>
        )}
        
        <div className={styles.list}>
          {tasks?.map((task) => (
            <TaskItem key={task.id} task={task} />
          ))}
          
          {!isLoading && tasks?.length === 0 && (
            <p style={{ textAlign: 'center', color: 'var(--text-secondary)', marginTop: '40px' }}>
              Your task list is empty. Time to be productive!
            </p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
