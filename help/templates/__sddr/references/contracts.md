# Contracts - Interfaces e Convenções Globais

Este documento é a **fonte da verdade** para interfaces, tipos e convenções compartilhadas entre todos os planos. Qualquer agente deve consultar este arquivo antes de criar interfaces ou tipos.

---

## Tipos de Dados Globais

### Entidades Base

```typescript
interface BaseEntity {
  id: string;
  created_at: string;
  updated_at: string;
  deleted_at?: string | null;
}

interface TenantEntity extends BaseEntity {
  tenant_id: string;
}
```

### Usuário

```typescript
interface User {
  id: string;
  tenant_id: string;
  email: string;
  name: string;
  avatar_url?: string | null;
  status: 'PENDING' | 'ACTIVE' | 'INACTIVE' | 'BLOCKED';
  role: Role;
  last_login_at?: string | null;
  created_at: string;
  updated_at: string;
}

interface Role {
  id: string;
  type: 'SUPER_ADMIN' | 'NUCLEO_NCK' | 'AGENTE_NCK' | 'CLIENTE' | 'FORNECEDOR' | 'INVESTIDOR';
  name: string;
  permissions: string[];
}
```

### Tenant

```typescript
interface Tenant {
  id: string;
  name: string;
  slug: string;
  domain?: string | null;
  logo_url?: string | null;
  status: 'ACTIVE' | 'SUSPENDED' | 'TRIAL';
  timezone: string;
}
```

### Projeto

```typescript
interface Project {
  id: string;
  tenant_id: string;
  name: string;
  slug: string;
  description?: string | null;
  status: 'PLANNING' | 'ACTIVE' | 'PAUSED' | 'COMPLETED' | 'ARCHIVED';
  work_mode: 'SCRUM' | 'KANBAN' | 'SIMPLE';
  color?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  created_at: string;
  updated_at: string;
}

interface ProjectMember {
  id: string;
  project_id: string;
  user_id: string;
  role: 'OWNER' | 'ADMIN' | 'MEMBER' | 'VIEWER';
  user: User;
  joined_at: string;
}
```

### Tarefa

```typescript
interface Task {
  id: string;
  tenant_id: string;
  project_id: string;
  sprint_id?: string | null;
  assignee_id?: string | null;
  title: string;
  description?: string | null;
  status: 'BACKLOG' | 'TODO' | 'IN_PROGRESS' | 'IN_REVIEW' | 'DONE' | 'CANCELLED';
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';
  order_index: number;
  estimated_hours?: number | null;
  actual_hours?: number | null;
  deadline?: string | null;
  completed_at?: string | null;
  assignee?: User | null;
  attachments?: Attachment[];
  created_at: string;
  updated_at: string;
}
```

### Sprint

```typescript
interface Sprint {
  id: string;
  tenant_id: string;
  project_id: string;
  name: string;
  goal?: string | null;
  status: 'PLANNING' | 'PLANNED' | 'ACTIVE' | 'COMPLETED' | 'CANCELLED';
  order_index: number;
  start_date?: string | null;
  end_date?: string | null;
  tasks?: Task[];
  created_at: string;
  updated_at: string;
}
```

### Nota

```typescript
interface Note {
  id: string;
  tenant_id: string;
  project_id?: string | null;
  task_id?: string | null;
  folder_id?: string | null;
  author_id: string;
  title: string;
  content: string;
  version: number;
  is_pinned: boolean;
  accent_color?: string | null;
  highlight_style: 'DEFAULT' | 'BOLD' | 'CALLOUT' | 'UNDERLINE';
  visibility: 'ALL_COMPANY' | 'FILTERED' | 'SPECIFIC_USERS';
  author: User;
  folder?: NoteFolder | null;
  attachments?: Attachment[];
  created_at: string;
  updated_at: string;
}

interface NoteFolder {
  id: string;
  tenant_id: string;
  parent_id?: string | null;
  name: string;
  accent_color?: string | null;
  children?: NoteFolder[];
  notes_count?: number;
  created_at: string;
  updated_at: string;
}

interface NoteVersion {
  id: string;
  note_id: string;
  content: string;
  version: number;
  created_by: string;
  created_at: string;
}
```

### Evento/Calendário

