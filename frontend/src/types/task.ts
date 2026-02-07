export enum TaskStatus {
  ACTIVE = 'active',
  COMPLETED = 'completed',
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}
