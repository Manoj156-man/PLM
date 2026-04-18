import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types based on our backend schemas
export interface Product {
  id: number;
  name: string;
  description: string;
  current_phase: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  product_id: number;
  title: string;
  description: string;
  assigned_to_agent: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Alert {
  id: number;
  product_id: number;
  severity: string;
  message: string;
  resolved: boolean;
  created_at: string;
  resolved_at: string | null;
}

export interface LifecycleEvent {
  id: number;
  product_id: number;
  phase: string;
  agent_id: string;
  event_type: string;
  description: string;
  timestamp: string;
}

export interface ProductDetail extends Product {
  tasks: Task[];
  alerts: Alert[];
  events: LifecycleEvent[];
}