```typescript
interface Event {
  id: string;
  tenant_id: string;
  project_id?: string | null;
  title: string;
  description?: string | null;
  type: 'MEETING' | 'DEADLINE' | 'MILESTONE' | 'REMINDER' | 'DELIVERY' | 'OTHER';
  location?: string | null;
  meeting_url?: string | null;
  color?: string | null;
  start_at: string;
  end_at: string;
  timezone: string;
  is_all_day: boolean;
  recurrence_rule?: string | null;
  attendees?: EventAttendee[];
  created_at: string;
  updated_at: string;
}

interface EventAttendee {
  id: string;
  event_id: string;
  user_id: string;
  status: 'PENDING' | 'ACCEPTED' | 'DECLINED' | 'TENTATIVE';
  user: User;
  responded_at?: string | null;
}

interface MeetingRequest {
  id: string;
  tenant_id: string;
  project_id?: string | null;
  title: string;
  description?: string | null;
  location?: string | null;
  meeting_url?: string | null;
  proposed_start_at: string;
  proposed_end_at: string;
  status: 'PENDING' | 'ACCEPTED' | 'DECLINED' | 'RESCHEDULED';
  creator: User;
  recipients: MeetingRequestRecipient[];
  created_at: string;
  updated_at: string;
}

interface MeetingRequestRecipient {
  id: string;
  meeting_request_id: string;
  user_id: string;
  user: User;
}
```

### Notificação

```typescript
interface Notification {
  id: string;
  tenant_id: string;
  user_id: string;
  project_id?: string | null;
  type: NotificationType;
  title: string;
  message: string;
  data?: Record<string, any> | null;
  status: 'UNREAD' | 'READ' | 'ARCHIVED';
  read_at?: string | null;
  created_at: string;
}

type NotificationType =
  | 'TASK_CREATED'
  | 'TASK_UPDATED'
  | 'TASK_ASSIGNED'
  | 'NOTE_CREATED'
  | 'NOTE_UPDATED'
  | 'SPRINT_CREATED'
  | 'SPRINT_STARTED'
  | 'SPRINT_COMPLETED'
  | 'MEETING_REQUEST_CREATED'
  | 'MEETING_REQUEST_ACCEPTED'
  | 'MEETING_REQUEST_DECLINED'
  | 'MEETING_REQUEST_RESCHEDULED';
```

### Business Model Canvas

```typescript
interface BusinessModelCanvas {
  id: string;
  tenant_id: string;
  project_id: string;
  name: string;
  description?: string | null;
  blocks: CanvasBlocks;
  assumptions?: CanvasAssumption[];
  experiments?: CanvasExperiment[];
  last_analysis?: Record<string, any> | null;
  created_at: string;
  updated_at: string;
}

interface CanvasBlocks {
  key_partners: string[];
  key_activities: string[];
  key_resources: string[];
  value_propositions: string[];
  customer_relationships: string[];
  channels: string[];
  customer_segments: string[];
  cost_structure: string[];
  revenue_streams: string[];
}

interface CanvasAssumption {
  id: string;
  text: string;
  validated: boolean;
}

interface CanvasExperiment {
  id: string;
  hypothesis: string;
  method: string;
  result?: string;
  status: 'pending' | 'running' | 'completed';
}
```

### Caverna do Dragão

```typescript
interface DragonSettings {
  id: string;
  tenant_id: string;
  max_capacity_morning: number;
  max_capacity_afternoon: number;
  tickets_per_week: number;
  advance_days: number;
  enabled: boolean;
}

interface DragonTicket {
  id: string;
  tenant_id: string;
  user_id: string;
  week_start: string;
  total_tickets: number;
  used_tickets: number;
  remaining_tickets: number;
}

interface DragonReservation {
  id: string;
  tenant_id: string;
  user_id: string;
  date: string;
  period: 'MORNING' | 'AFTERNOON';
  status: 'CONFIRMED' | 'CANCELLED' | 'COMPLETED' | 'NO_SHOW';
  checked_in_at?: string | null;
  user: User;
  created_at: string;
}
```

### Anexos

```typescript
interface Attachment {
  id: string;
  tenant_id: string;
  entity_type: 'task' | 'note' | 'project';
  entity_id: string;
  filename: string;
  original_name: string;
  mime_type: string;
  size: number;
  url: string;
  uploaded_by: string;
  created_at: string;
}
```

### Timeline

```typescript
interface TimelineEntry {
  id: string;
  tenant_id: string;
  user_id: string;
  project_id?: string | null;
  entity_type: string;
  entity_id: string;
  action: TimelineAction;
  old_value?: Record<string, any> | null;
  new_value?: Record<string, any> | null;
  user: User;
  created_at: string;
}

type TimelineAction =
  | 'CREATED'
  | 'UPDATED'
  | 'DELETED'
  | 'STATUS_CHANGED'
  | 'MEMBER_ADDED'
  | 'MEMBER_REMOVED'
  | 'ASSIGNED'
  | 'UNASSIGNED'
  | 'COMMENT_ADDED'
  | 'VERSION_CREATED';
```

---

## API Responses

### Padrão de Resposta

```typescript
interface ApiResponse<T> {
  data: T;
  message?: string;
}

interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    per_page: number;
    total_pages: number;
  };
}

interface ApiError {
  statusCode: number;
  message: string;
  error?: string;
}
```

### Autenticação

```typescript
interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: User;
  tenant: Tenant;
}

interface RefreshRequest {
  refresh_token: string;
}

interface RefreshResponse {
  access_token: string;
  refresh_token: string;
}

interface MagicLinkRequest {
  email: string;
}

interface MagicLinkVerifyRequest {
  token: string;
}
```

---

## Convenções de API

### Base URL
```
Produção: https://api.nckia.com.br/api/v1
Desenvolvimento: http://192.168.x.x:3000/api/v1
```

### Headers Obrigatórios
```
Authorization: Bearer <access_token>
Content-Type: application/json
X-Tenant-ID: <tenant_id>  (opcional, inferido do token)
```

### Endpoints por Módulo

| Módulo | Base Path |
|--------|-----------|
| Auth | `/auth` |
| Users | `/users` |
| Projects | `/projects` |
| Tasks | `/tasks` |
| Sprints | `/sprints` |
| Notes | `/notes` |
| Note Folders | `/note-folders` |
| Events | `/events` |
| Calendar | `/calendar` |
| Meeting Requests | `/meeting-requests` |
| Notifications | `/notifications` |
| Canvas | `/canvas` |
| Caverna Dragão | `/caverna-dragao` |
| Timeline | `/timeline` |
| Attachments | `/attachments` |

---

## Stores (Zustand)

### Convenção de Nomes

```typescript
// Arquivo: stores/auth.store.ts
interface AuthStore {
  // State
  user: User | null;
  tenant: Tenant | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refresh: () => Promise<void>;
  setUser: (user: User) => void;
}
```

### Stores Globais

| Store | Responsabilidade | Plano |
|-------|------------------|-------|
| `auth.store.ts` | Autenticação e usuário logado | 02 |
| `project.store.ts` | Projeto selecionado | 05 |
| `notification.store.ts` | Contadores e badges | 10 |
| `theme.store.ts` | Tema claro/escuro | 01 |

---

## Componentes Globais

### Providos pelo Plano 01

| Componente | Descrição |
|------------|-----------|
| `Button` | Botão com variantes (primary, secondary, outline, ghost) |
| `Input` | Campo de texto com label e erro |
| `Card` | Container com sombra e bordas |
| `Avatar` | Imagem de perfil circular |
| `Badge` | Etiqueta de status |
| `Skeleton` | Loading placeholder |
| `Modal` | Dialog modal |
| `Toast` | Notificação toast |
| `LoadingScreen` | Tela de carregamento full-screen |
| `EmptyState` | Estado vazio com ícone e mensagem |
| `ErrorState` | Estado de erro com retry |

### Props Padrão

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  fullWidth?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  onPress: () => void;
  children: React.ReactNode;
}

interface InputProps {
  label?: string;
  placeholder?: string;
  error?: string;
  secureTextEntry?: boolean;
  keyboardType?: KeyboardTypeOptions;
  autoCapitalize?: 'none' | 'sentences' | 'words' | 'characters';
  value: string;
  onChangeText: (text: string) => void;
}
```

---

## Tema

### Cores

```typescript
const colors = {
  // Primary
  primary: {
    50: '#EEF2FF',
    100: '#E0E7FF',
    500: '#6366F1',
    600: '#4F46E5',
    700: '#4338CA',
  },
  
  // Neutral (Dark theme base)
  neutral: {
    50: '#F9FAFB',
    100: '#F3F4F6',
    200: '#E5E7EB',
    300: '#D1D5DB',
    400: '#9CA3AF',
    500: '#6B7280',
    600: '#4B5563',
    700: '#374151',
    800: '#1F2937',
    900: '#111827',
    950: '#0F172A',
  },
  
  // Semantic
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  info: '#3B82F6',
};

// Dark theme (padrão)
const darkTheme = {
  background: colors.neutral[950],
  surface: colors.neutral[900],
  surfaceSecondary: colors.neutral[800],
  text: colors.neutral[50],
  textSecondary: colors.neutral[400],
  border: colors.neutral[700],
  primary: colors.primary[500],
};
```

### Espaçamento

```typescript
const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};
```

### Tipografia

```typescript
const typography = {
  h1: { fontSize: 32, fontWeight: '700', lineHeight: 40 },
  h2: { fontSize: 24, fontWeight: '600', lineHeight: 32 },
  h3: { fontSize: 20, fontWeight: '600', lineHeight: 28 },
  body: { fontSize: 16, fontWeight: '400', lineHeight: 24 },
  bodySmall: { fontSize: 14, fontWeight: '400', lineHeight: 20 },
  caption: { fontSize: 12, fontWeight: '400', lineHeight: 16 },
};
```

---

## Resolução de Conflitos

1. **Este arquivo (contracts.md)** é a fonte da verdade
2. Em caso de conflito, usar a definição deste arquivo
3. Se precisar alterar um tipo, atualizar AQUI primeiro
4. Planos com número menor têm precedência em conflitos de implementação

---

## Changelog

| Data | Alteração |
|------|-----------|
| 2026-02-05 | Versão inicial com todos os tipos |
